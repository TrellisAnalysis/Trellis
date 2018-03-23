class Element:
    def __init__(self, element_id, incidence, l, area, c, s, material):
        self.element_id = element_id
        self.incidence = incidence
        self.lenght = l
        self.cos = c
        self.sin = s
        self.material = material