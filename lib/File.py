class File:

    def __init__(self, path):
        self.path = path
        self.number_of_element_groups = None
        self.coordinates = self.getInfo("COORDINATES")
        self.element_groups = self.getElement_groups()
        self.incidences = self.getIncidences() # todo: better function
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
        if(info == "ELEMENT_GROUPS"):
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
