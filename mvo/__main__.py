from MVO_optimizer import MVO_optimizer
import benchmarks


def main():
    func = benchmarks.F5
    function_name, lb, up, dim = benchmarks.getFunctionDetails(func.__name__)

    optimizer = MVO_optimizer(
        func, dim, lb, up)

    best_solution, best_score = optimizer.optimize()
    print('\n'.join([
        f'{function_name=}',
        f'{best_score=}',
        f'{best_solution=}'])
    )


if __name__ == "__main__":
    main()
