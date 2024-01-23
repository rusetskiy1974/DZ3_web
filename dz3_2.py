from multiprocessing import cpu_count, Pool
from time import perf_counter

numbers = (10651060, 10651060, 10651060, 10651060 )


def factorize(*numbers_):
    result = tuple()

    for number in numbers_:
        factor_volume = []
        div = 1

        while True:
            if div > number:
                break

            if number % div == 0:
                factor_volume.append(div)

            div += 1

        result = result + tuple([factor_volume])

    return result


if __name__ == '__main__':
    
    start_time = perf_counter()
    factorize(*numbers)
    end_time = perf_counter()
    print(f'Work time for synchronous {end_time - start_time: 0.2f} second.')

    start_time = perf_counter()
    with Pool(processes=cpu_count()) as pool:
        pool.map(factorize, numbers)
    end_time = perf_counter()
    print(f'Work time for multiprocessing {end_time - start_time: 0.2f} second.')

