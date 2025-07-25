import random
import math

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def k_centres_clustering(data, k):
    centres = [random.choice(data)]
    while len(centres) < k:
        farthest_point = max(data, key=lambda p: min(euclidean(p, c) for c in centres))
        centres.append(farthest_point)
    clusters = {i: [] for i in range(k)}
    for point in data:
        nearest_idx = min(range(k), key=lambda i: euclidean(point, centres[i]))
        clusters[nearest_idx].append(point)
    return centres, clusters

points = [
        [1.0,  2.0,  3.0,  4.0],
        [1.1,  2.1,  2.9,  4.1],
        [9.0,  8.9,  9.1,  9.2],
        [8.8,  9.2,  9.0,  9.1],
        [4.9,  5.1,  5.0,  5.2],
    ]

centres, clusters = k_centres_clustering(points, k=3)
for i, c in enumerate(centres):
    print(f"Cluster {i+1}: {clusters[i]} and centre = {tuple(c for c in centres[i])}")
