from typing import Callable


class Function:
    def __init__(
        self,
        function: Callable[[float], float],
        function_name: str,
        dim: int,
        lower_bounds: float | int | list[float],
        upper_bounds: float | int | list[float],
        is_mininization: bool = True,
        visualisation: str = None,
    ):
        self.function = function
        self.function_name = function_name if function_name \
            else function.__name__
        self.dim = dim
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.is_mininization = is_mininization
        self.visualisation = visualisation

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.function=} {self.function_name=} {self.dim=} {self.lower_bounds=} {self.upper_bounds=} {self.visualisation=}"
