from Matrix import *

def Jacobi(it, tolerance, a, f):
    try_vector = Matrix(f.rows, 1)
    try_vector2 = Matrix(f.rows, 1)
    for iterations in range(it):
        tol = 0
        for i in range (try_vector.rows):
            sub = f.data[i][0]
            for j in range(f.rows):
                if (i != j):
                    sub -= a.data[i][j] * try_vector.data[j][0]
            sub /= a.data[i][i]
            try_vector2.data[i][0] = sub
            if(sub == 0):
                error = 1
            else:
                error = (sub - try_vector.data[i][0])/sub
            if(error < tol):
                tol +=1
        if(tol == f.rows):
            break
        for k in range (try_vector.rows):
            try_vector.data[k][0] = try_vector2.data[k][0]
    return try_vector2, error, iterations

it = 600
tolerance = 0.0001
list_a = [[3, -1, 0, 0],
          [-1, 3, 0, -2],
          [0, 0, 3, 1],
          [0, -2, 1, 3]]
a = Matrix.arrayToMatrix(list_a)
a = Matrix.s_multiply(a, 1/2*10e-5)
a.console()
list_f = [[0],[0], [0], [-1000]]
f = Matrix.arrayToMatrix(list_f) 
m, error, iterations = Jacobi(it, tolerance, a, f)
m.console()
# print(iterations)
