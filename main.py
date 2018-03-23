import sys
# insert path to libs
sys.path.insert(0, './lib')
from Matrix import *
from File import File
from Element import Element

a = File("in_test.txt")
# print(a.coordinates)
print(a.element_groups)
# print(a.bc_nodes)
# print(a.materials)
# print(a.geometric_properties)
# print(a.loads)

list_of_elements = []
for i in range (len(a.element_groups)):
    element_id = a.element_groups[i][0]
    element = Element()

# lists = [[4,7], [2,6]]
# b = toMatrix(lists)
# i = Matrix.inverse(b)
# i.console()

