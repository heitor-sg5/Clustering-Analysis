import math
import numpy as np

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.age = 0.0

    def add_child(self, child):
        self.children.append(child)

def pearson_correlation(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    am = a.mean()
    bm = b.mean()
    num = np.sum((a - am) * (b - bm))
    den = math.sqrt(np.sum((a - am) ** 2) * np.sum((b - bm) ** 2))
    if den == 0:
        return 0.0
    return num / den

def pearson_distance(a, b):
    return 1.0 - pearson_correlation(a, b)

def build_distance_matrix(points):
    n = len(points)
    D = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            d = pearson_distance(points[i], points[j])
            D[i, j] = D[j, i] = d
    return D

def hierarchical_clustering(D, n, linkage):
    D = np.array(D, dtype=float)

    clusters = {i: [i] for i in range(n)}
    nodes    = {i: Node(i) for i in range(n)}
    ages     = {i: 0.0     for i in range(n)}
    current_id = n

    def cluster_distance(ci, cj):
        vals = [D[a][b] for a in clusters[ci] for b in clusters[cj]]
        if linkage == "avg":
            return sum(vals) / (len(clusters[ci]) * len(clusters[cj]))
        elif linkage == "max":
            return max(vals)
        else:
            return min(vals)

    while len(clusters) > 1:
        min_dist = float('inf')
        to_merge = None
        cluster_keys = list(clusters.keys())
        for i in range(len(cluster_keys)):
            for j in range(i + 1, len(cluster_keys)):
                ci, cj = cluster_keys[i], cluster_keys[j]
                dist = cluster_distance(ci, cj)
                if dist < min_dist:
                    min_dist = dist
                    to_merge = (ci, cj)

        ci, cj = to_merge
        new_cluster = clusters[ci] + clusters[cj]
        new_node = Node(current_id)
        new_node.add_child(nodes[ci])
        new_node.add_child(nodes[cj])
        new_node.age = min_dist / 2
        nodes[current_id] = new_node
        ages[current_id] = new_node.age

        new_dists = []
        for ck in cluster_keys:
            if ck != ci and ck != cj:
                vals = [D[a][b] for a in new_cluster for b in clusters[ck]]
                if linkage == "avg":
                    dist = sum(vals) / (len(new_cluster) * len(clusters[ck]))
                elif linkage == "max":
                    dist = max(vals)
                else:
                    dist = min(vals)
                new_dists.append((ck, dist))

        clusters.pop(ci)
        clusters.pop(cj)
        clusters[current_id] = new_cluster

        size_before = D.shape[0]
        if current_id >= size_before:
            D = np.pad(D, ((0, 1), (0, 1)), mode='constant', constant_values=0.0)

        for ck, dist in new_dists:
            D[current_id][ck] = dist
            D[ck][current_id] = dist
        current_id += 1

    root_id = list(clusters.keys())[0]
    root = nodes[root_id]

    edges = []
    def collect_edges(node):
        for child in node.children:
            length = node.age - child.age
            edges.append((node.name, child.name, length))
            collect_edges(child)
    collect_edges(root)

    return root, edges

def print_tree(node, indent=0):
    print("  " * indent + str(node.name))
    for child in node.children:
        length = node.age - child.age
        print("  " * (indent + 1) + f"|-- {child.name} (len={length:.4f})")
        print_tree(child, indent + 2)

points = [
    [1.0,  2.0,  3.0,  4.0],
    [1.1,  2.1,  2.9,  4.1],
    [9.0,  8.9,  9.1,  9.2],
    [8.8,  9.2,  9.0,  9.1],
    [4.9,  5.1,  5.0,  5.2]
]

D = build_distance_matrix(points)
root, edges = hierarchical_clustering(D, n=len(points), linkage="avg")
print_tree(root)
