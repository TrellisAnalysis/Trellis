class File:

    def __init__(self, path):
        self.path = path
        self.number_of_nodes = None
        self.number_of_element_groups = None
        self.number_of_materials = None
        self.number_of_geometric_properties = None
        self.number_of_bcnodes = None
        self.number_of_loads = None
        self.coordinates = self.getCoordinates()
        self.element_groups = self.getElement_groups()
        self.incidences = self.getIncidences()
        self.materials = self.getMaterials()
        self.geometric_properties = self.getGeometric_properties()
        self.bc_nodes = self.getBC_nodes()
        self.loads = self.getLoads()


    def getCoordinates(self):
        f = open(self.path, 'r')
        linha = f.readline()
        while ("*COORDINATES" not in linha):
            linha = f.readline()
        self.number_of_nodes = int(f.readline().split(' ')[0])
        coordinates = []
        for i in range(self.number_of_nodes):
            coordinates.append([float(x) for x in f.readline().split()])
        return coordinates

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

    def getMaterials(self):
        f = open(self.path, 'r')
        linha = f.readline()
        while ("*MATERIALS" not in linha):
            linha = f.readline()
        self.number_of_materials = int(f.readline().split(' ')[0])
        materials = []
        for i in range(self.number_of_materials):
            materials.append([float(x) for x in f.readline().split()])
        return materials
    
    def getGeometric_properties(self):
        f = open(self.path, 'r')
        linha = f.readline()
        while ("*GEOMETRIC_PROPERTIES" not in linha):
            linha = f.readline()
        self.number_of_geometric_properties = int(f.readline().split(' ')[0])
        geometric_properties = []
        for i in range(self.number_of_geometric_properties):
            geometric_properties.append([float(x) for x in f.readline().split()])
        return geometric_properties
    
    def getBC_nodes(self):
        f = open(self.path, 'r')
        linha = f.readline()
        while ("*BCNODES" not in linha):
            linha = f.readline()
        self.number_of_bcnodes = int(f.readline().split(' ')[0])
        bc_nodes = []
        for i in range(self.number_of_bcnodes):
            bc_nodes.append([float(x) for x in f.readline().split()])
        return bc_nodes

    def getLoads(self):
        f = open(self.path, 'r')
        linha = f.readline()
        while ("*LOADS" not in linha):
            linha = f.readline()
        self.number_of_loads = int(f.readline().split(' ')[0])
        loads = []
        for i in range(self.number_of_loads):
            loads.append([float(x) for x in f.readline().split()])
        return loads
