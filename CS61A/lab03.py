from operator import add
# Q3
def f1():
    """
    >>> f1()
    3
    """
    "*** YOUR CODE HERE ***"
    f1=lambda:3;return f1()

def f2():
    """
    >>> f2()()
    3
    """
    "*** YOUR CODE HERE ***"
    f2=lambda:lambda:3;return f2()


def f3():
    """
    >>> f3()(3)
    3
    """
    "*** YOUR CODE HERE ***"
    f3=lambda:lambda x:x;return f3()

def f4():
    """
    >>> f4()()(3)()
    3
    """
    "*** YOUR CODE HERE ***"
    f4=lambda:lambda:lambda x:lambda:x;return f4()

# Q4
def lambda_curry2(func):
    """
    Returns a Curried version of a two argument function func.
    >>> x = lambda_curry2(add)
    >>> y = x(3)
    >>> y(5)
    8
    """
    "*** YOUR CODE HERE ***"
    return lambda x:lambda y:func(x,y)

# Q6
def sum(n):
    """Computes the sum of all integers between 1 and n, inclusive.
    Assume n is positive.

    >>> sum(1)
    1
    >>> sum(5)  # 1 + 2 + 3 + 4 + 5
    15
    """
    "*** YOUR CODE HERE ***"
    if n==0:
        return 0
    else:
        return n+sum(n-1)

# Q8
def hailstone(n):
    """Print out the hailstone sequence starting at n, and return the
    number of elements in the sequence.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    "*** YOUR CODE HERE ***"
    print(n)
    if n==1:
        return 1
    elif n%2==0:
        return hailstone(n//2)+1
    else:
        return hailstone(n*3+1)+1


