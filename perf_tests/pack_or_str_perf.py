import random
import struct
import time

"""
This simple script measures the performance of the two proposed method of distributing a float value trough Redis.
"""


def main():
    floatlist = [random.random() for _ in range(10 ** 7)]

    time_start = time.time()
    for f in floatlist:
        buf = struct.pack('!d', f)
        f2 = struct.unpack('!d', buf)[0]
    time_finish = time.time()

    print("pack: ", time_finish - time_start)

    time_start = time.time()
    for f in floatlist:
        buf = str(f)
        f2 = float(buf)
    time_finish = time.time()

    print("str: ", time_finish - time_start)


if __name__ == '__main__':
    main()
