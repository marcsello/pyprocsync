from multiprocessing import Process, Queue
import random
import time
import sys
from pyprocsync import ProcSync
import redis

"""
This is a simple script created to test the sole sync precision of PyProcSync.

The sync starts multiple processes on the same machine, since all threads running on the same machine
the system clock is guaranteed to be synchronized across all processes.
The number of processes should be provided trough a command line argument.

This script also requires a redis server running on localhost. The easiest way to start one is to use docker:
docker run -it -p127.0.0.1:6379:6379 redis
"""

REDIS_URL = "redis://localhost:6379/0"


def worker(num_nodes: int, run_id: str, times_queue: Queue):
    procsync = ProcSync(redis.from_url(REDIS_URL), run_id)
    # do random work
    time.sleep(random.randint(1, 10))
    procsync.sync("test", num_nodes)
    times_queue.put(time.time())  # record the time of continue
    procsync.close()


def calc_diffs_in_linear_combination(times):
    result = []
    for i, t1 in enumerate(times):
        for j, t2 in enumerate(times):
            if j != i:
                result.append(abs(t1 - t2))
    return result


def main():
    num_nodes = int(sys.argv[1])
    run_id = "".join(random.choice("abcdefghijklmnopqrstuv") for i in range(15))

    times_queue = Queue(maxsize=num_nodes)
    processes = []
    for i in range(num_nodes):
        p = Process(target=worker, args=(num_nodes, run_id, times_queue))
        processes.append(p)
        p.start()

    times = []
    for i in range(num_nodes):
        times.append(times_queue.get())

    for p in processes:
        p.join()

    # Calculate results
    print("measured continue times:", times)
    diffs_in_lincomb = calc_diffs_in_linear_combination(times)
    worst_diff = max(diffs_in_lincomb)
    print(f"worst diff: {worst_diff:.20f} sec")


if __name__ == '__main__':
    main()
