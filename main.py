import sys
import math
# insert path to libs
sys.path.insert(0, './lib')
from Matrix import *
from File import File
from Element import Element


def distance(ax, ay, bx, by):
    return( math.sqrt(pow(bx - ax, 2) + pow(by - ay, 2)))



a = File("in_test.txt")
# print("COORDENADAS")
# print(a.coordinates)
# print("ELEMENT GROUPS")
# print(a.element_groups)
# print("INCIDENCES")
# print(a.incidences)
# print(a.bc_nodes)
# print(a.materials)
# print(a.geometric_properties)
# print(a.loads)

list_of_elements = []
for i in range (len(a.element_groups)):
    element_id = i
    incidence = [a.incidences[i][1], a.incidences[i][2]]
    ax = a.coordinates[incidence[0] - 1][1]
    ay = a.coordinates[incidence[0] - 1][2]
    bx = a.coordinates[incidence[1] - 1][1]
    by = a.coordinates[incidence[1] - 1][2]
    # print("ax: " + str(ax) + " ay: " + str(ay) + " bx: " + str(bx) + " by: " + str(by))
    l = distance(ax, ay, bx, by)
    # print(l)
    area = a.geometric_properties[i]
    cos = math.fabs(bx - ax)/l
    sin = math.fabs(by - ay)/l
    element = Element(element_id, incidence, l, area, cos, sin)
    list_of_elements.append(element)

for j in range (len(list_of_elements)):
    list_of_elements[j].console()
    print("")

# lists = [[4,7], [2,6]]
# b = toMatrix(lists)
# i = Matrix.inverse(b)
# i.console()

