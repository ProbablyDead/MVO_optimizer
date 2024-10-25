import math
from random import random
import numpy as np
from sklearn.preprocessing import normalize


class MVO_optimizer:
    def __init__(self,
                 func,
                 universes,
                 max_time=10,
                 lower_bound=None,
                 upper_bound=None,
                 is_minimization: bool = True,
                 wep_min=0.2,
                 wep_max=1.,
                 p=6,
                 ) -> None:
        self.func = func
        self.universes = np.array(universes)
        self.dim = self.universes.ndim
        self.N = len(self.universes)
        self.is_minimization = is_minimization
        self.max_time = max_time
        self.wep_min = wep_min
        self.wep_max = wep_max
        self.p = p

        if not lower_bound:
            self.lower_bound = self.universes.min(axis=0)
        else:
            self.lower_bound = lower_bound \
                if isinstance(lower_bound, list) else [lower_bound]*self.dim

        if not upper_bound:
            self.upper_bound = self.universes.max(axis=0)
        else:
            self.upper_bound = upper_bound \
                if isinstance(upper_bound, list) else [upper_bound]*self.dim

    def __norm(self, array):
        array = array.reshape(1, -1)
        # Enforce dtype float
        if array.dtype != "float":
            array = np.asarray(array, dtype=float)

        # if statement to enforce dtype float
        B = normalize(array)
        B = np.reshape(B, -1)
        return B

    def __roulette_wheel_selection(self, array):
        p = random()
        for i, v in enumerate(array):
            if v > p:
                return i
        return -1

    def optimize(self):
        time = 1
        best_universe = [0.]*self.dim
        best_universe_inflation = float(
            "inf") * 1 if self.is_minimization else -1

        while time <= self.max_time:
            # Wormhole existence probability
            WEP = self.wep_min + time * \
                ((self.wep_max - self.wep_min) / self.max_time)
            # Traveling distance rate
            TDR = 1 - (math.pow(time, 1 / self.p) /
                       math.pow(self.max_time, 1 / self.p))

            # Clip values in universes to bounds
            self.universes = np.clip(
                self.universes, self.lower_bound, self.upper_bound)

            # Sort universes by inflation rates
            sorted_universes = sorted(self.universes, key=self.func)

            sorted_inflations = np.array(
                list(map(self.func, sorted_universes)))

            index = 0 if self.is_minimization else -1

            if self.is_minimization and sorted_inflations[index] < best_universe_inflation \
                    or not self.is_minimization and sorted_inflations[index] > best_universe_inflation:
                best_universe = np.copy(sorted_universes[index])
                best_universe_inflation = sorted_inflations[index]

            normilized_sorted_inflations = np.copy(
                self.__norm(sorted_inflations))

            for i in range(self.N):
                black_hole_index = i
                for j in range(self.dim):
                    r1 = random()
                    # Exploration
                    if r1 < normilized_sorted_inflations[i]:
                        white_hole_index = self.__roulette_wheel_selection(
                            normilized_sorted_inflations)
                        self.universes[black_hole_index, j] \
                            = sorted_universes[white_hole_index][j]

                    # Exploitation
                    if random() < WEP:
                        rand = ((self.upper_bound[j] -
                                 self.lower_bound[j]) * random()
                                + self.lower_bound[j]) * TDR
                        if random() < 0.5:
                            self.universes[i, j] = best_universe[j] + rand
                        else:
                            self.universes[i, j] = best_universe[j] - rand

            time += 1

        return best_universe.tolist(), float(best_universe_inflation)
