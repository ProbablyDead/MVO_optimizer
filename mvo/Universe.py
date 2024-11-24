import numpy as np
import math
from random import random


class Universe:
    __f = None
    __dim = None
    __lb = None
    __ub = None
    __p = None
    __wep_min = None
    __wep_max = None
    __max_time = None

    @classmethod
    def __check_bounds(_, value):
        assert Universe.__dim, "Universes dimension should be specified"
        return value if isinstance(value, list) else [value]*Universe.__dim

    @classmethod
    def set_parameters(_,
                       f=None,
                       dim=None,
                       lb=None,
                       ub=None,
                       p=None,
                       wep_min=None,
                       wep_max=None,
                       max_time=None
                       ):
        Universe.__f = f if f else Universe.__f
        Universe.__dim = dim if dim else Universe.__dim
        Universe.__lb = Universe.__check_bounds(
            lb) if lb is not None else Universe.__lb
        Universe.__ub = Universe.__check_bounds(
            ub) if ub is not None else Universe.__ub
        Universe.__p = p if p else Universe.__p
        Universe.__wep_min = wep_min if wep_min else Universe.__wep_min
        Universe.__wep_max = wep_max if wep_max else Universe.__wep_max
        Universe.__max_time = max_time if max_time else Universe.__max_time

    @classmethod
    def get_WEP(_, time):
        return Universe.__wep_min + time * \
            ((Universe.__wep_max - Universe.__wep_min) / Universe.__max_time)

    @classmethod
    def get_TDR(_, time):
        return 1 - (math.pow(time, 1 / Universe.__p) /
                    math.pow(Universe.__max_time, 1 / Universe.__p))

    @classmethod
    def get_random_value(_, j):
        return ((Universe.__ub[j] - Universe.__lb[j]) * random()
                + Universe.__lb[j])

    @classmethod
    def create_empty_universe(_,):
        tmp_ub = Universe.__ub
        tmp_lb = Universe.__lb

        Universe.set_parameters(
            ub=0,
            lb=0,
        )

        u = Universe()

        Universe.set_parameters(
            ub=tmp_ub,
            lb=tmp_lb,
        )

        return u

    def __init__(self):
        assert all(filter(lambda x: x != 0, (
            Universe.__f,
            Universe.__dim,
            Universe.__lb,
            Universe.__ub,
            Universe.__p,
            Universe.__wep_min,
            Universe.__wep_max,
            Universe.__max_time,
        ))), "Parameters must be specified in the Universe class"

        self.__array = np.array([np.random.uniform(
            Universe.__lb[i], Universe.__ub[i])
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
