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
import numpy
import os
import sqlite3


_DDL_FILE = os.path.join(os.path.dirname(__file__), "complex.sql")
_VIEW_CUTOFFF = 1990  # test as 1999 but with safety


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

    def insert_items(self, source_name, variable_name, neuron_ids, data):
        with self._db:
            raw_table = self._get_raw_table(
                source_name, variable_name, neuron_ids)
            cursor = self._db.cursor()
            # Get the column names
            cursor.execute("SELECT * FROM {}".format(raw_table))
            query = "INSERT INTO {} VALUES ({})".format(
                raw_table, ",".join("?" for _ in cursor.description))
            print(query)
            cursor.executemany(query, data)

            index_table = self._get_index_table(source_name, variable_name)
            query = "INSERT OR IGNORE INTO {} VALUES(?)".format(index_table)
            print(query)
            indexes = [[row[0]] for row in data]
            print(indexes)
            self._db.executemany(query, indexes)

    def _get_raw_table(self, source_name, variable_name, neuron_ids):
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

    def _create_matrix_table(self,  source_name, variable_name, neuron_ids):
        full_view = self._table_name(source_name, variable_name) + "_" + str(neuron_ids[0])
        raw_table = full_view + "_raw"

        # Create the raw table
        timestamp = "timestamp INTEGER PRIMARY KEY ASC"
        neuron_ids_str = ",".join(["'" + str(id) + "' INTEGER" for id in neuron_ids])
        ddl_statement = "CREATE TABLE {} ({}, {})".format(
            raw_table, timestamp, neuron_ids_str)
        self._db.execute(ddl_statement)

        index_table = self._get_index_table(source_name, variable_name)

        # create full view
        ddl_statement = """
            CREATE VIEW {} 
            AS SELECT * FROM {} LEFT JOIN {} USING (timestamp)
            """
        ddl_statement = ddl_statement.format(full_view, index_table, raw_table)
        self._db.execute(ddl_statement)

        self._db.execute(
            """
            INSERT INTO local_metadata(
                source_name, variable_name, raw_table, full_view, 
                first_neuron_id) 
            VALUES(?,?,?,?,?)
            """,
            (source_name, variable_name, raw_table, full_view, neuron_ids[0]))

        self._update_global_view(
            source_name, variable_name, full_view, len(neuron_ids))

        return raw_table

    def _table_name(self, source_name, variable_name):
        return source_name + "_" + variable_name

    def _get_index_table(self, source_name, variable_name):
        for row in self._db.execute(
                """
                SELECT index_table FROM global_metadata
                WHERE source_name = ? AND variable_name = ?
                LIMIT 1
                """, (source_name, variable_name)):
            return row["index_table"]

        # Create the index table
        index_table = self._table_name(source_name, variable_name) + "_indexes"
        ddl_statement = "CREATE TABLE {} (timestamp INTEGER PRIMARY KEY ASC)"
        ddl_statement = ddl_statement.format(index_table)
        self._db.execute(ddl_statement)

        # Register the index table
        #
        self._db.execute(
            """
            INSERT INTO global_metadata(
                source_name, variable_name, index_table, n_neurons) 
            VALUES(?,?,?, ?)
            """, (source_name, variable_name, index_table, 0))

        return index_table

    def _update_global_view(
            self, source_name, variable_name, local_view, n_neurons):
        for row in self._db.execute(
            """
            SELECT view_name, n_neurons FROM global_metadata
            WHERE source_name = ? AND variable_name = ?
            LIMIT 1
            """, (source_name, variable_name)):
            view_name = row["view_name"]
            old_n_neurons = row["n_neurons"]

        new_n_neurons = old_n_neurons + n_neurons
        if old_n_neurons == 0:
            global_view = local_view
        elif old_n_neurons < _VIEW_CUTOFFF:
            global_view = self._table_name(source_name, variable_name) + "_all"
            ddl_statement = "DROP VIEW IF EXISTS {}".format(global_view)
            self._db.execute(ddl_statement)
            if new_n_neurons < _VIEW_CUTOFFF:
                self._create_global_view(
                    source_name, variable_name, global_view)
            else:
                global_view = None
        else:
            global_view = None

        self._db.execute(
            """
            UPDATE global_metadata 
            SET view_name = ?, n_neurons = ?
            WHERE source_name = ? and variable_name = ?
            """,
            (global_view, new_n_neurons, source_name, variable_name))

    def _create_global_view(self, source_name, variable_name, global_view):
        local_views = self._get_local_views(source_name, variable_name)
        ddl_statement = "CREATE VIEW {} AS SELECT * FROM {}".format(
                global_view, " NATURAL JOIN ".join(local_views))
        print(ddl_statement)
        self._db.execute(ddl_statement)

    def _get_local_views(self, source_name, variable_name):
        local_views = []
        for row in self._db.execute(
                """
                SELECT full_view
                FROM local_metadata
                WHERE source_name = ? AND variable_name = ?
                ORDER BY first_neuron_id
                """, (source_name, variable_name)):
            local_views.append(row["full_view"])
        return local_views

    def _get_global_table(self, source_name, variable_name):
         for row in self._db.execute(
                """
                SELECT view_name FROM global_metadata
                WHERE source_name = ? AND variable_name = ?
                LIMIT 1
                """, (source_name, variable_name)):
            return row["view_name"]

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

    def get_data(self, source_name, variable_name):
        #with self._db:
        #    view_name = self._get_global_table(source_name, variable_name)
        #    if view_name:
        #        return self._get_data(view_name)

        local_views = self._get_local_views(source_name, variable_name)
        all_neurons_ids = []
        all_local_data = []
        for local_view in local_views:
            local_neurons_ids, timestamps, local_data = self._get_data(
                local_view)
            all_neurons_ids.append(local_neurons_ids)
            all_local_data.append(local_data)
        neurons_ids = numpy.hstack(all_neurons_ids)
        data = numpy.hstack(all_local_data)
        return neurons_ids, timestamps, data

    def _get_data(self, table_name):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM {}".format(table_name))
        names = [description[0] for description in cursor.description]
        neurons_ids = [int(i) for i in names[1:]]
        timestamps = []
        data = []
        values = numpy.array(cursor.fetchall())
        #for row in cursor.fetchall():
        #    timestamps.append(row[0])
        #    data.append(row[1:])
        return neurons_ids, values[:, 0], values[:, 1:]