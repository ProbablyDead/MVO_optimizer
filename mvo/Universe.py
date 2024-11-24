import numpy as np


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
        Universe.__lb = Universe.__check_bounds(
            lb) if lb is not None else Universe.__lb
        Universe.__ub = Universe.__check_bounds(
            ub) if ub is not None else Universe.__ub

    def __init__(self):
        assert all(filter(lambda x: x != 0, (
            Universe.__f,
            Universe.__dim,
            Universe.__lb,
            Universe.__ub
        ))), "f, dim, lb, ub must be specified in the Universe class using set_parameters method"

        self.__array = np.array([np.random.uniform(Universe.__lb[i], Universe.__ub[i])
                                 for i in range(Universe.__dim)])

    def get_array(self):
        return self.__array

    def get_parameter(self, at):
        return self.__array[at]

    def get_inflation_rate(self):
        assert self.__f, "f must be specified"
        return Universe.__f(self.__array)

    def send(self, to, at, delta=0):
        to.receive(at, self.__array[at] + delta)

    def receive(self, at, value):
        self.__array[at] = np.clip(
            value, Universe.__lb[at], Universe.__ub[at])
