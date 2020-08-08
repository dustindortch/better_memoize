# better_memoize

## Overview

[Ujihisa discusses the notion of memoization](https://ujihisa.blogspot.com/2010/11/memoized-recursive-fibonacci-in-python.html).  It is a process for caching the results of recursive functions so previously calculated results are not recalulated.  The example is rather common version of the Fibonacci sequence in Python and explains how to manually implement the capability within the function.  In better_memoize, I iteratively improve on this by implementing the DRY principle.

## Orignal

The code introduces a literal implementation of the Fibonacci sequence:

```python
def fib(n):
    return n if n < 2 else fib(n-2) + fib(n-1)
```

Ujihisa then introduces a cache and returns previously calculated results from the cache:

```python
__fib_cache = {}
def fib(n):
    if n in __fib_cache:
        return __fib_cache[n]
    else:
        __fib_cache[n] = n if n < 2 else fib(n-2) + fib(n-1)
        return __fib_cache[n]
```

Ujihisa's code returns nearly instantaneously for larger results that would have taken minutes to execute, proving the principle.  However, Ujihisa improves the code using decorators so that the original function remains unchanged and clean, and the decorator could be apply to other recursive functions:

```python
def memoize(f):
    cache = {}
    def decorated_function(*args):
        if args in cache:
            return cache[args]
        else:
            cache[args] = f(*args)
            return cache[args]
    return decorated_function

@memoize
def fib(n):
    return n if n < 2 else fib(n-2) + fib(n-1)
```

Again, quite functional with impressive performance and a great example of memoization.  However there is redundancy in the code, and that won't do.

## Improvement

The DRY principle is simple: Don't Repeat Yourself.

Easy enough.  So how do we do it?  The improvements can be made to both examples of memoization.  Simple remove redunant code and have a simple flow of execution.

What is redundant?  Well, in the conditional operations, there is an `if` and an `else`.  Sometimes there are great reasons for this logic, but in this case each condition performs the same final operation, `return cache[args]`.  So, regardless, the code performs this operation, this means we should just always do that.  But how do we work out the condition?  Instead of checking if the value is in the cache, we check if it is NOT in the cache.  If it is NOT in the cache, we place it in the cache.  Regardless of that, we always return from the cache:

```python
def memoize(f):
    cache = {}
    def decorated_function(*args):
        if not args in cache:
            cache[args] = f(*args)
        return cache[args]
    return decorated_function

@memoize
def fib(n):
    return n if n < 2 else fib(n-2) + fib(n-1)
```

The difference is subtle, but it is simple.  It saves two lines of code, the `else:` statement and the redunant `return cache[args]`.  The cost is adding 4 characters to the `if` statement, '`not` ', and saving four characters '    ' by taking the `return` out of the condition.  Net 0 additional characters to those lines of code, a better flow of execution, two fewer liens of code, and the implementation of a good principle.

## Testing

Use the `fib()` function without any of the memoization and run it for 3, 5, and 100:

```python
[fib(x) for x in [3, 5, 100]]
```

Then, run it again, with the same numbers.  Each run should take several minutes of operation and return: `[2, 5, 354224848179261915075]`

Now, add the memoization and run it again; nearly instantaneous.

Run it again for all numbers 1 - 500:

```python
[fib(x) for x in range(1,501)
```
