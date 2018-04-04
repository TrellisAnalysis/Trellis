import sys, getopt
import math
sys.path.insert(0, './lib')
from Matrix import *
from File import FileIn, FileOut
from Element import Element

def roundm(x):
    return round(x,3)

def distance(ax, ay, bx, by):
    return( math.sqrt(pow(bx - ax, 2) + pow(by - ay, 2)))

a = FileIn("in_test.txt")
list_of_elements = []
for i in range (len(a.element_groups)):
    element_id = i
    incidence = [a.incidences[i][1], a.incidences[i][2]]
    ax = a.coordinates[incidence[0] - 1][1]
    ay = a.coordinates[incidence[0] - 1][2]
    bx = a.coordinates[incidence[1] - 1][1]
    by = a.coordinates[incidence[1] - 1][2]
    l = distance(ax, ay, bx, by)
    # print(l)
    e = a.materials[i][0]
    area = a.geometric_properties[i][0]
    cos = math.fabs(bx - ax)/l
    sin = math.fabs(by - ay)/l
    restrictions_dof = []
    for j in range(len(a.bc_nodes)):
        if(a.bc_nodes[j][0] in incidence):
            restrictions_dof.append(j+1) 
       
        
    element = Element(element_id, incidence, l, area, cos, sin, e, restrictions_dof)
    list_of_elements.append(element)


# for j in range (len(list_of_elements)):
#     list_of_elements[j].console()
#     print("")


nodes = len(a.coordinates)
m_global = Matrix(2*nodes, 2*nodes)
for k in range(len(list_of_elements)):
    element = list_of_elements[k]
    dof = []
    for l in range(len(element.incidence)):
        incidence = element.incidence[l]
        dof.append((incidence*2)-1)
        dof.append(incidence*2)
    # print(dof)
    element.rigid.map(roundm)
    element.rigid.console()
    print("")
    for m in range(element.rigid.rows):
        for n in range(element.rigid.cols):
            m_global.data[dof[m]-1][dof[n]-1] += element.rigid.data[m][n]
            # m_global.data[dof[m]-1][dof[n]-1] += 1
m_global.map(roundm)
m_global.console()      
        

# if __name__ == "__main__":
#     main(sys.argv[1:])
