import numpy
import random
import sys
from scipy.sparse import issparse
from scipy.spatial.distance import cdist
from time import time


def kmeans(X, centres, delta=.001, maxiter=10, metric="euclidean", p=2, verbose=0):
    if not issparse(X):
        X = numpy.asanyarray(X)
    centres = centres.todense() if issparse(centres) else centres.copy()
    N, dim = X.shape
    k, cdim = centres.shape
    if dim != cdim:
        raise ValueError("kmeans: X %s and centres %s must have the same number of columns" % (X.shape, centres.shape))
    if verbose:
        print("kmeans: X %s  centres %s  delta=%.2g  maxiter=%d  metric=%s" % (X.shape, centres.shape, delta, maxiter, metric))
    allx = numpy.arange(N)
    prevdist = 0
    jiter = None
    xtoc = None
    distances = None
    for jiter in range(1, maxiter + 1):
        D = cdist_sparse(X, centres, metric=metric, p=p)  # |X| x |centres|
        xtoc = D.argmin(axis=1)  # X -> nearest centre
        distances = D[allx, xtoc]
        avdist = distances.mean()  # median ?
        if verbose >= 2:
            print("kmeans: av |X - nearest centre| = %.4g" % avdist)
        if (1 - delta) * prevdist <= avdist <= prevdist or jiter == maxiter:
            break
        prevdist = avdist
        for jc in range(k):  # (1 pass in C)
            c = numpy.where(xtoc == jc)[0]
            if len(c) > 0:
                centres[jc] = X[c].mean(axis=0)
    if verbose:
        print("kmeans: %d iterations  cluster sizes:" % jiter, numpy.bincount(xtoc))
    return centres, xtoc, distances


def kmeanssample(X, k, nsample=0, **kwargs):
    N, dim = X.shape
    if nsample == 0:
        nsample = max(2 * numpy.sqrt(N), 10 * k)
    Xsample = randomsample(X, int(nsample))
    pass1centres = randomsample(X, int(k))
    samplecentres = kmeans(Xsample, pass1centres, **kwargs)[0]
    return kmeans(X, samplecentres, **kwargs)


def cdist_sparse(X, Y, **kwargs):
    sxy = 2 * issparse(X) + issparse(Y)
    if sxy == 0:
        return cdist(X, Y, **kwargs)
    d = numpy.empty((X.shape[0], Y.shape[0]), numpy.float64)
    if sxy == 2:
        for j, x in enumerate(X):
            d[j] = cdist(x.todense(), Y, **kwargs)[0]
    elif sxy == 1:
        for k, y in enumerate(Y):
            d[:, k] = cdist(X, y.todense(), **kwargs)[0]
    else:
        for j, x in enumerate(X):
            for k, y in enumerate(Y):
                d[j, k] = cdist(x.todense(), y.todense(), **kwargs)[0]
    return d


def randomsample(X, n):
    sampleix = random.sample(xrange(X.shape[0]), int(n))
    return X[sampleix]


def nearestcentres(X, centres, metric="euclidean", p=2):
    D = cdist(X, centres, metric=metric, p=p)  # |X| x |centres|
    return D.argmin(axis=1)


if __name__ == "__main__":
    N = 10000
    dim = 10
    ncluster = 10
    kmsample = 100  # 0: random centres, > 0: kmeanssample
    kmdelta = .001
    kmiter = 10
    metric = "cityblock"  # "chebyshev" = max, "cityblock" L1,  Lqmetric
    seed = 1

    exec ("\n".join(sys.argv[1:]))  # run this.py N= ...
    numpy.set_printoptions(1, threshold=200, edgeitems=5, suppress=True)
    numpy.random.seed(seed)
    random.seed(seed)

    print("N %d  dim %d  ncluster %d  kmsample %d  metric %s" % (N, dim, ncluster, kmsample, metric))
    X = numpy.random.exponential(size=(N, dim))

    t0 = time()
    if kmsample > 0:
        centres, xtoc, dist = kmeanssample(X, ncluster, nsample=kmsample, delta=kmdelta, maxiter=kmiter, metric=metric, verbose=2)
    else:
        randomcentres = randomsample(X, ncluster)
        centres, xtoc, dist = kmeans(X, randomcentres, delta=kmdelta, maxiter=kmiter, metric=metric, verbose=2)
    print("%.0f msec" % ((time() - t0) * 1000))
