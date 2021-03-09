-- Copyright (c) 2018-2019 The University of Manchester
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.

-- https://www.sqlite.org/pragma.html#pragma_synchronous
PRAGMA main.synchronous = OFF;

-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
-- A table assigning ids to source names
CREATE TABLE IF NOT EXISTS local_matrix_metadata(
	source_name STRING NOT NULL,
	variable_name STRING NOT NULL,
	raw_table STRING NOT NULL,
	full_view STRING,
	first_neuron_id INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS global_matrix_metadata(
	source_name STRING NOT NULL,
	variable_name STRING NOT NULL,
	index_table STRING NOT NULL,
	view_name STRING NULL,
	n_neurons INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS spikes_metadata(
	source_name STRING NOT NULL,
	variable_name STRING NOT NULL,
	data_table STRING NOT NULL);

CREATE TABLE IF NOT EXISTS counts_metadata(
	source_name STRING NOT NULL,
	variable_name STRING NOT NULL,
	data_table STRING NOT NULL);

