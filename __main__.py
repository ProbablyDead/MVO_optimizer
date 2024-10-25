from MVO_optimizer import MVO_optimizer
from benchmarks import func_sqr


def main():
    data = [[5, 6], [3, 4], [1, 1], [7, 8]]

    optimizer = MVO_optimizer(
        func_sqr, data, max_time=1000, is_minimization=False)
    print(optimizer.optimize())


if __name__ == "__main__":
    main()
