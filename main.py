import sys, getopt
import math
sys.path.insert(0, './lib')
from Matrix import *
from File import FileIn, FileOut
from Element import Element
from Methods import Jacobi

def distance(ax, ay, bx, by):
    return (math.sqrt(pow(bx - ax, 2) + pow(by - ay, 2)))

def distance2(a, b):
    return (math.sqrt(pow(a, 2) + pow(b, 2)))

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
        length = distance(ax, ay, bx, by)
        e = truss.materials[i][0]
        area = truss.geometric_properties[i][0]
        cos = math.fabs(bx - ax) / length
        sin = math.fabs(by - ay) / length
        restrictions_dof = []
        for j in range(len(truss.bc_nodes)):
            if(truss.bc_nodes[j][0] in incidence):
                restrictions_dof.append(j+1) 
       
        element = Element(element_id, incidence, length, area, cos, sin, e, restrictions_dof)
        list_of_elements.append(element)

    return truss, list_of_elements

def computeGlobalRigid(truss, list_of_elements):
    nodes = len(truss.coordinates)
    global_rigid_matrix = Matrix(2*nodes, 2*nodes)
    for i in range(len(list_of_elements)):
        element = list_of_elements[i]
        dof = []
        for length in range(len(element.incidence)):
            incidence = element.incidence[length]
            dof.append((incidence*2)-1)
            dof.append(incidence*2)
        # print(dof)
        for j in range(element.rigid.rows):
            for k in range(element.rigid.cols):
                global_rigid_matrix.data[dof[j]-1][dof[k]-1] += element.rigid.data[j][k]
    return global_rigid_matrix

def computeRestrictedDofs(truss):
    # print(a.bc_nodes)
    restricted_dofs = []
    for i in range(len(truss.bc_nodes)):
        first = truss.bc_nodes[i][0]
        second = truss.bc_nodes[i][1]
        r = first*2
        if (second == 1):
            r-=1
        restricted_dofs.append(r)

    # print(restricted_dofs)
    return restricted_dofs

def computeCleanGlobalRigid(global_rigid_matrix, restricted_dofs):
    vector = []
    for i in range(global_rigid_matrix.rows):
        for j in range(global_rigid_matrix.cols):
            if(((i+1) not in restricted_dofs) and ((j+1) not in restricted_dofs)):
                vector.append(global_rigid_matrix.data[i][j])

    clean_rigid_matrix = Matrix.listToMatrix(vector,global_rigid_matrix.rows-len(restricted_dofs), global_rigid_matrix.rows-len(restricted_dofs))
    return clean_rigid_matrix

def computeLoadMatrix(truss, clean_rigid_matrix, restricted_dofs):
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
    for j in range(len(loadsr)):
        if (j+1) not in restricted_dofs:
            loadsr_finale.append(loadsr[j])
    list_loads = []


    for k in range(len(loadsr_finale)):
        list_loads.append([loadsr_finale[k]])

    list_loads = Matrix.arrayToMatrix(list_loads)
    r, error, iterations = Jacobi(100, 0.0001, clean_rigid_matrix, list_loads)

    l_finale = []

    vv = [0] * nodes * 2
    k = 0
    for l in range (len(vv)):
        if((l+1) not in restricted_dofs):
            vv[l] = r.data[k][0]
            k+=1
            
    displacement_matrix = Matrix.listToMatrix(vv, len(vv), 1)
    return displacement_matrix

def computeStressesStrains(list_of_elements, displacement_matrix):
    list_stress = []
    list_strain = []
    for i in range(len(list_of_elements)):
        dof = []
        element = list_of_elements[i]
        for length in range(len(element.incidence)):
            incidence = element.incidence[length]
            dof.append((incidence*2)-1)
            dof.append(incidence*2)

        current_displacement = []
        for j in range(len(displacement_matrix.data)):
            if j+1 in dof:
                current_displacement.append(displacement_matrix.data[j][0])
        current_displacement = Matrix.listToMatrix(current_displacement, len(current_displacement), 1)

        m_result = Matrix.s_multiply(element.m,(1/element.length))
        m_result = Matrix.s_multiply(m_result,current_displacement)
        stress = distance2(m_result.data[0][0],m_result.data[1][0])
        # m_result.console(True)
        strain = stress * element.e
        # print(strain)
        list_strain.append(strain)
        list_stress.append(stress)
    return list_stress, list_strain


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
    global_rigid_matrix = computeGlobalRigid(truss, list_of_elements)
    restricted_dofs = computeRestrictedDofs(truss)
    clean_rigid_matrix = computeCleanGlobalRigid(global_rigid_matrix, restricted_dofs)
    displacement_matrix = computeLoadMatrix(truss, clean_rigid_matrix, restricted_dofs)
    displacement_matrix.console()
    reaction_forces = 0
    stresses, strains = computeStressesStrains(list_of_elements, displacement_matrix)

    output = FileOut(outputfile, truss, Matrix.toArray(displacement_matrix), reaction_forces, stresses, strains)
    output.writeOutputFile()

if __name__ == "__main__":
    main(sys.argv[1:])
