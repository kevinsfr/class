# CS 61A Fall 2014
# Name:Kevin Sheng
# Login:cs61a-fj


def two_equal(a, b, c):
    """Return whether exactly two of the arguments are equal and the
    third is not.

    >>> two_equal(1, 2, 3)
    False
    >>> two_equal(1, 2, 1)
    True
    >>> two_equal(1, 1, 1)
    False
    >>> result = two_equal(5, -1, -1) # return, don't print
    >>> result
    True

    """
    return ((a==b) and (b!=c)) or ((a==c) and (b!=c)) or ((b==c) and (a!=c))


def same_hailstone(a, b):
    """Return whether a and b are both members of the same hailstone
    sequence.

    >>> same_hailstone(10, 16) # 10, 5, 16, 8, 4, 2, 1
    True
    >>> same_hailstone(16, 10) # order doesn't matter
    True
    >>> result = same_hailstone(3, 19) # return, don't print
    >>> result
    False

    """
    n=a
    while (n!=1) and (n!=b):
        if n%2==0:
            n=n//2
        else:
            n=n*3+1
    f=(n==b)
    n=b
    while (n!=1) and (n!=a):
        if n%2==0:
            n=n//2
        else:
            n=n*3+1
    return f or (n==a)

def near_golden(perimeter):
    """Return the integer height of a near-golden rectangle with PERIMETER.

    >>> near_golden(42) # 8 x 13 rectangle has perimeter 42
    8
    >>> near_golden(68) # 13 x 21 rectangle has perimeter 68
    13
    >>> result = near_golden(100) # return, don't print
    >>> result
    19

    """
    h,w=1,perimeter//2-1
    minh=h
    min=abs(w/h-1-h/w)
    while (w!=1):
        w-=1
        h+=1
        x=abs(w/h-1-h/w)
        if (x<min):
            min=x
            minh=h
    return (minh)


