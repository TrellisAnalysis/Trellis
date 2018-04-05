import sys, getopt
import math
sys.path.insert(0, './lib')
from Matrix import *
from File import FileIn, FileOut
from Element import Element
from Methods import Jacobi


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
    for m in range(element.rigid.rows):
        for n in range(element.rigid.cols):
            m_global.data[dof[m]-1][dof[n]-1] += element.rigid.data[m][n]

# print(a.bc_nodes)
dof_k = []
for o in range(len(a.bc_nodes)):
    first = a.bc_nodes[o][0]
    second = a.bc_nodes[o][1]
    r = first*2
    if (second == 1):
        r-=1
    dof_k.append(r)

# print(dof_k)

vector = []
for p in range(m_global.rows):
    for q in range(m_global.cols):
        if(((p+1) not in dof_k) and ((q+1) not in dof_k)):
            vector.append(m_global.data[p][q])

gg = Matrix.listToMatrix(vector,m_global.rows-len(dof_k), m_global.rows-len(dof_k))


loadsr = [0] * 2 * nodes
for o in range(len(a.loads)):
    first = a.loads[o][0]
    second = a.loads[o][1]
    r = first*2
    if (second == 1):
        r-=1
    loadsr[int(r)-1]  = a.loads[o][2]   


loadsr_finale = []
for y in range(len(loadsr)):
    if (y+1) not in dof_k:
        loadsr_finale.append(loadsr[y])
list_loads = []


for i in range(len(loadsr_finale)):
    list_loads.append([loadsr_finale[i]])

list_loads = Matrix.arrayToMatrix(list_loads)
r, error, iterations = Jacobi(100, 0.0001, gg, list_loads)

l_finale = []

vv = [0] * nodes * 2
k = 0
for s in range (len(vv)):
    if((s+1) not in dof_k):
        vv[s] = r.data[k][0]
        k+=1
        
m_dis = Matrix.listToMatrix(vv, nodes, 2)
m_dis.console()
tension_list = []
for i in range(len(list_of_elements)):
    element = list_of_elements[i]
