import unittest
from matrix import Matrix
import numpy as np

class TestMatrix(unittest.TestCase):
    
    def test_add(self):
        A = Matrix([1,2,3,4], [2,3,4,1], [3,2,4,1])
        B = Matrix([4,3,2,1], [3,2,1,4], [2,3,1,4])
        result = A + B
        # print(result.mat)
        self.assertEqual(result.mat, tuple([[5]*4]*3))
        # except Exception as e:
        #     print("Wrong answer w.rt. to addition")

    def test_sub(self):

        A = Matrix([1,2,3,4], [2,3,4,1], [3,2,4,1])
        B = Matrix([4,3,2,1], [3,2,1,4], [2,3,1,4])
        result = A - B
        try:
            self.assertEqual(result.mat, ([-3,-1,1,3],[-1,1,3,-3],[1,-1,3,-3]))
        except Exception as e:
            print ("Wrong answer w.rt. to substraction")

    def test_pow(self):
       
        A = Matrix([1,2,3,4], [2,3,4,1], [3,2,4,1], [2,4,1,3])
        result = A ** 2
        m = np.array([[1,2,3,4], [2,3,4,1], [3,2,4,1], [2,4,1,3]])
        expec = np.linalg.matrix_power(m,2).tolist()
        # print(f'{expec}, "\n" {result.mat}')
    
        self.assertEqual(list(result.mat), (expec))
    


    def test_mul(self):
        A = Matrix([1,2,3,4], [2,3,4,1], [3,2,4,1], [2,3,1,4])
        B = Matrix([4,3,2,1], [3,2,1,4], [2,3,1,4], [4,3,2,1])
        expec = np.matmul([[1,2,3,4], [2,3,4,1], [3,2,4,1], [2,3,1,4]], [[4,3,2,1], [3,2,1,4], [2,3,1,4], [4,3,2,1]])
        expec = expec.tolist()
        result = A*B
        try:
            self.assertEqual(result.mat, tuple(expec))
        except Exception as e:
            print("Wrong answer w.rt. to multiplication")

if __name__ =='__main__':
    unittest.main()