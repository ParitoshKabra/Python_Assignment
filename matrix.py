import copy


class Matrix:
    def __init__(self, *args):
        try:
            var = len(args[0])
            for item in args:
                length = len(item)
                if length > var:
                    var = length
            for item in args:
                length = len(item)
                if length < var:
                    while length < var:
                        item.append(0)
                        length += 1
            self.mat = args
        except (IndexError, ValueError):
            self.mat = []

    # def __init__(self, other):
    #     # self.mat = []
    #     self = copy.deepcopy(other)

    def __add__(self, other):
        rowPre = len(self.mat)
        rowPost = len(other.mat)
        c = Matrix()
        if rowPre == rowPost:
            colPre = len(self.mat[0])
            colPost = len(other.mat[0])
            if colPre == colPost:
                # print("YES")
                for i in range(rowPre):
                    row = []
                    for j in range(colPre):
                        row.append(self.mat[i][j] + other.mat[i][j])
                    c.mat.append(row)
                c.mat = tuple(c.mat)
                return c
            else:
                raise ValueError('Column order not same...terminating subtraction!')
        else:
            raise ValueError('Addition can be performed only on matrices of same order')

    def __sub__(self, other):
        rowPre = len(self.mat)
        rowPost = len(other.mat)
        c = Matrix()
        if rowPre == rowPost:
            colPre = len(self.mat[0])
            colPost = len(other.mat[0])
            if colPre == colPost:
                # print("YES")
                for i in range(rowPre):
                    row = []
                    for j in range(colPre):
                        row.append(self.mat[i][j] - other.mat[i][j])
                    c.mat.append(row)
                c.mat = tuple(c.mat)
                return c
            else:
                raise ValueError('Column order not same...terminating subtraction!')
        else:
            raise ValueError('Subtraction can be performed only on matrices of same order')

    def __mul__(self, other):
        c = Matrix()
        if len(self.mat[0]) == len(other.mat):
            for i in range(len(self.mat)):
                row = []
                for j in range(len(other.mat[0])):
                    sum1 = 0
                    for k in range(len(other.mat)):
                        sum1 += self.mat[i][k] * other.mat[k][j]
                        # print(i, j, k)
                    row.append(sum1)

                c.mat.append(row)
        c.mat = tuple(c.mat)
        return c

    def is_square(self):
        return len(self.mat) == len(self.mat[0])

    def identity(self):
        if not Matrix.is_square(self):
            raise ValueError('IDENTITY is defined only for SQUARE order!!')
        else:
            c = Matrix()
            for i in range(len(self.mat)):
                row = [0] * len(self.mat)
                row[i] = 1
                c.mat.append(row)
            return c

    def __pow__(self, x):
        if (x == 0):
            return Matrix.identity(self)
        res = Matrix.identity(self)
        # temp = Matrix(self)
        a = self
        # print(a.mat)
        epsilon = 1e-6
        while(x > epsilon):
            if x % 2 == 1:
                res = res * a
            x = int(x/ 2)
            # print(x) 
            a = a* a #problem!!!
            # print("problem")
        return res
    def cof(self, mat, temp, p, q,n):
        i = 0
        j = 0
        # n = len(mat[0])
        for row in range(n):
            for col in range(n):
                if (row != p) & (col != q):
                    temp[i][j] = mat[row][col]
                    j = j+1
                    if j == n - 1:
                        j = 0
                        i += 1
        return temp
    def det(self, mat, n):
        if len(mat) == len(mat[0]):
            # print(n)
            if n == 1:
                return mat[0][0]
            elif n == 2:
                return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
            else:
                determinant = 0
                sign = 1
                temp = [[0] * (n) for i in range(n)]
                for f in range(n):
                    temp = Matrix.cof(self, mat, temp, 0, f,n)
                    # print(temp)
                    determinant = determinant + sign * int(mat[0][f]) * Matrix.det(self, temp,n-1)
                    # print(determinant)
                    sign = -sign
                return determinant
        else:
            raise ValueError('Not a SQUARE matrix')


# r3 = [1, 4, 3]
# r1 = [1, 2, 3]
# r2 = [2, 3, 4]
# r4 = [1, 2, 3]
# r5 = [1, 3, 4]
# r6 = [1, 2, 5]
# # r7 = [1, 2, 6]
# A = Matrix(r1, r2, r3)
# B = Matrix(r4, r5, r6)
# # print(A.mat)
# # print(B.mat)
# try:
#     C = A + B
#     D = A - B
#     E = (A ** 2)*A

#     F = A ** 3
#     print(A.det(A.mat, len(A.mat)))
#     # print(F.det(F.mat, len(F.mat)))
#     print(C.mat)
#     print(D.mat)
#     print(E.mat)
#     print(F.mat)
#     # print(F.mat, len(F.mat))
#     # print(E.mat)
# except ValueError as e:
#     print (e)