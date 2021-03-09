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
_MATRIX = "matrix"
_SINGLE = "single"
_EVENT = "event"


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

    META_TABLES = ["metadata", "local_matrix_metadata"]

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
            names = [row["name"]
                            for row in self._db.execute(
                    "SELECT name FROM sqlite_master WHERE type='view'")]
            for name in names:
                self._db.execute("DROP VIEW " + name)
            for name in self.META_TABLES:
                self._db.execute("DELETE FROM " + name)

    def _table_name(self, source_name, variable_name):
        return source_name + "_" + variable_name

    def get_variable_map(self):
        with self._db:
            variables = defaultdict(list)
            for row in self._db.execute(
                    """
                    SELECT source_name, variable_name, data_type
                    FROM metadata 
                    GROUP BY source_name, variable_name, data_type
                    """):
                variables[row["source_name"]].append("{}:{}".format(
                    row["variable_name"], row["data_type"]))
            return variables

    def _check_table_exist(self, table_name):
        for _ in self._db.execute(
                """
                SELECT name FROM sqlite_master WHERE type='table' AND name=?
                LIMIT 1
                """, [table_name]):
            return True
        return False

    def _get_data_table(
            self, source_name, variable_name, data_type, create_table):
        for row in self._db.execute(
                """
                SELECT data_table, data_type
                FROM metadata
                WHERE source_name = ? AND variable_name = ?
                LIMIT 1
                """, (source_name, variable_name)):
            if data_type:
                assert(data_type == row["data_type"])
            return row["data_table"]

        if not create_table:
            raise Exception("No Data for {}:{}".format(
                source_name, variable_name))

        if data_type == _MATRIX:
            data_table = None  # data_table done later if at all
        elif data_type == _SINGLE:
            data_table = self._create_single_table(source_name, variable_name)
        elif data_type == _EVENT:
            data_table = self._create_event_table(source_name, variable_name)
        else:
            raise NotImplementedError(
                "No create table for datatype {}".format(data_type))

        self._db.execute(
            """
            INSERT OR IGNORE INTO metadata(
                source_name, variable_name, data_table, data_type, n_neurons) 
            VALUES(?,?,?,?,0)
            """, (source_name, variable_name, data_table, data_type))

        return data_table

    def _get_table_ids(self, table_name):
        cursor = self._db.cursor()
        # Get the column names
        cursor.execute("SELECT * FROM {} LIMIT 1".format(table_name))
        ids = [int(description[0]) for description in cursor.description[1:]]
        return ids

    def _get_column_data(self, table_name):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM {}".format(table_name))
        names = [description[0] for description in cursor.description]
        neurons_ids = numpy.array(names[1:], dtype=numpy.integer)
        values = numpy.array(cursor.fetchall())
        return neurons_ids, values[:, 0], values[:, 1:]

    # matrix data

    def insert_matrix(self, source_name, variable_name, neuron_ids, data):
        """
        Inserts matrix data into the database

        :param source_name:
        :param variable_name:
        :param neuron_ids:
        :param data:
        :return:
        """
        with self._db:
            raw_table = self._get_matrix_raw_table(
                source_name, variable_name, neuron_ids)

            cursor = self._db.cursor()
            # Get the number of columns
            cursor.execute("SELECT * FROM {} LIMIT 1".format(raw_table))
            query = "INSERT INTO {} VALUES ({})".format(
                raw_table, ",".join("?" for _ in cursor.description))
            print(query)
            cursor.executemany(query, data)

            index_table = self._get_matix_index_table(
                source_name, variable_name)
            query = "INSERT OR IGNORE INTO {} VALUES(?)".format(index_table)
            indexes = [[row[0]] for row in data]
            self._db.executemany(query, indexes)

    def _get_matrix_raw_table(self, source_name, variable_name, neuron_ids):
        for row in self._db.execute(
                """
                SELECT raw_table
                FROM local_matrix_metadata
                WHERE source_name = ? AND variable_name = ? 
                    AND first_neuron_id = ?
                LIMIT 1
                """, (source_name, variable_name, neuron_ids[0])):
            table_name = row["raw_table"]
            check_ids = self._get_table_ids(table_name)
            assert(check_ids == list(neuron_ids))
            return (table_name)

        return self._create_matrix_table(source_name, variable_name, neuron_ids)

    def _create_matrix_table(self,  source_name, variable_name, neuron_ids):
        full_view = self._table_name(source_name, variable_name) + "_" + str(neuron_ids[0])
        raw_table = full_view + "_raw"

        # Create the raw table
        timestamp = "timestamp INTEGER PRIMARY KEY ASC"
        neuron_ids_str = ",".join(["'" + str(id) + "' INTEGER" for id in neuron_ids])
        ddl_statement = "CREATE TABLE IF NOT EXISTS {} ({}, {})".format(
            raw_table, timestamp, neuron_ids_str)
        self._db.execute(ddl_statement)

        index_table = self._get_matix_index_table(source_name, variable_name)

        # create full view
        ddl_statement = """
            CREATE VIEW {} 
            AS SELECT * FROM {} LEFT JOIN {} USING (timestamp)
            """
        ddl_statement = ddl_statement.format(full_view, index_table, raw_table)
        self._db.execute(ddl_statement)

        self._db.execute(
            """
            INSERT OR IGNORE INTO local_matrix_metadata(
                source_name, variable_name, raw_table, full_view, 
                first_neuron_id) 
            VALUES(?,?,?,?,?)
            """,
            (source_name, variable_name, raw_table, full_view, neuron_ids[0]))

        self._get_data_table(source_name, variable_name, _MATRIX, True)

        self._update_global_matrix_view(
            source_name, variable_name, full_view, len(neuron_ids))

        return raw_table

    def _get_matix_index_table(self, source_name, variable_name):
        index_table = self._table_name(source_name, variable_name) + "_indexes"
        if self._check_table_exist(index_table):
            return index_table

        # Create the index table
        ddl_statement = """
            CREATE TABLE IF NOT EXISTS {} 
            (timestamp INTEGER PRIMARY KEY ASC)
            """.format(index_table)
        self._db.execute(ddl_statement)

        return index_table

    def _update_global_matrix_view(
            self, source_name, variable_name, local_view, n_neurons):
        self._db.execute(
            """
            UPDATE metadata 
            SET n_neurons = n_neurons + ?
            WHERE source_name = ? and variable_name = ?
            """,
            (n_neurons, source_name, variable_name))

        for row in self._db.execute(
            """
            SELECT n_neurons FROM metadata
            WHERE source_name = ? AND variable_name = ?
            LIMIT 1
            """, (source_name, variable_name)):
            new_n_neurons = row["n_neurons"]

        if new_n_neurons == n_neurons:
            global_view = local_view
        else:
            global_view = self._table_name(source_name, variable_name) + "_all"
            ddl_statement = "DROP VIEW IF EXISTS {}".format(global_view)
            self._db.execute(ddl_statement)
            if new_n_neurons < _VIEW_CUTOFFF:
                self._create_global_view(
                    source_name, variable_name, global_view)
            else:
                global_view = None

        self._db.execute(
            """
            UPDATE metadata 
            SET data_table = ?
            WHERE source_name = ? and variable_name = ?
            """,
            (global_view, source_name, variable_name))

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
                FROM local_matrix_metadata
                WHERE source_name = ? AND variable_name = ?
                ORDER BY first_neuron_id
                """, (source_name, variable_name)):
            local_views.append(row["full_view"])
        return local_views

    def get_matrix_data(self, source_name, variable_name):
        with self._db:
            view_name = self._get_data_table(
                source_name, variable_name, _MATRIX, False)
            if view_name:
                return self._get_column_data(view_name)

        local_views = self._get_local_views(source_name, variable_name)
        all_neurons_ids = []
        all_local_data = []
        for local_view in local_views:
            local_neurons_ids, timestamps, local_data = self._get_column_data(
                local_view)
            all_neurons_ids.append(local_neurons_ids)
            all_local_data.append(local_data)
        neurons_ids = numpy.hstack(all_neurons_ids)
        data = numpy.hstack(all_local_data)
        return neurons_ids, timestamps, data

    # Events data

    def insert_events(self, source_name, variable_name, data):
        with self._db:
            data_table = self._get_data_table(
                source_name, variable_name, _EVENT, True)
            query = "INSERT INTO {} VALUES (?, ?)".format(data_table)
            print(query)
            self._db.executemany(query, data)

    def _create_event_table(self, source_name, variable_name):
        data_table = self._table_name(source_name, variable_name)
        ddl_statement = """
            CREATE TABLE IF NOT EXISTS {} (
            timestamp INTEGER NOT NULL, 
            neuron_id INTEGER NOT NULL)
            """.format(data_table)
        self._db.execute(ddl_statement)
        return data_table

    def get_spike_data(self, source_name, variable_name):
        with self._db:
            data_table = self._get_data_table(
                source_name, variable_name, _EVENT, False)
            cursor = self._db.cursor()
            cursor.execute("SELECT * FROM {}".format(data_table))
            return numpy.array(cursor.fetchall())

    # counts data

    def insert_single(self, source_name, variable_name, id, data):
        with self._db:
            data_table = self._get_data_table(
                source_name, variable_name, _SINGLE, True)

            # Make sure a column exists for this id
            # Different cores will have different ids safetly needed
            ids_in_table = self._get_table_ids(data_table)
            if id not in ids_in_table:
                ddl = "ALTER TABLE {} ADD '{}' INTEGER".format(data_table, id)
                print(ddl)
                self._db.execute(ddl)

            # make sure rows exist for each timestamp
            query = "INSERT or IGNORE INTO {}(timestamp) VALUES (?)"
            query = query.format(data_table)
            print(query)
            timestamps = [[row[0]] for row in data]
            self._db.executemany(query, timestamps)

            # update the rows with the data
            query = "UPDATE {} SET '{}' = ? where timestamp = ?"
            query = query.format(data_table, id)
            print(query)
            values = [[row[1], row[0]] for row in data]
            self._db.executemany(query, values)

    def _create_single_table(self, source_name, variable_name):
        data_table = self._table_name(source_name, variable_name)
        ddl_statement = """
            CREATE TABLE  IF NOT EXISTS {} (
            timestamp INTEGER PRIMARY KEY ASC)
            """.format(data_table)
        self._db.execute(ddl_statement)
        return data_table

    def get_single_data(self, source_name, variable_name):
        with self._db:
            data_table = self._get_data_table(
                source_name, variable_name, _SINGLE, False)
            return self._get_column_data(data_table)