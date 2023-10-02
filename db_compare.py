# Copyright (c) 2024 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from spinn_front_end_common.utilities.sqlite_db import SQLiteDB


def table_names(db):
    names = []
    for row in db.execute(
            """
            SELECT name
            FROM sqlite_schema
            WHERE type ='table' AND name NOT LIKE 'sqlite_%'
             """):
        names.append(row["name"])
    return names


def column_names(db, table):
    names = []
    for row in db.execute(
            """
            SELECT name
            FROM PRAGMA_TABLE_INFO(?)
             """, (table, )):
        names.append(row["name"])
    return names


def get_data(db, table, column_names):
    data = []
    query = f"SELECT * FROM {table}"
    for row in db.execute(query):
        row_dict = {}
        for name in column_names:
            row_dict[name] = row[name]
        data.append(row_dict)
    return data

with SQLiteDB("/home/brenninc/spinnaker/my_spinnaker/reports/roc/run_1/ds.sqlite3", text_factory=str) as a:
    with SQLiteDB("/home/brenninc/spinnaker/my_spinnaker/reports/master/run_1/ds.sqlite3", text_factory=str) as b:

        a_tables = table_names(a)
        b_tables = table_names(b)
        assert a_tables == b_tables
        for table in a_tables:
            print(f"{table=}")
            a_columns = column_names(a, table)
            b_columns = column_names(b, table)
            print(f"{a_columns=}")
            assert a_columns == b_columns
            a_data = get_data(a, table, a_columns)
            b_data = get_data(b, table, a_columns)
            if a_data != b_data:
                assert len(a_data) == len(b_data)
                for a_row, b_row in zip(a_data, b_data):
                    if a_row != b_row:
                        print(a_row)
                        print(b_row)
                        for name in a_columns:
                            if a_row[name] != b_row[name]:
                                print(f"column name:{name}")
                                print(a_row[name])
                                print(b_row[name])
                        print("------")

        #print(a_tables)
        #column_names = column_names(a, a_tables[0])
        #print(column_names)
        #print(get_data(a, a_tables[0], column_names))


