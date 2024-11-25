from random import random
import numpy as np
from sklearn.preprocessing import normalize
from copy import deepcopy
from Universe import Universe


class MVO_optimizer:
    def __init__(self,
                 func,
                 dim,
                 lower_bound,
                 upper_bound,
                 N=50,
                 max_time=1000,
                 is_minimization=True,
                 wep_min=0.2,
                 wep_max=1.,
                 p=6,
                 visualization=True
                 ) -> None:
        self.dim = dim
        self.N = N
        self.is_minimization = is_minimization
        self.max_time = max_time
        Universe.set_parameters(
            f=func,
            dim=dim,
            lb=lower_bound,
            ub=upper_bound,
            max_time=max_time,
            wep_min=wep_min,
            wep_max=wep_max,
            p=p,
        )
        self.visualization = visualization

    def __norm(self, array):
        # Reshape and enforce dtype float
        array = np.asarray(array, dtype=float).reshape(1, -1)
        # Normalize and reshape back
        return normalize(array).ravel()

    def __roulette_wheel_selection(self, array):
        cumulative_probabilities = np.cumsum(array/np.sum(array))
        idx = np.searchsorted(cumulative_probabilities, random())
        return min(idx, self.N-1)

    def optimize(self):
        multiverse = [Universe() for _ in range(self.N)]

        best_universe = Universe.create_empty_universe()
        best_universe_inflation = \
            float("inf") if self.is_minimization else -float("inf")

        time = 1

        rng = range(self.max_time + 1)

        if self.visualization:
            import tqdm
            rng = tqdm.tqdm(rng)

        for time in rng:
            WEP = Universe.get_WEP(time)
            TDR = Universe.get_TDR(time)

            inflations = np.array([universe.get_inflation_rate()
                                   for universe in multiverse])

            sorted_indices = np.argsort(inflations)
            if not self.is_minimization:
                sorted_indices = sorted_indices[::-1]
            sorted_universes = [deepcopy(multiverse[i])
                                for i in sorted_indices]
            sorted_inflations = np.copy(inflations[sorted_indices])

            if sorted_inflations[0] < best_universe_inflation \
                if self.is_minimization \
                    else sorted_inflations[0] > best_universe_inflation:

                best_universe = deepcopy(sorted_universes[0])
                best_universe_inflation = sorted_inflations[0]

            normilized_sorted_inflations = np.copy(
                self.__norm(sorted_inflations))

            for i in range(self.N):
                black_hole_index = i
                for j in range(self.dim):
                    # Exploration
                    if random() < normilized_sorted_inflations[i]:
                        white_hole_index = self.__roulette_wheel_selection(
                            normilized_sorted_inflations)

                        sorted_universes[white_hole_index].send(
                            multiverse[black_hole_index], j)
                    # Exploitation
                    if random() < WEP:
                        rand_value = Universe.get_random_value(j) * TDR
                        best_universe.send(multiverse[i], j,
                                           delta=rand_value *
                                           (1 if random() < 0.5 else -1))

        return best_universe.get_array().tolist(), float(best_universe_inflation)
