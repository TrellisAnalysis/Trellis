
import sys

# insert path to libs
sys.path.insert(0, './lib')
from Matrix import *
from File import File

a = File("in_test.txt")
print(a.element_groups)