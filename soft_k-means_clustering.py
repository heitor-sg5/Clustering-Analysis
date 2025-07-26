import math
import random
import numpy as np

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def mean_point(points, weights):
    points = np.asarray(points, dtype=float)
    weights = np.asarray(weights, dtype=float)
    weighted_mean = np.average(points, axis=0, weights=weights)
    return tuple(weighted_mean)

def soft_k_means(data, k, beta, I=100):
    centres = random.sample(data, k)

    def e_step(data, centres, beta):
        responsibilities = []
        for point in data:
            weights = []
            for c in centres:
                dist = euclidean(point, c)
                weights.append(math.exp(-beta * dist))
            total_weight = sum(weights)
            responsibilities.append([w / total_weight for w in weights])
        return responsibilities

    def m_step(data, responsibilities, k):
        new_centres = []
        for j in range(k):
            weights_j = [resp[j] for resp in responsibilities]
            new_c = mean_point(data, weights_j)
            new_centres.append(new_c)
        return new_centres

    for _ in range(I):
        responsibilities = e_step(data, centres, beta)
        new_centres = m_step(data, responsibilities, k)
        if max(euclidean(centres[i], new_centres[i]) < 1e-6 for i in range(k)):
            break
        centres = new_centres
    clusters = {i: [] for i in range(k)}
    for i, point in enumerate(data):
        assigned = max(range(k), key=lambda j: responsibilities[i][j])
        clusters[assigned].append(point)
    return centres, responsibilities, clusters

points = [
        [1.0,  2.0,  3.0,  4.0],
        [1.1,  2.1,  2.9,  4.1],
        [9.0,  8.9,  9.1,  9.2],
        [8.8,  9.2,  9.0,  9.1],
        [4.9,  5.1,  5.0,  5.2]
    ]

centres, responsibilities, clusters = soft_k_means(points, k=3, beta=1.0)
for i, c in enumerate(centres):
    print(f"Cluster {i+1}: {clusters[i]} and centre = {tuple(round(float(c), 1) for c in centres[i])}")
