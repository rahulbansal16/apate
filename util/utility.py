def isTimeEqual(t1, t2, diff):
    if type(t1) == str:
        t1 = int(t1)
    if type(t2) == str:
        t2 = int(t2)
    return abs(t1-t2) <= diff
