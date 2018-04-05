import sys
sys.path.insert(0, './lib')
from Matrix import *


class Element:
    def __init__(self, element_id, incidence, l, area, c, s, e, restrictions_dof):
        self.element_id = element_id
        self.incidence = incidence
        self.length = l
        self.area = area
        self.cos = c
        self.sin = s
        self.e = e
        self.m = None
        self.rigid = self.computeRigid()
        self.restrictions_dof = restrictions_dof

    def console(self):
        print("ELEMENT_ID: {0}".format(self.element_id))
        print("INCIDENCE: {0}".format(self.incidence))
        print("LENGHT: {0}".format(self.length))
        print("AREA: {0}".format(self.area))
        print("COS: {0}".format(self.cos))
        print("SIN: {0}".format(self.sin))
        print("E: {0}".format(self.e))
        print("restrictions_dof: {0}".format(self.restrictions_dof))
        print("RIGID:")
        self.rigid.console()

    def computeRigid(self):
        c = self.cos
        s = self.sin
        matrix = [[c**2, c*s, -(c**2), -c*s],
                  [c*s, s**2, -(c*s), -(s**2)],
                  [-(c**2), -(c*s), c**2, c*s],
                  [-(c*s), -(s**2), c*s, s**2]]
        m = Matrix.arrayToMatrix(matrix)
        self.m = m
        return Matrix.s_multiply(m, (self.e * self.area) / self.length)
    
    
