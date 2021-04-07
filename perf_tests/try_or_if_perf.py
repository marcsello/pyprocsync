import time

"""
This simple script measures the performance between two proposed methods to check if the sync time is already late.
"""


def sleep_method_1(secs):
    secs2 = secs - 1
    if secs2 >= 0:
        time.sleep(secs2)


def sleep_method_2(secs):
    try:
        time.sleep(secs - 1)
    except ValueError:
        pass


def main():
    for t in [0, 1, 1.001]:
        for method in [sleep_method_1, sleep_method_2]:

            time_start = time.time()
            for i in range(10 ** 7):
                method(t)
            time_finish = time.time()

            print(f"{method.__name__}({t - 1}) = {time_finish - time_start}s")


if __name__ == '__main__':
    main()
