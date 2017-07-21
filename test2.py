import os

asstring = os.environ.get('P7_INTEGRATION_FACTOR', "1")
print asstring
p7_integration_factor = float(asstring)
print p7_integration_factor
