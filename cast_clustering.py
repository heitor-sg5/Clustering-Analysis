import numpy as np

def euclidean_similarity(a, b, max_dist):
    dist = np.linalg.norm(np.asarray(a) - np.asarray(b))
    return 1 - dist / max_dist if max_dist != 0 else 1.0

def build_similarity_matrix(points):
    points = np.asarray(points, dtype=float)
    n = len(points)
    max_dist = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(points[i] - points[j])
            max_dist = max(max_dist, d)
    R = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            if i == j:
                R[i, j] = 1.0
            else:
                r = euclidean_similarity(points[i], points[j], max_dist)
                R[i, j] = R[j, i] = r
    return R

def mean_point(points):
    p = np.asarray(points, dtype=float)
    return tuple(p.mean(axis=0))

def cast(points, theta):
    n = len(points)
    R = build_similarity_matrix(points)

    def theta_degree(i, nodes):
        return sum(1 for j in nodes if j != i and R[i, j] >= theta)

    def affinity_to_cluster(i, C):
        return np.mean([R[i, j] for j in C]) if C else 0.0

    unassigned = set(range(n))
    clusters = []

    while unassigned:
        degrees = {i: theta_degree(i, unassigned) for i in unassigned}
        seed = max(degrees, key=degrees.get)
        C = {seed}
        changed = True
        while changed:
            changed = False
            best_add = None
            for i in unassigned - C:
                aff = affinity_to_cluster(i, C)
                if aff >= theta:
                    if best_add is None or aff > best_add[0]:
                        best_add = (aff, i)

            if best_add is not None:
                C.add(best_add[1])
                changed = True

            worst_remove = None
            for i in list(C):
                aff = affinity_to_cluster(i, C)
                if aff < theta:
                    if worst_remove is None or aff < worst_remove[0]:
                        worst_remove = (aff, i)

            if worst_remove is not None:
                C.remove(worst_remove[1])
                changed = True

        clusters.append(sorted(C))
        unassigned -= C

    centres = [mean_point([points[i] for i in cl]) for cl in clusters]
    return clusters, centres

points = [
    [1.0,  2.0,  3.0,  4.0],
    [1.1,  2.1,  2.9,  4.1],
    [9.0,  8.9,  9.1,  9.2],
    [8.8,  9.2,  9.0,  9.1],
    [4.9,  5.1,  5.0,  5.2]
]

clusters, centres = cast(points, theta=0.8)
for i, cl in enumerate(clusters):
    print(f"Cluster {i+1}: {[points[i] for i in cl]} and centre = {tuple(round(float(c), 1) for c in centres[i])}")
