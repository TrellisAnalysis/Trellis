import sys, getopt
import math
sys.path.insert(0, './lib')
from Matrix import *
from File import FileIn, FileOut
from Element import Element
from Methods import Jacobi, GaussSeidel


def round2(x):
    return round(x,3)

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
    # res = Matrix.s_multiply(global_rigid_matrix,)

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

    return restricted_dofs

def computeCleanGlobalRigid(global_rigid_matrix, restricted_dofs):
    vector = []
    for i in range(global_rigid_matrix.rows):
        for j in range(global_rigid_matrix.cols):
            if(((i+1) not in restricted_dofs) and ((j+1) not in restricted_dofs)):
                vector.append(global_rigid_matrix.data[i][j])

    clean_rigid_matrix = Matrix.listToMatrix(vector,global_rigid_matrix.rows-len(restricted_dofs), global_rigid_matrix.rows-len(restricted_dofs))
    return clean_rigid_matrix

def computeLoadMatrix(truss, clean_rigid_matrix, restricted_dofs, method, max_iterations):
    nodes = len(truss.coordinates)
    global_load_vector = [0] * 2 * nodes
    for i in range(len(truss.loads)):
        first = truss.loads[i][0]
        second = truss.loads[i][1]
        r = first*2
        if (second == 1):
            r-=1
        global_load_vector[int(r)-1] = truss.loads[i][2]   

    load_vector = []
    for j in range(len(global_load_vector)):
        if (j+1) not in restricted_dofs:
            load_vector.append(global_load_vector[j])
    list_loads = []

    for k in range(len(load_vector)):
        list_loads.append([load_vector[k]])

    list_loads = Matrix.arrayToMatrix(list_loads)
    if(method != 'Gauss-Seidel'):
        result, error, iterations = Jacobi(max_iterations, 0.0000000001, clean_rigid_matrix, list_loads)
    else:
        result, error, iterations = GaussSeidel(max_iterations, 0.0000000001, clean_rigid_matrix, list_loads)
    
    displacements_vector = [0] * nodes * 2
    k = 0
    for l in range (len(displacements_vector)):
        if((l+1) not in restricted_dofs):
            displacements_vector[l] = result.data[k][0]
            k+=1
            
    displacement_matrix = Matrix.listToMatrix(displacements_vector, len(displacements_vector), 1)
    return displacement_matrix, iterations

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
        
        result_matrix = Matrix.s_multiply(element.transformation_matrix,(1/element.length))
        result_matrix = Matrix.s_multiply(result_matrix,current_displacement)
        stress = result_matrix.data[0][0]
        strain = stress * element.e
        list_strain.append(strain)
        list_stress.append(stress)
    return list_stress, list_strain

def computeReactionForces(m_global, displacement_matrix, loads, number_of_nodes):
    # loads = len(loads)
    # print(loads)
    forces_vector = Matrix.s_multiply(m_global, displacement_matrix)
    reaction_forces = []
    vector_names = []
    list_index = []
    forces_vector.map(round2)
    # forces_vector.console()

    for j in range (number_of_nodes):
        string_x = '{0} '.format(j+1) + 'FX' + ' ='
        string_y = '{0} '.format(j+1) + 'FY' + ' ='
        vector_names.append(string_x)
        vector_names.append(string_y)
    vector_names_finale = [] # desculpa borba :(
    for i in range(len(loads)):
        first = loads[i][0]
        second = loads[i][1]
        r = first*2
        if (second == 1):
            r-=1
        r -=1
        list_index.append(int(r))

    for k in range(forces_vector.rows):
        if (k not in list_index) and (forces_vector.data[k][0] != 0):
            vector_names_finale.append(vector_names[k])
            reaction_forces.append(forces_vector.data[k][0])
    return reaction_forces, vector_names_finale
    
        


def main(argv):
    inputfile = ''
    outputfile = ''
    method = 'Gauss-Seidel'
    iterations = 500
    try:
        opts, args = getopt.getopt(argv, "hi:o:m:n:", ["ifile=", "ofile=", "method=", "iterations="])
    except getopt.GetoptError:
        print('Usage is: main.py -i <inputfile> -o <outputfile> -m <method> -n <number of iterations> or test.py -h for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile> -m <method> -n <number of iterations>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-m", "--method"):
            method = arg
        elif opt in ("-n", "--iterations"):
            iterations = arg
        else:
            print('An error ocurred, type "test.py -h for help"')
            sys.exit()

    print('Input file is:', inputfile)
    print('Output file is:', outputfile)
    print("Using {0} method". format(method))

    truss, list_of_elements = load_truss(inputfile)
    global_rigid_matrix = computeGlobalRigid(truss, list_of_elements)
    restricted_dofs = computeRestrictedDofs(truss)
    clean_rigid_matrix = computeCleanGlobalRigid(global_rigid_matrix, restricted_dofs)
    displacement_matrix, iterations = computeLoadMatrix(truss, clean_rigid_matrix, restricted_dofs, method, int(iterations))
    res = Matrix.s_multiply(global_rigid_matrix,displacement_matrix)
    # res.console()
    # displacement_matrix.console()
    reaction_forces, vector_names = computeReactionForces(global_rigid_matrix, displacement_matrix, truss.loads, len(truss.coordinates))
    stresses, strains = computeStressesStrains(list_of_elements, displacement_matrix)

    output = FileOut(outputfile, truss, Matrix.toArray(displacement_matrix), reaction_forces, vector_names, stresses, strains)
    output.writeOutputFile()
    print('Number of iterations: {0}'. format(iterations + 1))
    print('')


if __name__ == "__main__":
    main(sys.argv[1:])
