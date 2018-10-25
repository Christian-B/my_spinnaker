import datetime

from vertex_levels import VertexLevels
from abstract_has_constraints \
    import AbstractHasConstraints

loops = 1000000
start = datetime.datetime.now()
for i in range(loops):
    vertex = VertexLevels()
    isinstance(vertex, AbstractHasConstraints)
mid = datetime.datetime.now()
vertex = VertexLevels()
for i in range(loops):
    isinstance(vertex, AbstractHasConstraints)
mid2 = datetime.datetime.now()
for i in range(loops):
    try:
        vertex.has_label()
    except Exception:
        print("oops")
end = datetime.datetime.now()
print(mid - start)
print(mid2 - mid)
print(end - mid2)
