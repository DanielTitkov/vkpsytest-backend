from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        print('func: {} args:[_, _] took: {:2.4f} ms'.format(
            f.__name__,
            (te-ts)*1000
        ))
        return result
    return wrap