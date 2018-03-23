class Element:
    def __init__(self, element_id, incidence, l, area, c, s):
        self.element_id = element_id
        self.incidence = incidence
        self.lenght = l
        self.cos = c
        self.sin = s
    
    def console(self):
        print("ELEMENT_ID: {0}".format(self.element_id))
        print("INCIDENCE: {0}".format(self.incidence))
        print("LENGHT: {0}".format(self.lenght))
        print("COS: {0}".format(self.cos))
        print("SIN: {0}".format(self.sin))
