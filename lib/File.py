class FileIn:
    def __init__(self, path):
        self.path = path
        self.number_of_element_groups = None
        self.coordinates = self.getInfo("COORDINATES")
        self.element_groups = self.getElement_groups()
        self.incidences = self.getIncidences()  # todo: better function
        self.materials = self.getInfo("MATERIALS")
        self.geometric_properties = self.getInfo("GEOMETRIC_PROPERTIES")
        self.bc_nodes = self.getInfo("BCNODES")
        self.loads = self.getInfo("LOADS")

    def getInfo(self, info):
        f = open(self.path, 'r')
        line = f.readline()
        while (("*" + info) not in line):
            line = f.readline()
        iterator = int(f.readline().split(' ')[0])
        info_list = []
        if (info == "ELEMENT_GROUPS"):
            for i in range(iterator):
                info_list.append([x for x in f.readline().split()])
            for k in range(2):
                print(info_list)
                info_list[i][k] = int(info_list[i][k])

        else:
            for i in range(iterator):
                info_list.append([float(x) for x in f.readline().split()])
        return info_list

    def getElement_groups(self):
        f = open(self.path, 'r')
        linha = f.readline()
        while ("*ELEMENT_GROUPS" not in linha):
            linha = f.readline()
        self.number_of_element_groups = int(f.readline().split(' ')[0])
        element_groups = []
        for i in range(self.number_of_element_groups):
            element_groups.append([x for x in f.readline().split()])
            for k in range(2):
                element_groups[i][k] = int(element_groups[i][k])
        return element_groups

    def getIncidences(self):
        f = open(self.path, 'r')
        linha = f.readline()
        while ("*INCIDENCES" not in linha):
            linha = f.readline()
        incidences = []
        for i in range(self.number_of_element_groups):
            incidences.append([int(x) for x in f.readline().split()])
        return incidences

class FileOut:
    def __init__(self, file_name, truss, displacements, reaction_forces, vector_names, strains, stresses):
        self.file_name = file_name
        self.truss = truss
        self.displacements = displacements
        self.reaction_forces = reaction_forces
        self.element_strains = strains
        self.element_stresses = stresses
        self.vector_names = vector_names
    
    def writeOutputFile(self):
        file = open(self.file_name, "w")

        number_of_nodes = len(self.truss.incidences)

        file.write("*DISPLACEMENTS\n")
        k = 0
        for node in range(number_of_nodes):
            file.write("{0} {1} {2} {3}\n".format(node + 1, self.displacements[k], self.displacements[k + 1], 0))
            k+=2
        
        file.write("\n*REACTION_FORCES\n")
        for i in range(len(self.reaction_forces)):
            file.write("{0} {1} \n".format(self.vector_names[i], self.reaction_forces[i]))
        # for node in range(number_of_nodes):
        #     file.write("{0} {1}\n".format(node + 1, self.reaction_forces))
        
        file.write("\n*ELEMENT_STRAINS\n")
        for node in range(number_of_nodes):
            file.write("{0} {1}\n".format(node + 1, self.element_strains[node]))

        file.write("\n*ELEMENT_STRESSES\n")
        for node in range(number_of_nodes):
            file.write("{0} {1}\n".format(node + 1, self.element_stresses[node]))