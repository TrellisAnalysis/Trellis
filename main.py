
import sys

# insert path to libs
sys.path.insert(0, './lib')
from Matrix import *
from File import File

# a = File("in_test.txt")
# print(a.coordinates)
# print(a.element_groups)
# print(a.bc_nodes)
# print(a.materials)
# print(a.geometric_properties)
# print(a.loads)
 
# lists = [[4,7], [2,6]]
# b = toMatrix(lists)
# i = Matrix.inverse(b)
# i.console()

array = [[1,3],[1,2]]

a = Matrix.convert(array)

a.console()
