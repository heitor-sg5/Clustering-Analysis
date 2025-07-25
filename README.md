# Clustering Analysis

This repository contains implementations of core clustering algorithms for analyzing multidimensional biological data, particularly expression vectors. These methods enable grouping of data points based on similarity or distance, using approaches such as k-centres, Lloyd’s k-means, soft k-means, Cluster Affinity Search Technique (CAST) clustering with Pearson correlation, and UPGMA hierarchical clustering.

---

## 🧬 What are Clusters?

In biology, clusters refer to groups of expression vectors (numerical representations of gene expression levels across different conditions or time points) that exhibit similar patterns. Clustering these vectors helps identify sets of genes that are co-expressed or co-regulated, revealing functional relationships, shared pathways, or common regulatory mechanisms. Computational clustering enables researchers to analyze large-scale expression data efficiently, uncovering biologically meaningful groups that may be too complex to detect manually.

---

## 📁 Files in This Repository

- `k-centres_clustering.py`: Implements k-centres clustering by iteratively selecting the farthest point as a new center, then assigning points to nearest centers.
- `lloyd_k-means_clustering.py`: Implements k-means clustering with a probabilistic initialization (k-means++), followed by iterative refinement of cluster centers by recalculating the center of gravity to minimize distortion within clusters.
- `soft_k-means_clustering`: Implements soft k-means clustering with a softness parameter beta, allowing probabilistic cluster membership and weighted mean updates.
- `hierarchical_clustering.py`: Implements UPGMA clustering by converting expression vectors into distance a matrix using Pearson's correlation, grouping data points that minimize distance.
- `cast_clustering.py`: Implements CAST clustering, using Pearson's correlation to build a similarity matrix and cluster points by affinity threshold theta, adding/removing points to optimize cluster cohesion.

---

## ⚙️ How to Use

### 1. Prepare Input

The input is an m-dimensional expression vector matrix, consisting of one or more values for each given variable (e.g. gene/protein) at different conditions and/or time points. For example:

points = [[1.0,  2.0,  3.0,  4.0], [1.1,  2.1,  2.9,  4.1], [9.0,  8.9,  9.1,  9.2], [8.8,  9.2,  9.0,  9.1], [4.9,  5.1,  5.0,  5.2],]

### 2. Run the Algorithms

The scripts will output the formed clusters (labeled 1, ..., n) along with the data points assigned to each cluster and their corresponding cluster centers.

For `hierarchical_clustering.py`, instead of clusters, the output is a dendrogram (tree) representing the hierarchical relationships among the data points.

---

#### k-Centres

  bash
```k-centres_clustering.py```

#### Lloyd Algorithm with k-Means++ Initialization 

  bash
```lloyd_k-means_clustering.py```

#### Soft k-Means 

  bash
```soft_k-means_clustering```

#### UPGMA Hierarchical Clustering

  bash
```hierarchical_clustering.py```

#### CAST Algorithm

  bash
```cast_clustering.py```

The variables points (expression vector matrix), k (number of clusters), beta (stiffness parameter), and theta (similarity parameter) are defined at the bottom of each script, but can be changed to your needs. You can also change the linkage criteria (max, min, avg) in `hierarchical_clustering.py`.

---

## 🧠 Algorithm Overviews

### k-Centres

- Selects initial centers by iteratively choosing the point farthest from existing centers.
- Assigns each point to its nearest center forming clusters.
- Does not update centers after initial selection, aiming to minimize maximum cluster radius.
- Time complexity: O(k * n^2)

### Lloyd Algorithm with k-Means++ Initialization  

- Initializes centers probabilistically with k-means++ to improve spread.
- Alternates between assigning points to nearest centers and updating centers as cluster centroids (centers of gravity).
- Iterates until convergence or maximum iterations reached, minimizing total within-cluster variance.
- Time complexity: O(I * k * n * d)

### Soft k-Means

- Initializes centers randomly.
- Performs expectation step computing soft cluster membership probabilities based on distances and stiffness parameter beta.
- Maximization step updates centers as weighted means using membership probabilities (centers of gravity).
- Iterates until convergence, allowing soft assignments to clusters.
- Time complexity: O(I * k * n * d)

### UPGMA Hierarchical Clustering

- Computes pairwise Pearson distance matrix between points.
- Iteratively merges closest clusters based on linkage criteria (avg, max, min).
- Updates distance matrix after each merge and builds a dendrogram with node ages.
- Time complexity: O(n^3)

### CAST Algorithm

- Builds similarity matrix based on Pearson correlation of expression vectors.
- Greedily forms clusters by adding points highly correlated above threshold theta and removing low-affinity points.
- Updates clusters iteratively until stable, centers computed as mean vectors (centers of gravity).
- Time complexity: O(n^2 * d)

---

## 🧪 Example Output

- Clusters:

  Cluster 1: [[8.8, 9.2, 9.0, 9.1]] and centre = (8.8, 9.2, 9.0, 9.1)

  Cluster 2: [[9.0, 8.9, 9.1, 9.2]] and centre = (9.0, 8.9, 9.1, 9.2)

  Cluster 3: [[1.0, 2.0, 3.0, 4.0], [1.1, 2.1, 2.9, 4.1], [4.9, 5.1, 5.0, 5.2]] and centre = (2.3, 3.1, 3.6, 4.4)
  
- Clusters Dendogram:

  8
  |-- 6 (len=0.1629)
    6
      |-- 3 (len=0.0842)
        3
      |-- 4 (len=0.0842)
        4
  |-- 7 (len=0.1456)
    7
      |-- 2 (len=0.1016)
        2
      |-- 5 (len=0.1001)
        5
          |-- 0 (len=0.0015)
            0
          |-- 1 (len=0.0015)
            1

---

## 👤 Author

Heitor Gelain do Nascimento
Email: heitorgelain@outlook.com
GitHub: @heitor-sg5

---

## 📚 References

Bioinformatics Algorithms: An Active Learning Approach (Chapter 8) by
Phillip Compeau & Pavel Pevzner
https://bioinformaticsalgorithms.com
