def apply_to_all(map_fn, s):
    return [map_fn(x) for x in s]

def keep_if(filter_fn, s):
    return [x for x in s if filter_fn(x)]

def reduce(reduce_fn, s, initial):
    reduced = initial
    for x in s:
        reduced = reduce_fn(reduced, x)
    return reduced

# Q6
def deep_len(lst):
    """Returns the deep length of the list.

    >>> deep_len([1, 2, 3])     # normal list
    3
    >>> x = [1, [2, 3], 4]      # deep list
    >>> deep_len(x)
    4
    >>> x = [[1, [1, 1]], 1, [1, 1]] # deep list
    >>> deep_len(x)
    6
    """
    "*** YOUR CODE HERE ***"
    if type(lst)!=list:
        return 1
    else:
        s=[deep_len(b) for b in lst]
        return sum(s)

# Q7
def merge(lst1, lst2):
    """Merges two sorted lists recursively.

    >>> merge([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> merge([], [2, 4, 6])
    [2, 4, 6]
    >>> merge([1, 2, 3], [])
    [1, 2, 3]
    >>> merge([5, 7], [2, 4, 6])
    [2, 4, 5, 6, 7]
    """
    "*** YOUR CODE HERE ***"
    l1,l2=len(lst1),len(lst2)
    s=[]
    i,j=0,0
    while (i<l1) and (j<l2):
        if lst1[i]<=lst2[j]:
            s=s+[lst1[i]]
            i+=1
        else:
            s=s+[lst2[j]]
            j+=1
    if i<l1:
        s=s+lst1[i:]
    if j<l2:
        s=s+lst2[j:]
    return s

# Q11
def coords(fn, seq, lower, upper):
    """
    >>> seq = [-4, -2, 0, 1, 3]
    >>> fn = lambda x: x**2
    >>> coords(fn, seq, 1, 9)
    [[-2, 4], [1, 1], [3, 9]]
    """ 
    "*** YOUR CODE HERE ***"
    x=keep_if(lambda x:(fn(x)>=lower) and (fn(x)<=upper),seq)
    y=apply_to_all(fn,x)
    s=[]
    i=0
    while i<len(x):
        s=s+[[x[i],y[i]]]
        i+=1
    return s

# Q13
def deck():
    "*** YOUR CODE HERE ***"
    i=1
    s=[]
    while i<=4:
        j=1;
        while j<=13:
            if i==1:
                s=s+[['heart',j]]
            elif i==2:
                s=s+[['spade',j]]
            elif i==3:
                s=s+[['diamond',j]]
            else:
                s=s+[['club',j]]
            j+=1
        i+=1
    return s

def sort_deck(deck):
    "*** YOUR CODE HERE ***"
    return sorted(sorted(deck,key=lambda deck:deck[1]),key=lambda deck:deck[0])
