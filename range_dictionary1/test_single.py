from range_dictionary.old.range_dictionary_single import RangeDictionary

start = 0
end = 200
default = dict()
default["start"] = start
default["end"] = end
full = RangeDictionary(start, end, default)

print full
print full.all_get_ranges()
print full.get_by_value(45)

start = 25
end = 50
print full.get_ranges(start, end)
new = dict()
new["start"] = start
new["end"] = end

full.set_range(start, end, new)
print full.all_get_ranges()
print full.get_by_value(45)

start = 40
end = 70
print full.get_ranges(start, end)
new = dict()
new["start"] = start
new["end"] = end

full.set_range(start, end, new)
print full.all_get_ranges()
print full.get_by_value(45)

start = 10
end = 60
print full.get_ranges(start, end)
new = dict()
new["start"] = start
new["end"] = end

full.set_range(start, end, new)
print full.all_get_ranges()
print full.get_by_value(45)
