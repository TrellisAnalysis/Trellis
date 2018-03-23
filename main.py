
import sys

# insert path to libs
sys.path.insert(0, './lib')
from Matrix import *
from File import File

a = File("in_test.txt")
print(a.coordinates)
print(a.element_groups)
print(a.bc_nodes)
print(a.materials)
print(a.geometric_properties)
print(a.loads)
 