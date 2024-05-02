from spinn_utilities.config_holder import set_config
from spinnman.spalloc import SpallocClient
from spinnman.config_setup import unittest_setup


SPALLOC_URL = "https://spinnaker.cs.man.ac.uk/spalloc"
SPALLOC_USERNAME = "christian-test"
SPALLOC_PASSWORD = ""
SPALLOC_MACHINE = "SpiNNaker1M"

WIDTH = 1
HEIGHT = 1
x = 0
y = 3
b = 0

unittest_setup()
set_config("Machine", "version",5)
client = SpallocClient(SPALLOC_URL, SPALLOC_USERNAME, SPALLOC_PASSWORD)
job = client.create_job_rect_at_board(
    WIDTH, HEIGHT, triad=(x, y, b), machine_name=SPALLOC_MACHINE,
    max_dead_boards=3)
print(job)
print("Waiting until ready...")
with job:
    job.launch_keepalive_task()
    job.wait_until_ready()

    print(job.get_connections())
    txrx = job.create_transceiver()
    dims = txrx._get_machine_dimensions()
    print(f"{dims.height=}, {dims.width=}")

    input("Press Enter to release...")
client.close()#print(2^(1/(2^1)))