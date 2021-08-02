from typing import IO
import unittest
from matrix import Matrix, InvalidMatrixOperationException, InvalidMatrixContentException
import numpy as np
#assertRaises unitTest video
class TestMatrix(unittest.TestCase):
    
    def test_corr(self):
        with self.assertRaises(InvalidMatrixContentException):
            A = Matrix([[1,2,3,4], ['paritosh', 2.5, 6.7, 8.9]])

    def test_add(self):
        A = Matrix([[1,2,3,4], [2,3,4,1], [3,2,4,1]])
        B = Matrix([[4,3,2,1], [3,2,1,4], [2,3,1,4]])
        result = A + B                                  
        
        self.assertEqual(result.mat, [[5]*4]*3)  
        with self.assertRaises(InvalidMatrixOperationException):
            C = Matrix([[1,2,3,2.6]])
            C + A

    def test_sub(self):

        A = Matrix([[1,2,3,4], [2,3,4,1], [3,2,4,1,5]])
        B = Matrix([[4,3,2,1], [3,2,1,4], [2,3,1,4,8]])
        
        test = Matrix([[4,3,2,1], [3,2,1,4], [2,3,1,4]])
        result = A - B
        
        self.assertEqual(result.mat, [[-3,-1,1,3,0],[-1,1,3,-3,0],[1,-1,3,-3,-3]])
        with self.assertRaises(InvalidMatrixOperationException):
            test - A
        

    def test_pow(self):
       
        A = Matrix([[1,2,3,4], [2,3,4,1], [3,2,4,1], [2,4,1,3]])
        test = Matrix([[1,2,3,4,6], [2,3,4,1], [3,2,4,1], [2,4,1,3]])
        
        result = A ** 2
        
        m = np.array([[1,2,3,4], [2,3,4,1], [3,2,4,1], [2,4,1,3]])
        expec = np.linalg.matrix_power(m,2).tolist()

        with self.assertRaises(InvalidMatrixOperationException):
            test = test**2
        self.assertEqual(result.mat, expec)
    


    def test_mul(self):
        A = Matrix([[1,2,3], [2,3,4.8], [3,2,4], [2,3,1]])
        B = Matrix([[4,3,2,1], [3,2,1,4], [2,3,1,4]])
        
        test1 = Matrix([[4,3,2], [3,2,1], [2,3,1], [4,3,2]])
        test2 = Matrix([[4,3,2,1], [3,2,1,4], [2,3,1,4], [4,3,2,1]])

        expec = np.matmul([[1,2,3], [2,3,4.8], [3,2,4], [2,3,1]], [[4,3,2,1], [3,2,1,4], [2,3,1,4]])
        expec = expec.tolist()
        result = A*B

        with self.assertRaises(InvalidMatrixOperationException):
            test = test1*test2
            
        self.assertEqual(result.mat, expec)
    
    def test_det(self):
        A = Matrix([[1,2,3], [2,3,4.8], [3,2,4], [2,3,1]])
        B = Matrix([[4,3,2,1], [3,2,1,4], [2,3,1,4]])
        det = np.array([[16, 16, 7, 21], [26.6, 26.4, 11.8, 33.2], [26, 25, 12, 27], [19, 15, 8, 18]])
        deter = int(np.linalg.det(det))
        C = A*B
        self.assertEqual(int(C.det(C.mat)), deter) 
        with self.assertRaises(InvalidMatrixOperationException):
            A.det(A.mat)       

if __name__ =='__main__':
    unittest.main()