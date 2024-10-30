from MVO_optimizer import MVO_optimizer
import benchmarks
import inspect
from time import time


def main():
    functions = sorted(list(
        filter(lambda x: x[0].startswith("F"), inspect.getmembers(
            benchmarks, inspect.isfunction))
    ), key=lambda x: int(x[0][1:]))

    for func in functions:
        func = func[1]
        function_name, lb, up, dim = benchmarks.getFunctionDetails(
            func.__name__)

        start_time = time()
        optimizer = MVO_optimizer(func, dim, lb, up)

        best_solution, best_score = optimizer.optimize()
        time_s = time() - start_time
        print(f'{function_name=}\t{best_score=}\t{time_s=}\n{best_solution=}')


if __name__ == "__main__":
    main()
