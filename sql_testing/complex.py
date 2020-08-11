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

    def _get_local_metadata(self, source_name, variable_name, neuron_ids):
        with self._db:
            for row in self._db.execute(
                    """
                    SELECT table_name, neuron_ids, n_neurons 
                    FROM local_metadata
                    WHERE source_name = ? AND variable_name = ? 
                        AND first_neuron_id = ?
                    LIMIT 1
                    """, (source_name, variable_name, neuron_ids[0])):
                return row["table_name"], row["neuron_ids"], row["n_neurons"]

        table_name = source_name + "_" + variable_name + "_" + str(neuron_ids[0])
        neuron_ids_str = ",".join(["'" + str(id) + "'" for id in neuron_ids])
        self._db.execute(
            """
            INSERT INTO local_metadata(
                source_name, variable_name, table_name, first_neuron_id, 
                n_neurons, neuron_ids) 
            VALUES(?,?,?,?,?,?)
            """, (source_name, variable_name, table_name, neuron_ids[0],
                  len(neuron_ids), neuron_ids_str))

        ddl_statement = "CREATE TABLE {} (timestamp, {})".format(
            table_name, neuron_ids_str)
        self._db.execute(ddl_statement)
        return table_name, neuron_ids_str, len(neuron_ids)

    def _get_global_metadata(self, source_name, variable_name):
        with self._db:
            for row in self._db.execute(
                    """
                    SELECT view_name, neuron_ids, n_neurons FROM global_metadata
                    WHERE source_name = ? AND variable_name = ?
                    LIMIT 1
                    """, (source_name, variable_name)):
                return row["view_name"], row["neuron_ids"], row["n_neurons"]

            table_names = []
            neuron_ids = None
            n_neurons = 0
            for row in self._db.execute(
                    """
                    SELECT table_name, neuron_ids, n_neurons FROM local_metadata
                    WHERE source_name = ? AND variable_name = ?
                    ORDER BY first_neuron_id
                    """, (source_name, variable_name)):
                table_names.append(row["table_name"])
                if  neuron_ids is None:
                    neuron_ids = row["neuron_ids"]
                else:
                    neuron_ids = "," + row["neuron_ids"]
                n_neurons += row["n_neurons"]

            view_name = source_name + "_" + variable_name
            ddl_statement = "CREATE VIEW {} AS SELECT * FROM {}".format(
                view_name, " NATURAL JOIN ".join(table_names))
            self._db.execute(ddl_statement)
            self._db.execute(
                """
                INSERT INTO global_metadata(
                    source_name, variable_name, view_name, n_neurons, neuron_ids) 
                VALUES(?,?,?,?,?)
                """,
                (source_name, variable_name, view_name, n_neurons, neuron_ids))

            return view_name, neuron_ids, n_neurons

    def insert_items(self, source_name, variable_name, neuron_ids, data):
        table_name, neuron_ids_str, n_neurons = self._get_local_metadata(
            source_name, variable_name, neuron_ids)
        query = "INSERT INTO {}(timestamp, {}) VALUES (?{})".format(
            table_name, neuron_ids_str, (",?" * n_neurons))
        print(query)
        with self._db:
            cursor = self._db.cursor()
            cursor.executemany(query, data)

    def clear_ds(self):
        """ Clear all saved data specification data
        """
        with self._db:
            tables_names = [row["table_name"]
                            for row in self._db.execute(
                    "SELECT table_name FROM local_metadata")]
            for table_name in tables_names:
                self._db.execute("DROP TABLE " + table_name)
            self._db.execute("DELETE FROM local_metadata")

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
                self._get_global_metadata(source_name, variable_name)

    def get_data(self, source_name, variable_name):
        view_name, neuron_ids_str, n_neurons = self._get_global_metadata(
            source_name, variable_name)
        with self._db:
            query = "SELECT * FROM {}".format(view_name)
            args = neuron_ids_str.split("'")
            args.insert(0, "timestamp")
            return [row[:] for row in self._db.execute(query)]
