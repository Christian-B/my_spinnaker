# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict
import os
import sqlite3


_DDL_FILE = os.path.join(os.path.dirname(__file__), "complex.sql")


class SqlLiteDatabase(object):
    """ Specific implementation of the Database for SQLite 3.

    .. note::
        NOT THREAD SAFE ON THE SAME DB.
        Threads can access different DBs just fine.

    .. note::
        This totally relies on the way SQLite's type affinities function.
        You can't port to a different database engine without a lot of work.
    """

    __slots__ = [
        # the database holding the data to store
        "_db",
    ]

    META_TABLES = ["global_metadata", "local_metadata"]

    def __init__(self, database_file=None):
        """
        :param str database_file: The name of a file that contains (or will\
            contain) an SQLite database holding the data. If omitted, an\
            unshared in-memory database will be used.
        :type database_file: str
        """
        if database_file is None:
            database_file = ":memory:"  # Magic name!
        self._db = sqlite3.connect(database_file)
        self.__init_db()

    def __del__(self):
        self.close()

    def __enter__(self):
        """ Start method is use in a ``with`` statement
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ End method if used in a ``with`` statement.

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.close()

    def close(self):
        """ Finalises and closes the database.
        """
        if self._db is not None:
            self._db.close()
            self._db = None

    def __init_db(self):
        """ Set up the database if required.
        """
        self._db.row_factory = sqlite3.Row
        with open(_DDL_FILE) as f:
            sql = f.read()
        self._db.executescript(sql)

    def _get_raw_table(self, source_name, variable_name, neuron_ids):
        with self._db:
            for row in self._db.execute(
                    """
                    SELECT raw_table
                    FROM local_metadata
                    WHERE source_name = ? AND variable_name = ? 
                        AND first_neuron_id = ?
                    LIMIT 1
                    """, (source_name, variable_name, neuron_ids[0])):
                return row["table_name"]

        return self._create_matrix_table(source_name, variable_name, neuron_ids)

    def table_name(self,  source_name, variable_name):
        return source_name + "_" + variable_name

    def _create_matrix_table(self,  source_name, variable_name, neuron_ids):
        with self._db:
            ordered_view = self.table_name(source_name, variable_name) + "_" + str(neuron_ids[0])
            raw_table = ordered_view + "_raw"

            # Create the raw table
            timestamp = "timestamp INTEGER PRIMARY KEY ASC"
            neuron_ids_str = ",".join(["'" + str(id) + "' INTEGER" for id in neuron_ids])
            ddl_statement = "CREATE TABLE {} ({}, {})".format(
                raw_table, timestamp, neuron_ids_str)
            self._db.execute(ddl_statement)

            ddl_statement = "CREATE VIEW {} AS SELECT * FROM {} ORDER BY timestamp".format(
                ordered_view, raw_table)
            self._db.execute(ddl_statement)

            # save the raw_table and ordered_view
            self._db.execute(
                """
                INSERT INTO local_metadata(
                    source_name, variable_name, raw_table, ordered_view, first_neuron_id, n_neurons) 
                VALUES(?,?,?,?,?,?)
                """, (source_name, variable_name, raw_table, ordered_view, neuron_ids[0], len(neuron_ids)))

            return raw_table

    def _get_global_table(self, source_name, variable_name):
        with self._db:
            for row in self._db.execute(
                    """
                    SELECT view_name FROM global_metadata
                    WHERE source_name = ? AND variable_name = ?
                    LIMIT 1
                    """, (source_name, variable_name)):
                return row["view_name"]
        self._create_full_views(source_name, variable_name)
        return self._create_global_metadata(source_name, variable_name)

    def _create_full_views(self, source_name, variable_name):
        with self._db:
            ordered_views = []
            first_neuron_ids = []
            for row in self._db.execute(
                    """
                    SELECT ordered_view, first_neuron_id
                    FROM local_metadata
                    WHERE source_name = ? AND variable_name = ?
                    ORDER BY first_neuron_id
                    """, (source_name, variable_name)):
                ordered_views.append(row["ordered_view"])
                first_neuron_ids.append(row["first_neuron_id"])
        if len(ordered_views) == 0:
            raise Exception("No data for source {} and variable {}".format(
                source_name, variable_name))
        full_views = self.create_full_views(source_name, variable_name, ordered_views)
        for i in range(len(first_neuron_ids)):
            print(source_name, variable_name, full_views[i], first_neuron_ids[i])
            self._db.execute(
                """
                UPDATE local_metadata 
                SET full_view = ? 
                WHERE source_name = ? and variable_name = ? and first_neuron_id = ?
                """,
                (full_views[i], source_name, variable_name, first_neuron_ids[i]))

    def create_full_views(self, source_name, variable_name, ordered_views):
        index_view = self.table_name(source_name, variable_name) + "_indexes"
        ddl_statement = " CREATE VIEW {} AS SELECT timestamp FROM {}".format(
            index_view, ordered_views[0])
        for i in range(1, len(ordered_views)):
            ddl_statement += " UNION SELECT timestamp from {}".format(
                ordered_views[i])
        self._db.execute(ddl_statement)

        if len(ordered_views) == 1:
            return ordered_views

        full_views = []
        with self._db:
            for row in self._db.execute(
                    "SELECT COUNT(*) as count FROM {}".format(index_view)):
                full_count = row["count"]

            for ordered_view in ordered_views:
                for row in self._db.execute(
                        "SELECT COUNT(*) as count FROM {}".format(ordered_view)):
                    local_count = row["count"]

                if local_count == full_count:
                    full_views.append(ordered_view)
                else:
                    full_views.append(self._create_full_view(index_view, ordered_view))
        return full_views

    def _create_full_view(self, index_view, ordered_view):
        with self._db:
            full_view = ordered_view + "_full"
            ddl_statement = """
                CREATE VIEW {} 
                AS SELECT * FROM {} LEFT JOIN {} USING (timestamp)
                """
            ddl_statement = ddl_statement.format(full_view, index_view, ordered_view)
            self._db.execute(ddl_statement)
        return full_view

    def _create_global_metadata(self, source_name, variable_name):
        with self._db:
            full_views = []
            total_n_neurons = 0
            for row in self._db.execute(
                    """
                    SELECT full_view, n_neurons FROM local_metadata
                    WHERE source_name = ? AND variable_name = ?
                    ORDER BY first_neuron_id
                    """, (source_name, variable_name)):
                full_views.append(row["full_view"])
                total_n_neurons += row["n_neurons"]

            print("total_n_neurons: ", total_n_neurons)
            if total_n_neurons < 1991:
                return self._create_global_views(
                    source_name, variable_name, full_views)
        return None
    # def _create_index_view(self):

    def _create_global_views(self, source_name, variable_name, table_names):
            view_name = self.table_name(source_name, variable_name)
            ddl_statement = "CREATE VIEW {} AS SELECT * FROM {}".format(
                view_name, " NATURAL JOIN ".join(table_names))
            print(ddl_statement)
            with self._db:
                self._db.execute(ddl_statement)
                self._db.execute(
                    """
                    INSERT INTO global_metadata(
                        source_name, variable_name, view_name) 
                    VALUES(?,?,?)
                    """,
                    (source_name, variable_name, view_name))
            with self._db:
                cursor = self._db.cursor()
                query = "SELECT * FROM {}".format(view_name)
                print(query)
                cursor.execute(query)
                names = [description[0] for description in cursor.description]

            fields = names[0]
            for name in names[1:]:
                fields += ", '{0}' / 65536.0 AS '{0}'".format(name)
            ddl_statement = "CREATE VIEW {} AS SELECT {} FROM {}".format(
                view_name+"_as_float", fields, view_name)
            self._db.execute(ddl_statement)

            return view_name

    def insert_items(self, source_name, variable_name, neuron_ids, data):
        table_name = self._get_raw_table(
            source_name, variable_name, neuron_ids)
        with self._db:
            cursor = self._db.cursor()
            # Get the column names
            cursor.execute("SELECT * FROM {}".format(table_name))
            query = "INSERT INTO {} VALUES ({})".format(
                table_name, ",".join("?" for _ in cursor.description))
            print(query)
            cursor.executemany(query, data)

    def clear_ds(self):
        """ Clear all saved data specification data
        """
        with self._db:
            names = [row["name"]
                            for row in self._db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'")]
            for name in self.META_TABLES:
                names.remove(name)
            for name in names:
                self._db.execute("DROP TABLE " + name)
            self._db.execute("DELETE FROM local_metadata")
            names = [row["name"]
                            for row in self._db.execute(
                    "SELECT name FROM sqlite_master WHERE type='view'")]
            for name in names:
                self._db.execute("DROP VIEW " + name)
            for name in self.META_TABLES:
                self._db.execute("DELETE FROM " + name)

    def get_variable_map(self):
        variables = defaultdict(list)
        with self._db:
            for row in self._db.execute(
                    """
                    SELECT source_name, variable_name 
                    FROM local_metadata 
                    GROUP BY source_name, variable_name
                    """):
                variables[row["source_name"]].append(row["variable_name"])
        return variables

    def create_views(self):
        variables = self.get_variable_map()
        for source_name, variables in variables.iteritems():
            for variable_name in variables:
                self._get_global_table(source_name, variable_name)

    def get_data(self, source_name, variable_name):
        view_name = self._get_global_table(source_name, variable_name)
        if view_name:
            return self._get_data(view_name)

    def _get_data(self, table_name):
        with self._db:
            cursor = self._db.cursor()
            cursor.execute("SELECT * FROM {}".format(table_name))
            names = [description[0] for description in cursor.description]
            data = [list(row[:]) for row in cursor.fetchall()]
            return names, data
