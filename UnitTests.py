import unittest
import numpy
from fftconvolve import FFTConvolve

class TestFFTConvolve(unittest.TestCase):

    def test_normalization_calculation(self):
        bitsize = 16
        self.assertEqual(32767.0, ((2**bitsize / 2) - 1))

    def test_numpy_array_shapes(self):
        shapeX = []
        shapeH = []
        shapeX = numpy.array(shapeX)
        shapeH = numpy.array(shapeH)
        complexResult = (numpy.issubdtype(shapeX.dtype, numpy.complexfloating))
        self.assertFalse(complexResult)

    def test_maximum_in_normalization(self):
        a = [4,-3,3,-4,6,3,-3,4,6,-8,0,1,-6]
        a = numpy.array(a)
        if abs(numpy.amax(a)) > abs(numpy.amin(a)): maximum = abs(numpy.amax(a))
        else: maximum = abs(numpy.amin(a))
        self.assertEqual(8, maximum)

if __name__ == '__main__':
    unittest.main()
