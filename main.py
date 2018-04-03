import sys, getopt
import math
sys.path.insert(0, './lib')
from Matrix import *
from File import FileIn, FileOut
from Element import Element


#top
def distance(ax, ay, bx, by):
    return (math.sqrt(pow(bx - ax, 2) + pow(by - ay, 2)))


def load_file(inputfile):
    a = FileIn(inputfile)
    list_of_elements = []
    for i in range(len(a.element_groups)):
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
        cos = math.fabs(bx - ax) / l
        sin = math.fabs(by - ay) / l
        dof = []
        for j in range(len(a.bc_nodes)):
            if (a.bc_nodes[j][0] in incidence):
                dof.append(j + 1)

        element = Element(element_id, incidence, l, area, cos, sin, e, dof)
        list_of_elements.append(element)

    ## print info
    # for j in range (len(list_of_elements)):
        #     list_of_elements[j].console()
        #     print("")


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

    load_file(inputfile)

    output = FileOut(outputfile)
    output.writeOutputFile()

if __name__ == "__main__":
    main(sys.argv[1:])
