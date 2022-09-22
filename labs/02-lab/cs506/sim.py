def euclidean_dist(x, y):
    res = 0
    for i in range(len(x)):
        res += (x[i] - y[i])**2
    return res**(1/2)

def manhattan_dist(x, y):
    res = 0
    for i in range(len(x)):
        res += abs(x[i] - y[i])
    return res

def jaccard_dist(x, y):
    if len(x) == 0:
        return 1
    res = 0
    for i in range(len(x)):
        if x[i] == y[i]:
            res += 1
    return 1 - (res/len(x))

def cosine_sim(x, y):
    if len(x) == 0:
        return 1
    if len(y) == 0:
        return 1
    dotprod = 0
    magnofx = 0
    magnofy = 0
    for i in range(min(len(x), len(y))):
        dotprod += x[i] * y[i]
        magnofx += x[i] * x[i]
        magnofy += y[i] * y[i]
    magnofx = magnofx ** (0.5)
    magnofy = magnofy ** (0.5)
    if magnofx == 0 or magnofy == 0:
        return 0
    return dotprod / (magnofx * magnofy)

# Feel free to add more
