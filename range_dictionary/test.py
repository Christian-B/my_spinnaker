from range_dictionary import RangeDictionary

start = 0
end = 200
default = dict()
default["start"] = start
default["end"] = end

full =  RangeDictionary (start, end, default)

print full
print "--"
print full.keys()

view = full.view_by_index(45)
print ("start", view["start"])

view_range = full.view_by_zone(start, end)
full.setitem_by_zone(25, 50, "start", 25)
print full.get_ranges()
print full.view_by_index(45)
print ("start", view["start"])

full.setitem_by_zone(35, 70, "end", 70)
for index_range in full.get_ranges():
    print (index_range , "  ",  full.view_by_range(index_range))

print full.view_by_index(45).has_key("start")
print full.view_by_index(45)["start"]

print full.view_by_index(45).has_key("foo")
try:
    print full.get_value(45, "foo")
except KeyError as key_error:
    print key_error

view.setitem_by_index("middle", 45)
for index_range in full.all_get_ranges():
    print (index_range , "  ",  str(full.get_by_range(index_range)))
