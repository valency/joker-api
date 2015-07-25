import numpy
from statsmodels.tools import categorical

if __name__ == "__main__":
    a = numpy.array(['a', 'b', 'c', 'a', 'b', 'c'])
    b = categorical(a, drop=True)
    print a, b
    c = numpy.array([1, 2, 1, 2, 1, 2])
    print c
    d = numpy.column_stack((c, b))
    print d
