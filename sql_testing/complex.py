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
from enum import Enum
import numpy
import os
import sqlite3


class TABLE_TYPES(Enum):
    EVENT = 0
    SINGLE = 1
    MATRIX = 2


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
        """ Clear all saved data
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

    def _table_name(self, source, variable):
        """
        Get a table name based on source and variable names

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :rtype: str
        """
        return source + "_" + variable

    def get_variable_map(self):
        """
        Gets a map of sources to a list of variables:table_type

        :rtype: dict(list(str))
        """
        with self._db:
            variables = defaultdict(list)
            for row in self._db.execute(
                    """
                    SELECT source, variable, table_type
                    FROM metadata 
                    GROUP BY source, variable, table_type
                    """):
                variables[row["source"]].append("{}:{}".format(
                    row["variable"], row["table_type"]))
            return variables

    def _check_table_exist(self, table_name):
        """
        Support function to see if a table already exists

        :param str table_name: name of a Table
        :return: True if and l=only if the table exists
        :type: bool
        """
        for _ in self._db.execute(
                """
                SELECT name FROM sqlite_master WHERE type='table' AND name=?
                LIMIT 1
                """, [table_name]):
            return True
        return False

    def insert_data(self, source, variable, ids, data):
        """
        Inserts data into the database

        This call supports multiple types of ids/data using the ids param to
        identify the type

        If ids is None acts like a call to insert_events

        If ids is a single int acts like a call to insert_single

        If ids is a list of ints acts like a call to insert_matrix

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param data: A 2d matrix with the first column being the timestamp.
        :param ids: The ids for the data being added or None for events(spikes)
        :type ids: list(int), int, None
        :return:
        """
        if isinstance(ids, int):
            self.insert_single(source, variable, ids, data)
        elif ids is None:
            self.insert_events(source, variable, data)
        else:
            self.insert_matrix(source, variable, ids, data)

    def _get_data_table(
            self, source, variable, table_type, create_table):
        """
        Finds or if allowed creates a data table based on source and variable

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param table_type: Type of table to find or create
        :type table_type: TABLE_TYPES or None
        :param bool create_table:
        :return:
            The name and type of the Table.
            Name could be None if the data is too complex to get from a
            single table.
        type: (str, TABLE_TYPES) or (None, TABLE_TYPES)
        :raises:
            An Exception if an existing Table does not have the exected type
            An Expcetion if the table does not exists an create_table is False
        """
        for row in self._db.execute(
                """
                SELECT data_table, table_type
                FROM metadata
                WHERE source = ? AND variable = ?
                LIMIT 1
                """, (source, variable)):
            if table_type:
                assert(table_type.value == row["table_type"])
            return row["data_table"], row["table_type"]

        if not create_table:
            raise Exception("No Data for {}:{}".format(
                source, variable))

        if table_type == TABLE_TYPES.MATRIX:
            data_table = None  # data_table done later if at all
        elif table_type == TABLE_TYPES.SINGLE:
            data_table = self._create_single_table(source, variable)
        elif table_type == TABLE_TYPES.EVENT:
            data_table = self._create_event_table(source, variable)
        else:
            raise NotImplementedError(
                "No create table for datatype {}".format(table_type))

        self._db.execute(
            """
            INSERT OR IGNORE INTO metadata(
                source, variable, data_table, table_type, n_ids) 
            VALUES(?,?,?,?,0)
            """, (source, variable, data_table, table_type.value))

        return data_table, table_type

    def _get_table_ids(self, table_name):
        """
        Gets the ids for this table

        The assumption is that names of all but the first column are ids
        in a form that can be cast to int

        :param str table_name: Name of the table to check
        :rype: list(int)
        """
        cursor = self._db.cursor()
        # Get the column names
        cursor.execute("SELECT * FROM {} LIMIT 1".format(table_name))
        ids = [int(description[0]) for description in cursor.description[1:]]
        return ids

    def _get_column_data(self, table_name):
        """
        Gets the data from single column based database.

        The assumption is that names of all but the first column are ids
        in a form that can be cast to int

        :param str table_name: Name of the table to get data for
        :return: Three numpy arrays
            - The ids of the data
            - The timestamps of the data
            - The data with shape len(timestamp), len(ids)
        :rtype: (numpy.ndarray, numpy.ndarray, numpy.ndarray)
        """
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM {}".format(table_name))
        names = [description[0] for description in cursor.description]
        ids = numpy.array(names[1:], dtype=numpy.integer)
        values = numpy.array(cursor.fetchall())
        return ids, values[:, 0], values[:, 1:]

    def get_data(self, source, variable):
        """
        Gets the data for this source and variable name

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return: One or Three numpy arrays
            - The ids of the data (Not for event/spike data)
            - The timestamps of the data  (Not for event/spike data)
            - The data with shape len(timestamp), len(ids)
            or shape (2, X) timestamp, id
        :rtype: (numpy.ndarray, numpy.ndarray, numpy.ndarray) or numpy.ndarray
        """
        with self._db:
            data_table, table_type = self._get_data_table(
                source, variable, None, False)
            if table_type == TABLE_TYPES.MATRIX:
                return self._get_matrix_data(
                    source, variable, table_type)
            if table_type == TABLE_TYPES.SINGLE:
                return self._get_column_data(data_table)
            if table_type == TABLE_TYPES.EVENT:
                return self._get_events_data(data_table)

    def _clean_data(self, data):
        """
        If requires does any pre cleaning of the data

        For example numpy arrays are converted to lists

        :param data: the input data
        :return: The data as lists that can be used in queries
        """
        if isinstance(data, numpy.ndarray):
            return data.tolist()
        return data

    # matrix data

    def insert_matrix(self, source, variable, ids, data):
        """
        Inserts matrix data into the database

        This method can be called multiple times with the same source and
        variable, and multiple distinct ids lists. The assumption is that no
        id will be in more than one of these distinct lists,
        and that the lists will be in the same order each time.

        The data will be a 2D array where the first column is the timestamp
        and the one column for each id.

        There can ever only be a single value per timestamp, id pair.

        The get methods deal with missing data so there is not requirement
        that every timestamp has data for all ids lists.

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param list(int) ids: The ids for the data.
        :param data: 2d array of shape (X, len(ids)+1)
        :type data: iterable(iterable(int) or numpty.ndarray
        """
        data = self._clean_data(data)
        with self._db:
            raw_table = self._get_matrix_raw_table(
                source, variable, ids)

            cursor = self._db.cursor()
            # Get the number of columns
            cursor.execute("SELECT * FROM {} LIMIT 1".format(raw_table))
            query = "INSERT INTO {} VALUES ({})".format(
                raw_table, ",".join("?" for _ in cursor.description))
            print(query)
            cursor.executemany(query, data)

            index_table = self._get_matix_index_table(
                source, variable)
            query = "INSERT OR IGNORE INTO {} VALUES(?)".format(index_table)
            indexes = [[row[0]] for row in data]
            self._db.executemany(query, indexes)

    def _get_matrix_raw_table(self, source, variable, ids):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param ids:
        :return:
        """
        for row in self._db.execute(
                """
                SELECT raw_table
                FROM local_matrix_metadata
                WHERE source = ? AND variable = ? 
                    AND first_id = ?
                LIMIT 1
                """, (source, variable, ids[0])):
            table_name = row["raw_table"]
            check_ids = self._get_table_ids(table_name)
            assert(check_ids == list(ids))
            return (table_name)

        return self._create_matrix_table(source, variable, ids)

    def _create_matrix_table(self,  source, variable, ids):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param ids:
        :return:
        """
        full_view = self._table_name(source, variable) + "_" + str(ids[0])
        raw_table = full_view + "_raw"

        # Create the raw table
        timestamp = "timestamp INTEGER PRIMARY KEY ASC"
        ids_str = ",".join(["'" + str(id) + "' INTEGER" for id in ids])
        ddl_statement = "CREATE TABLE IF NOT EXISTS {} ({}, {})".format(
            raw_table, timestamp, ids_str)
        self._db.execute(ddl_statement)

        index_table = self._get_matix_index_table(source, variable)

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
                source, variable, raw_table, full_view, 
                first_id) 
            VALUES(?,?,?,?,?)
            """,
            (source, variable, raw_table, full_view, ids[0]))

        self._get_data_table(source, variable, TABLE_TYPES.MATRIX, True)

        self._update_global_matrix_view(
            source, variable, full_view, len(ids))

        return raw_table

    def _get_matix_index_table(self, source, variable):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return:
        """
        index_table = self._table_name(source, variable) + "_indexes"
        ddl_statement = """
            CREATE TABLE IF NOT EXISTS {} 
            (timestamp INTEGER PRIMARY KEY ASC)
            """.format(index_table)
        self._db.execute(ddl_statement)

        return index_table

    def _update_global_matrix_view(
            self, source, variable, local_view, n_ids):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param local_view:
        :param n_ids:
        :return:
        """
        self._db.execute(
            """
            UPDATE metadata 
            SET n_ids = n_ids + ?
            WHERE source = ? and variable = ?
            """,
            (n_ids, source, variable))

        for row in self._db.execute(
            """
            SELECT n_ids FROM metadata
            WHERE source = ? AND variable = ?
            LIMIT 1
            """, (source, variable)):
            new_n_ids = row["n_ids"]

        if new_n_ids == n_ids:
            global_view = local_view
        else:
            global_view = self._table_name(source, variable) + "_all"
            ddl_statement = "DROP VIEW IF EXISTS {}".format(global_view)
            self._db.execute(ddl_statement)
            if new_n_ids < _VIEW_CUTOFFF:
                self._create_global_view(
                    source, variable, global_view)
            else:
                global_view = None

        self._db.execute(
            """
            UPDATE metadata 
            SET data_table = ?
            WHERE source = ? and variable = ?
            """,
            (global_view, source, variable))

    def _create_global_view(self, source, variable, global_view):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param global_view:
        :return:
        """
        local_views = self._get_local_views(source, variable)
        ddl_statement = "CREATE VIEW {} AS SELECT * FROM {}".format(
                global_view, " NATURAL JOIN ".join(local_views))
        print(ddl_statement)
        self._db.execute(ddl_statement)

    def _get_local_views(self, source, variable):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return:
        """
        local_views = []
        for row in self._db.execute(
                """
                SELECT full_view
                FROM local_matrix_metadata
                WHERE source = ? AND variable = ?
                ORDER BY first_id
                """, (source, variable)):
            local_views.append(row["full_view"])
        return local_views

    def get_matrix_data(self, source, variable):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return:
        """
        with self._db:
            data_table, _ = self._get_data_table(
                source, variable, TABLE_TYPES.MATRIX, False)
            return self._get_matrix_data(
                source, variable, data_table)

    def _get_matrix_data(self, source, variable, data_table):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param data_table:
        :return:
        """
        if data_table:
            return self._get_column_data(data_table)

        local_views = self._get_local_views(source, variable)
        all_ids = []
        all_local_data = []
        for local_view in local_views:
            local_ids, timestamps, local_data = self._get_column_data(
                local_view)
            all_ids.append(local_ids)
            all_local_data.append(local_data)
        ids = numpy.hstack(all_ids)
        data = numpy.hstack(all_local_data)
        return ids, timestamps, data

    # Events data

    def insert_events(self, source, variable, data):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param data:
        :return:
        """
        data = self._clean_data(data)
        with self._db:
            data_table, _ = self._get_data_table(
                source, variable, TABLE_TYPES.EVENT, True)
            query = "INSERT INTO {} VALUES (?, ?)".format(data_table)
            print(query)
            self._db.executemany(query, data)

    def _create_event_table(self, source, variable):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return:
        """
        data_table = self._table_name(source, variable)
        ddl_statement = """
            CREATE TABLE IF NOT EXISTS {} (
            timestamp INTEGER NOT NULL, 
            id INTEGER NOT NULL)
            """.format(data_table)
        self._db.execute(ddl_statement)
        return data_table

    def get_events_data(self, source, variable):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return:
        """
        with self._db:
            data_table, _ = self._get_data_table(
                source, variable, TABLE_TYPES.EVENT, False)
            return self._get_events_data(data_table)

    def _get_events_data(self, data_table):
        """

        :param data_table:
        :return:
        """
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM {}".format(data_table))
        return numpy.array(cursor.fetchall())

    # counts data

    def insert_single(self, source, variable, id, data):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :param id:
        :param data:
        :return:
        """
        data = self._clean_data(data)
        with self._db:
            data_table, _ = self._get_data_table(
                source, variable, TABLE_TYPES.SINGLE, True)

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

    def _create_single_table(self, source, variable):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return:
        """
        data_table = self._table_name(source, variable)
        ddl_statement = """
            CREATE TABLE  IF NOT EXISTS {} (
            timestamp INTEGER PRIMARY KEY ASC)
            """.format(data_table)
        self._db.execute(ddl_statement)
        return data_table

    def get_single_data(self, source, variable):
        """

        :param str source: Name of the source for example the population
        :param str variable: Name of the variable
        :return:
        """
        with self._db:
            data_table, _ = self._get_data_table(
                source, variable, TABLE_TYPES.SINGLE, False)
            return self._get_column_data(data_table)