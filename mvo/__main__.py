from MVO_optimizer import MVO_optimizer
import benchmarks
import inspect
from time import time


def main():
    functions = sorted(list(
        filter(lambda x: x[0].startswith("F"), inspect.getmembers(
            benchmarks, inspect.isfunction))
    ), key=lambda x: int(x[0][1:]))

    num_of_runs = 30

    for func in functions:
        func = func[1]
        function_name, lb, up, dim = benchmarks.getFunctionDetails(
            func.__name__)

        start_time = time()

        ave_result = 0
        for i in range(num_of_runs):
            optimizer = MVO_optimizer(
                func, dim, lb, up, max_time=750, N=25, visualization=True)

            best_solution, best_score = optimizer.optimize()

            ave_result += best_score

        time_s = (time() - start_time)/num_of_runs
        ave_result /= num_of_runs
        print(f'{function_name=}\t{ave_result=:.6f}\t{time_s=:.2f}')


if __name__ == "__main__":
    main()
