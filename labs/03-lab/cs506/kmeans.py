from collections import defaultdict
from math import inf
import random
import csv
from numpy.random import choice

def get_centroid(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    print(points)
    centroid = []
    #if type(points[0] == int):
    #    return sum(points)/len(points)
    for dim in points[0]:
        centroid.append(0)
    for point in points:
        for i in range(len(point)):
            centroid[i] += point[i]
    for i in range(len(centroid)):
        centroid[i] /= len(points)
    return centroid
            
            


def get_centroids(dataset, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the centroid for each of the assigned groups.
    Return `k` centroids in a list
    """
    clusters = []
    uniqueclusters = set()
    for assignment in assignments:
        if assignment not in uniqueclusters:
            clusters.append([])
            uniqueclusters.add(assignment)
    for i in range(len(assignments)):
        clusters[assignments[i]].append(dataset[i])
    centroids = []
    for cluster in clusters:
        centroids.append(get_centroid(cluster))
    return centroids
    
    


def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    res = 0
    for i in range(len(a)):
        res += (a[i] - b[i])**2
    return res**(1/2)


def distance_squared(a, b):
    return distance(a,b)**2


def cost_function(clustering):
    cost = 0
    centroids = []
    print('hey whatsup')
    print(clustering)
    for i in range(len(clustering)):
        centroids.append(get_centroid(clustering[i]))
    for i in range(len(clustering)):
        cur_centroid = centroids[i]
        for point in clustering[i]:
            cost += distance(cur_centroid, point)
    return cost
        


def generate_k(dataset, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return_list = []
    unused_indexes = []
    for i in range(len(dataset)):
        unused_indexes.append(i)
    for i in range(k):
        index_of_indextoadd = random.randint(0, len(unused_indexes) - 1)
        indextoadd = unused_indexes[index_of_indextoadd]
        del unused_indexes[index_of_indextoadd]
        return_list.append(dataset[indextoadd])
    return return_list


def pick_number_proportionally(dataset):
    prob_distr = [item/sum(dataset) for item in dataset]
    num = choice(dataset, p=prob_distr)
    for i in range(len(dataset)):
        if dataset[i] == num:
            return i

def generate_k_pp(dataset, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    where points are picked with a probability proportional
    to their distance as per kmeans pp
    """
    unused_indexes = []
    for i in range(len(dataset)):
        unused_indexes.append(i)
    first_center_ind = random.randint(0, len(dataset) - 1)
    first_center = dataset[first_center_ind]
    del unused_indexes[first_center_ind]
    centers = [first_center]
    while k != 1:
        next_potential_centers = []
        for i in unused_indexes:
            next_potential_centers.append(dataset[i])
        distance_for_each_potential = []
        for pot in next_potential_centers:
            min_dist = distance(pot, centers[0])
            for i in range(1, len(centers)):
                min_dist = min(min_dist, distance(pot, centers[i]))
            distance_for_each_potential.append(min_dist**2)
        picked_index = pick_number_proportionally(distance_for_each_potential)
        centers.append(next_potential_centers[picked_index])
        del unused_indexes[picked_index]
        k -= 1
    return centers


def _do_lloyds_algo(dataset, k_points):
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = get_centroids(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering


def k_means(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")
    
    k_points = generate_k(dataset, k)
    return _do_lloyds_algo(dataset, k_points)


def k_means_pp(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")

    k_points = generate_k_pp(dataset, k)
    return _do_lloyds_algo(dataset, k_points)


def clustered_all_points(clustering, dataset):
    points = []
    for assignment in clustering:
        points += clustering[assignment]
    for point in points:
        if point not in dataset:
            return False
    return True
