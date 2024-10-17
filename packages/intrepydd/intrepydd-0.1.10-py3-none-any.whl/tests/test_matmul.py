import intrepydd
from intrepydd.lang import *

def foo(a: Array(float64, 2), b: Array(float64, 2), c: Array(float64, 2)) -> Array(float64, 2):
    return c / (a @ b)


foo1 = intrepydd.compile(foo)

N = 10000
a = np.random.randn(N, N)
b = np.random.randn(N, N)
c = np.random.randn(N, N)
assert np.allclose(foo(a, b, c), foo1(a, b, c))