import copy

class InvalidMatrixContentException(Exception):
    """Raised when the matrix content is non-numeric"""

    def __init__(self, message="matrix should have numeric elements only!"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class InvalidMatrixOperationException(RuntimeError):
    """Raised when matrix do not satisy the condition for a particula arithmetic operation"""
    
    def __init__(self, operator = "" ,msg="Invalid arithmetic Operation"):
        self.operator = operator
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.operator}': {self.msg}"
    


class Matrix:
    """Custom User-Defined Matrix and some arithmetic Operations on it"""
    def __init__(self, args=[]):   # whole matrix as input
        try:
            for li in args:
                for elem in li:
                    if not (type(elem) == int or type(elem) == float):
                        raise InvalidMatrixContentException
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
        except IndexError:
            self.mat=[]


    def __add__(self, other):
        rowPre = len(self.mat)
        rowPost = len(other.mat)
        c = Matrix()
        if rowPre == rowPost:
            colPre = len(self.mat[0])
            colPost = len(other.mat[0])
            if colPre == colPost:
                for i in range(rowPre):
                    row = []
                    for j in range(colPre):
                        row.append(self.mat[i][j] + other.mat[i][j])
                    c.mat.append(row)
                return c
            else:
                raise InvalidMatrixOperationException('+','Column order not same...terminating addition!') 
        else:
            raise InvalidMatrixOperationException('+','Addition can be performed only on matrices of same order')

    def __sub__(self, other):
        rowPre = len(self.mat)
        rowPost = len(other.mat)
        c = Matrix()
        if rowPre == rowPost:
            colPre = len(self.mat[0])
            colPost = len(other.mat[0])
            if colPre == colPost:
                for i in range(rowPre):
                    row = []
                    for j in range(colPre):
                        row.append(self.mat[i][j] - other.mat[i][j])
                    c.mat.append(row)
                return c
            else:
                raise InvalidMatrixOperationException('-','Column order not same...terminating subtraction!')
        else:
            raise InvalidMatrixOperationException('-','Subtraction can be performed only on matrices of same order')

    def __mul__(self, other):
        c = Matrix()
        if len(self.mat[0]) == len(other.mat):
            for i in range(len(self.mat)):
                row = []
                for j in range(len(other.mat[0])):
                    determ1 = 0
                    for k in range(len(other.mat)):
                        determ1 += self.mat[i][k] * other.mat[k][j]
                    row.append(determ1)

                c.mat.append(row)
            return c
        else:
            raise InvalidMatrixOperationException('*', 'Multiplication can be performed only on matrices of [mn | nk] types')

    def is_square(self):
        return len(self.mat) == len(self.mat[0])

    def identity(self):
        if not Matrix.is_square(self):
            raise InvalidMatrixOperationException(msg='IDENTITY is defined only for SQUARE matrix!!')
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
        a = self
        epsilon = 1e-6
        while(x > epsilon):
            if x % 2 == 1:
                res = res * a
            x = int(x/ 2)
            a = a* a 
        return res

    def cof(self, mat, i, j):
        return [row[: j] + row[j+1:] for row in (mat[: i] + mat[i+1:])]

    def det(self, mat):
        if len(mat) == len(mat[0]):
            n = len(mat)
            if n == 1:
                return mat[0][0]
            elif n == 2:
                return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
            else:
                determ = 0
                for current_column in range(len(mat)):
 
                    sign = (-1) ** (current_column)

                    sub_det = self.det(mat=self.cof(mat=mat, i=0, j=current_column))

                    determ += (sign * mat[0][current_column] * sub_det)
    
                    return determ
        else:
            raise InvalidMatrixOperationException(msg='Not a SQUARE matrix')

