import sys, getopt
import math
sys.path.insert(0, './lib')
from Matrix import *
from File import FileIn, FileOut
from Element import Element
from Methods import Jacobi

def distance(ax, ay, bx, by):
    return( math.sqrt(pow(bx - ax, 2) + pow(by - ay, 2)))

def load_truss(inputfile):
    truss = FileIn(inputfile)

    list_of_elements = []

    for i in range(len(truss.element_groups)):
        element_id = i
        incidence = [truss.incidences[i][1], truss.incidences[i][2]]
        ax = truss.coordinates[incidence[0] - 1][1]
        ay = truss.coordinates[incidence[0] - 1][2]
        bx = truss.coordinates[incidence[1] - 1][1]
        by = truss.coordinates[incidence[1] - 1][2]
        l = distance(ax, ay, bx, by)
        # print(l)
        e = truss.materials[i][0]
        area = truss.geometric_properties[i][0]
        cos = math.fabs(bx - ax) / l
        sin = math.fabs(by - ay) / l
        restrictions_dof = []
        for j in range(len(truss.bc_nodes)):
            if(truss.bc_nodes[j][0] in incidence):
                restrictions_dof.append(j+1) 
       
        element = Element(element_id, incidence, l, area, cos, sin, e, restrictions_dof)
        list_of_elements.append(element)

    return truss, list_of_elements

def computeGlobalRigid(truss, list_of_elements):
    nodes = len(truss.coordinates)
    m_global = Matrix(2*nodes, 2*nodes)
    for i in range(len(list_of_elements)):
        element = list_of_elements[i]
        dof = []
        for l in range(len(element.incidence)):
            incidence = element.incidence[l]
            dof.append((incidence*2)-1)
            dof.append(incidence*2)
        # print(dof)
        for j in range(element.rigid.rows):
            for k in range(element.rigid.cols):
                m_global.data[dof[j]-1][dof[k]-1] += element.rigid.data[j][k]
    return m_global

def computeRestrictedDofs(truss):
    # print(a.bc_nodes)
    dof_k = []
    for i in range(len(truss.bc_nodes)):
        first = truss.bc_nodes[i][0]
        second = truss.bc_nodes[i][1]
        r = first*2
        if (second == 1):
            r-=1
        dof_k.append(r)

    # print(dof_k)
    return dof_k

def computeCleanGlobalRigid(m_global, dof_k):
    vector = []
    for i in range(m_global.rows):
        for j in range(m_global.cols):
            if(((i+1) not in dof_k) and ((j+1) not in dof_k)):
                vector.append(m_global.data[i][j])

    gg = Matrix.listToMatrix(vector,m_global.rows-len(dof_k), m_global.rows-len(dof_k))
    return gg

def computeLoadMatrix(truss, gg, dof_k):
    nodes = len(truss.coordinates)
    loadsr = [0] * 2 * nodes
    for i in range(len(truss.loads)):
        first = truss.loads[i][0]
        second = truss.loads[i][1]
        r = first*2
        if (second == 1):
            r-=1
        loadsr[int(r)-1]  = truss.loads[i][2]   


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
    return m_dis


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Usage is: test.py -i <inputfile> -o <outputfile> or test.py -h for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        else:
            print('An error ocurred, type "test.py -h for help"')
            sys.exit()

    print('Input file is:', inputfile)
    print('Output file is:', outputfile)
    print('')

    truss, list_of_elements = load_truss(inputfile)
    m_global = computeGlobalRigid(truss, list_of_elements)
    dof_k = computeRestrictedDofs(truss)
    gg = computeCleanGlobalRigid(m_global, dof_k)
    m_dis = computeLoadMatrix(truss, gg, dof_k)
    m_dis.console()
    print('')

    output = FileOut(outputfile)
    output.writeOutputFile()

if __name__ == "__main__":
    main(sys.argv[1:])
