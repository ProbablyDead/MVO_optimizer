import math
from random import random
import numpy as np
from sklearn.preprocessing import normalize


class MVO_optimizer:
    def __init__(self,
                 func,
                 dim,
                 lower_bound,
                 upper_bound,
                 N=50,
                 max_time=1000,
                 is_minimization: bool = True,
                 wep_min=0.2,
                 wep_max=1.,
                 p=6,
                 visualization=True
                 ) -> None:
        self.func = func
        self.dim = dim
        self.N = N
        self.is_minimization = is_minimization
        self.max_time = max_time
        self.wep_min = wep_min
        self.wep_max = wep_max
        self.p = p
        self.visualization = visualization

        self.lower_bound = lower_bound \
            if isinstance(lower_bound, list) else [lower_bound]*self.dim

        self.upper_bound = upper_bound \
            if isinstance(upper_bound, list) else [upper_bound]*self.dim

    def __norm(self, array):
        # Reshape and enforce dtype float
        array = np.asarray(array, dtype=float).reshape(1, -1)
        # Normalize and reshape back
        return normalize(array).ravel()

    def __roulette_wheel_selection(self, array):
        cumulative_probabilities = np.cumsum(array)
        idx = np.searchsorted(cumulative_probabilities, random())
        return min(idx, self.N-1)

    def optimize(self):
        universes = np.zeros((self.N, self.dim))
        for i in range(self.dim):
            universes[:, i] = np.random.uniform(
                self.lower_bound[i], self.upper_bound[i], self.N)

        time = 1
        best_universe = [0.]*self.dim
        best_universe_inflation = \
            float("inf") if self.is_minimization else -float("inf")

        rng = range(self.max_time)

        if self.visualization:
            import tqdm
            rng = tqdm.tqdm(rng)

        for time in rng:
            # Wormhole existence probability
            WEP = self.wep_min + time * \
                ((self.wep_max - self.wep_min) / self.max_time)
            # Traveling distance rate
            TDR = 1 - (math.pow(time, 1 / self.p) /
                       math.pow(self.max_time, 1 / self.p))

            # Clip values in universes to bounds
            universes = np.clip(
                universes, self.lower_bound, self.upper_bound)

            inflations = np.apply_along_axis(self.func, 1, universes)
            sorted_indices = np.argsort(inflations)
            if not self.is_minimization:
                sorted_indices = sorted_indices[::-1]
            sorted_universes = universes[sorted_indices]
            sorted_inflations = inflations[sorted_indices]

            if self.is_minimization and sorted_inflations[0] < best_universe_inflation \
                    or not self.is_minimization and sorted_inflations[0] > best_universe_inflation:
                best_universe = np.copy(sorted_universes[0])
                best_universe_inflation = sorted_inflations[0]

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
                        universes[black_hole_index, j] \
                            = sorted_universes[white_hole_index][j]

                    # Exploitation
                    if random() < WEP:
                        rand = ((self.upper_bound[j] -
                                 self.lower_bound[j]) * random()
                                + self.lower_bound[j]) * TDR
                        if random() < 0.5:
                            universes[i, j] = best_universe[j] + rand
                        else:
                            universes[i, j] = best_universe[j] - rand

        return best_universe.tolist(), float(best_universe_inflation)
