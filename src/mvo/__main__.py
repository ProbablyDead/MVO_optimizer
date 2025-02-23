from .MVO_optimizer import MVO_optimizer
from functions import benchmarks
from time import time


def main():
    # import inspect
    # functions = [f for _, f in sorted(list(
    #     filter(lambda x: x[0].startswith("F"), inspect.getmembers(
    #         benchmarks, inspect.isfunction))
    # ), key=lambda x: int(x[0][1:]))]

    functions = [benchmarks.TCSD]
    is_minimization = True

    functions = [benchmarks.AJM]
    is_minimization = False

    num_of_runs = 10
    max_time = 10000
    N = 100
    print(f"{num_of_runs=}\t{max_time=}\t{N=}")

    for func in functions:
        function_name, lb, up, dim = benchmarks.getFunctionDetails(
            func.__name__)

        print(f"{function_name=}")

        start_time = time()

        ave_result = 0
        best_solution = []
        best_score = None
        for i in range(num_of_runs):
            optimizer = MVO_optimizer(
                func, dim, lb, up, max_time=max_time, N=N, visualization=False,
                is_minimization=is_minimization)

            solution, score = optimizer.optimize()

            print(f"{i+1}) {score=}")

            if not best_score or (score < best_score if is_minimization
                                  else score > best_score):
                best_score = score
                best_solution = solution

            ave_result += score

        ave_time_s = (time() - start_time)/num_of_runs
        ave_result /= num_of_runs
        print(f'{ave_result=:.6f}\t{ave_time_s=:.2f}')
        print(f'{best_solution=}: {best_score=}')


if __name__ == "__main__":
    main()
