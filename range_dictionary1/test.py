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

view = full.get_view_by_index(45)
print ("start", view["start"])

view_range = full.get_view_by_zone(start, end)
full.setitem_by_zone(25, 50, "start", 25)
print full.all_get_ranges()
print full.get_by_index(45)
print ("start", view.get_value("start"))

full.setitem_by_zone(35, 70, "end", 70)
for index_range in full.all_get_ranges():
    print (index_range , "  ",  full.get_by_range(index_range))

print full.has_key(45, "start")
print full.get_value(45, "start")

print full.has_key(45, "foo")
try:
    print full.get_value(45, "foo")
except KeyError as key_error:
    print key_error

view.setitem_by_index("middle", 45)
for index_range in full.all_get_ranges():
    print (index_range , "  ",  full.get_by_range(index_range))
