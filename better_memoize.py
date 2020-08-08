def memoize(f):
    cache = {}
    def decorated_function(*args):
        if not args in cache:
            cache[args] = f(*args)
        return cache[args]
    return decorated_function

@memoize
def fib(n):
    return n if n <=1 else fib(n-1) + fib(n-2)