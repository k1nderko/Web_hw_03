from multiprocessing import Process, Manager, Pool
from multiprocessing import cpu_count
from time import time
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def factorize(*number):
    return [division(num) for num in number]

def division(num):
    result = []
    for i in range(1, num + 1):
        if num % i == 0:
            result.append(i)
    return result

if __name__ == '__main__':

    list = [128, 255, 99999, 10651060]

    start_time_2 = time()
    a, b, c, d = factorize(*list)
    time_sync = time() - start_time_2
    logging.info(f'sync: {time_sync}')

    start_time = time()
    with Pool(processes=cpu_count()) as pool:
        a, b, c, d = pool.map(division, list)
    time_async = time() - start_time
    logging.info(f'async: {time_async}')


    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
