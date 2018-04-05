import math
import random


class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []

        for i in range(self.rows):
            self.data.append([])
            for j in range(self.cols):
                self.data[i].append(0)

    def randomize(self):
        # Randomize Matrix
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = random.uniform(-1, 1)

    def console(self, complete=False):
        # Print Matrix data
        if (complete == True):
            print('ROWS: {0}'.format(self.rows))
            print('COLUMNS: {0}'.format(self.cols))
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                print(self.data[i][j], end=' ')
            print()

    @staticmethod
    def arrayToMatrix(array):
        # convert array to Matrix type
        a = len(array)
        try:
            b = len(array[0])
            result = Matrix(a, b)
            for i in range(result.rows):
                for j in range(result.cols):
                    result.data[i][j] = array[i][j]
        except TypeError:
            b = 1
            result = Matrix(a, b)
            for i in range(result.rows):
                result.data[i][0] = array[i]

        return result

    @staticmethod
    def listToMatrix(l, rows, cols):
        # transform vectors to Matrix type
        k = 0
        result = Matrix(rows, cols)
        for i in range(rows):
            for j in range(cols):
                result.data[i][j] = l[k]
                k+=1
        return result

    @staticmethod
    def transpose(a):
        # Transpose matrix
        transposed = Matrix(a.cols, a.rows)
        for i in range(a.rows):
            for j in range(a.cols):
                transposed.data[j][i] = a.data[i][j]
        return transposed

    @staticmethod
    def s_add(a, b):
        # If Matrix add number by number
        result = Matrix(a.rows, a.cols)
        if isinstance(b, Matrix):
            if a.rows == b.rows and a.cols == b.cols:
                for i in range(a.rows):
                    for j in range(a.cols):
                        result.data[i][j] = a.data[i][j] + b.data[i][j]
            else:
                print(
                    "The matrix should have the same numbers of rows and columns"
                )

        else:
            # If int add to all numbers of self.data
            for i in range(a.rows):
                for j in range(a.cols):
                    result.data[i][j] = a.data[i][j] + b
        return result

    def add(self, a):
        # If Matrix add number by number
        if isinstance(a, Matrix):
            if self.rows == a.rows and self.cols == a.cols:
                for i in range(self.rows):
                    for j in range(self.cols):
                        self.data[i][j] += a.data[i][j]
            else:
                print(
                    "The matrix should have the same numbers of rows and columns"
                )

        else:
            # If int add to all numbers of self.data
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] += a

    @staticmethod
    def s_subtract(a, b):
        # If Matrix subtract number by number
        result = Matrix(a.rows, a.cols)
        if isinstance(b, Matrix):
            if a.rows == b.rows and a.cols == b.cols:
                for i in range(a.rows):
                    for j in range(a.cols):
                        result.data[i][j] = a.data[i][j] - b.data[i][j]
            else:
                print(
                    "The matrix should have the same numbers of rows and columns"
                )

        else:
            # If int add to all numbers of self.data
            for i in range(a.rows):
                for j in range(a.cols):
                    result.data[i][j] = a.data[i][j] - b
        return result

    def subtract(self, a):
        # If Matrix add number by number
        if isinstance(a, Matrix):
            if self.rows == a.rows and self.cols == a.cols:
                for i in range(self.rows):
                    for j in range(self.cols):
                        self.data[i][j] -= a.data[i][j]
            else:
                print(
                    "The matrix should have the same numbers of rows and columns"
                )

        else:
            # If int add to all numbers of self.data
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] -= a

    @staticmethod
    def s_hadamard(a, b):
        if a.rows == b.rows and a.cols == b.cols:
            result = Matrix(a.rows, a.cols)
            for i in range(a.rows):
                for j in range(a.cols):
                    result.data[i][j] = a.data[i][j] * b.data[i][j]
            return result
        else:
            print("The number of columns and rows of A must be the same of B")

    def hadamard(self, a):
        if self.rows == a.rows and self.cols == a.cols:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] *= a.data[i][j]
        else:
            print("The number of columns and rows of A must be the same of B")

    @staticmethod
    def inverse(self):
        if (self.rows != self.cols):
            print(
                "The matrix should have the same numbers of rows and columns")
            return None
        else:
            if (self.rows == 2):
                result = Matrix(2, 2)
                result.data = [[self.data[1][1], -self.data[0][1]],
                               [-self.data[1][0], self.data[0][0]]]
                return (self.s_multiply(result, 1 / self.det()))

    @staticmethod
    def s_multiply(a, b):
        # If Matrix multiply matrix by matrix
        if isinstance(b, Matrix):
            if a.cols == b.rows:
                result = Matrix(a.rows, b.cols)
                for i in range(result.rows):
                    for j in range(result.cols):
                        total = 0
                        for k in range(a.cols):
                            total += a.data[i][k] * b.data[k][j]
                        result.data[i][j] = total

            else:
                print(
                    "The matrix should have the same numbers of rows and columns"
                )
                return None

        else:
            result = Matrix(a.rows, a.cols)
            # If int multiply to all numbers of self.data
            for i in range(a.rows):
                for j in range(a.cols):
                    result.data[i][j] = a.data[i][j] * b
        return result

    def det(self):
        if (self.cols == self.rows):
            if (self.rows == 2):
                # if matrix is 2x2
                return (self.data[0][0] * self.data[1][1]) - (
                    self.data[0][1] * self.data[1][0])

    @staticmethod
    # convert Matrix to array type
    def toArray(a):
        arr = []
        for i in range(a.rows):
            for j in range(a.cols):
                arr.append(a.data[i][j])
        return arr

    @staticmethod
    def s_map(a, f):
        result = Matrix(a.rows, a.cols)
        for i in range(a.rows):
            for j in range(a.cols):
                result.data[i][j] = f(a.data[i][j])
        return result

    def col_map(self, f):
        for i in range(self.rows):
            self.data[i] = f(self.data[i])

    def map(self, f):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = f(self.data[i][j])


class Identity(Matrix):
    def __init__(self, rows, cols):
        Matrix.__init__(self, rows, cols)
        for i in range(self.rows):
            for j in range(self.cols):
                if (i != j):
                    self.data[i][j] = 0
                else:
                    self.data[i][j] = 1
