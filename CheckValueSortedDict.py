from sortedcollections import ValueSortedDict

sdram_tracker = ValueSortedDict(lambda x: -x)
sdram_tracker["one"] = 1
sdram_tracker["two"] = 2

print(sdram_tracker.items())