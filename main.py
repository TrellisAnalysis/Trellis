import sys
import math
sys.path.insert(0, './lib')
from Matrix import *
from File import File
from Element import Element
#top
def distance(ax, ay, bx, by):
    return( math.sqrt(pow(bx - ax, 2) + pow(by - ay, 2)))

a = File("in_test.txt")
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
    e = a.materials[i][0]
    area = a.geometric_properties[i][0]
    cos = math.fabs(bx - ax)/l
    sin = math.fabs(by - ay)/l
    dof = []
    for j in range(len(a.bc_nodes)):
        if(a.bc_nodes[j][0] in incidence):
            dof.append(j+1) 
       
        
    element = Element(element_id, incidence, l, area, cos, sin, e, dof)
    list_of_elements.append(element)


## print info
# for j in range (len(list_of_elements)):
#     list_of_elements[j].console()
#     print("")


