import numpy

cust_matrix = numpy.array([[0.5, 0.3], [0.2, 0.2]])
weight = numpy.array([2, 1])
print numpy.nan_to_num(numpy.multiply(cust_matrix, numpy.array([numpy.array(weight)] * 2)))
