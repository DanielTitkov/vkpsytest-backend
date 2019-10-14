from functools import wraps
from time import time

import logging

def timing(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        logging.warning('called func: {} args:[{}, {}] took: {:2.4f} ms'.format(
            f.__name__,
            "args" or args, 
            "kwargs" or kwargs,
            (te-ts)*1000,
        ))
        return result
    return wrap