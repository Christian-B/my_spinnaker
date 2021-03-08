# Copyright (c) 2017-2020 The University of Manchester
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

import random
from complex import SqlLiteDatabase

def random_data(timesteps, neuron_ids):
    data = []
    for timestep in timesteps:
        line = []
        line.append(timestep)
        for _ in neuron_ids:
            line.append(random.randint(0, 100000000))
        data.append(line)
    return data

def insert(source_name, variable_name, timesteps, neuron_ids):
    data = random_data(timesteps, neuron_ids)
    db.insert_matrix(source_name, variable_name, neuron_ids, data)

db = SqlLiteDatabase("complex.sqlite3")
db.clear_ds()

source_name = "population1"
variable_name = "voltage"
neuron_ids = range(10)
timesteps =range(1, 100, 2)
insert(source_name, variable_name, timesteps, neuron_ids)
timesteps =range(100, 200)
insert(source_name, variable_name, timesteps, neuron_ids)

neuron_ids = range(10, 30, 2)
timesteps =range(0, 100, 2)
insert(source_name, variable_name, timesteps, neuron_ids)
timesteps =range(100, 200)
insert(source_name, variable_name, timesteps, neuron_ids)

source_name = "population1"
variable_name = "gsyn"
neuron_ids = range(10)
timesteps =range(100)
insert(source_name, variable_name, timesteps, neuron_ids)

source_name = "pop2"
variable_name = "voltage"
neuron_ids = range(20)
timesteps =range(100)
insert(source_name, variable_name, timesteps, neuron_ids)

#print(db.get_sources())
print(db.get_variable_map())

print("population1", "voltage")
neurons_ids, timestamps, data = db.get_matrix_data("population1", "voltage")
print(neurons_ids.shape, timestamps.shape, data.shape)

print("pop2", "voltage")
neurons_ids, timestamps, data = db.get_matrix_data("pop2", "voltage")
print(neurons_ids.shape, timestamps.shape, data.shape)

print("population1", "gsyn")
neurons_ids, timestamps, data = db.get_matrix_data("population1", "gsyn")
print(neurons_ids.shape, timestamps.shape, data.shape)
db.close()
