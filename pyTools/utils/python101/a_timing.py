import timeit

if __name__ == '__main__':
    tick = timeit.default_timer()
    val = print('Hello World')
    timeDelta = timeit.default_timer() - tick
    print(f'TTime: {timeDelta:.6f} sec')
