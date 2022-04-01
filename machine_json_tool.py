import json
from spinn_machine.json_utils import (to_json, from_json_path)
import pyNN.spiNNaker as sim

n_boards = 480
n_chips_required = 0 - n_boards


sim.setup(timestep=1.0, n_chips_required=n_chips_required)
machine = sim.get_machine()
sim.end()
print("Got machine")

jpath = "{}board.json".format(n_boards)
j_machine = to_json(machine)
with open(jpath, "w") as f:
    json.dump(j_machine, f)

machine2 = from_json_path(jpath)

j_machine2 = to_json(machine2)
testpath = "test.json"
with open(testpath, "w") as f:
    json.dump(j_machine2, f)


assert j_machine == j_machine2
