def filter(func, iterable):
    for x in iterable:
        if func(x):
            return x
