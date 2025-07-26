import random
import math
import numpy as np

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def mean_point(points):
    p = np.asarray(points, dtype=float)
    return tuple(p.mean(axis=0))

def k_means_initializer(data, k):
    centres = random.sample(data, k)
    while len(centres) < k:
        dist_sq = []
        for point in data:
            min_dist = min(euclidean(point, c) for c in centres)
            dist_sq.append(min_dist ** 2)
        total = sum(dist_sq)
        probs = [d / total for d in dist_sq]
        cumulative_probs = []
        cumsum = 0
        for p in probs:
            cumsum += p
            cumulative_probs.append(cumsum)
        r = random.random()
        for i, cp in enumerate(cumulative_probs):
            if r < cp:
                centres.append(data[i])
                break
    return centres

def centres_to_clusters(data, centres):
    clusters = {i: [] for i in range(len(centres))}
    for point in data:
        nearest_idx = min(range(len(centres)), key=lambda i: euclidean(point, centres[i]))
        clusters[nearest_idx].append(point)
    return clusters

def clusters_to_centres(clusters, data):
    new_centres = []
    for i in range(len(clusters)):
        if clusters[i]:
            new_centres.append(mean_point(clusters[i]))
        else:
            new_centres.append(random.choice(data))
    return new_centres

def k_means_clustering(data, k, I=100):
    centres = k_means_initializer(data, k)
    for _ in range(I):
        clusters = centres_to_clusters(data, centres)
        new_centres = clusters_to_centres(clusters, data)
        if all(euclidean(centres[i], new_centres[i]) < 1e-6 for i in range(k)):
            break
        centres = new_centres
    return centres, clusters

points = [
        [1.0,  2.0,  3.0,  4.0],
        [1.1,  2.1,  2.9,  4.1],
        [9.0,  8.9,  9.1,  9.2],
        [8.8,  9.2,  9.0,  9.1],
        [4.9,  5.1,  5.0,  5.2]
    ]

centres, clusters = k_means_clustering(points, 3)
for i, c in enumerate(centres):
    print(f"Cluster {i+1}: {clusters[i]} and centre = {tuple(round(float(c), 1) for c in centres[i])}")
