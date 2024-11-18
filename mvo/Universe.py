import numpy as np
from random import uniform


class Universe:
    __f = None
    __dim = None
    __lb = None
    __ub = None

    @classmethod
    def __check_bounds(_, value):
        assert Universe.__dim, "Universes dimension should be specified"
        return value if isinstance(value, list) else [value]*Universe.__dim

    @classmethod
    def set_parameters(_, f=None, dim=None, lb=None, ub=None):
        Universe.__f = f if f else Universe.__f
        Universe.__dim = dim if dim else Universe.__dim
        Universe.__lb = Universe.__check_bounds(lb) if lb else Universe.__lb
        Universe.__ub = Universe.__check_bounds(ub) if ub else Universe.__ub

    def __init__(self):
        assert all((
            Universe.__f,
            Universe.__dim,
            Universe.__lb,
            Universe.__ub
        )), "f, dim, lb, ub must be specified in the Universe class using set_parameters method"

        self.__array = np.array([uniform(Universe.__lb[i], Universe.__ub[i])
                                 for i in range(Universe.__dim)])

    def get_array(self):
        return self.__array

    def get_inflation_rate(self):
        return Universe.__f(self.__array)

    def send(self, at, value):
        self.__array[at] = value


Universe.set_parameters(
    f=(lambda x: np.sum(x**2)),
    dim=2,
    lb=[1, 10],
    ub=[2, 20]
)

u = Universe()
u.send(1, 100)
print(u.get_array())
