import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA
import umap
import networkx as nx
import argparse

# Load distance matrix
def load_distance_matrix(file_path):
    return np.loadtxt(file_path)

# Reduce dimensionality using MDS
def reduce_dimensionality_mds(distance_matrix, n_components=2):
    mds = MDS(n_components=n_components, dissimilarity="precomputed", random_state=42)
    return mds.fit_transform(distance_matrix)

# Reduce dimensionality using t-SNE
def reduce_dimensionality_tsne(distance_matrix, n_components=2):
    tsne = TSNE(n_components=n_components, metric="precomputed", random_state=42)
    return tsne.fit_transform(distance_matrix)

# Reduce dimensionality using UMAP
def reduce_dimensionality_umap(distance_matrix, n_components=2):
    umap_reducer = umap.UMAP(n_components=n_components, metric="precomputed", random_state=42)
    return umap_reducer.fit_transform(distance_matrix)

# Reduce dimensionality using PCA
def reduce_dimensionality_pca(distance_matrix, n_components=2):
    pca = PCA(n_components=n_components)
    return pca.fit_transform(distance_matrix)

# Reduce dimensionality using Fruchterman-Reingold (graph-based)
def reduce_dimensionality_fruchterman(distance_matrix):
    G = nx.Graph()
    num_points = distance_matrix.shape[0]
    for i in range(num_points):
        for j in range(i + 1, num_points):
            G.add_edge(i, j, weight=1.0 / (distance_matrix[i, j] + 1e-5))
    pos = nx.spring_layout(G, seed=42)
    return np.array([pos[i] for i in range(num_points)])

# Plot the 2D scatterplot
def plot_scatter(data_2d, method_name):
    plt.figure(figsize=(10, 7))
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c='blue', alpha=0.5)
    plt.title(f'2D Scatterplot using {method_name}')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize an all-against-all distance matrix as a 2D scatterplot.")
    parser.add_argument("--matrix", type=str, required=True, help="Path to the all-against-all distance matrix file (txt format). Ensure it is a square matrix.")
    parser.add_argument("--method", type=str, choices=["mds", "tsne", "umap", "pca", "fruchterman"], default="mds", help="Dimensionality reduction method to use: 'mds', 'tsne', 'umap', 'pca', or 'fruchterman'.")

    args = parser.parse_args()
    distance_matrix = load_distance_matrix(args.matrix)

    if args.method == "mds":
        reduced_data = reduce_dimensionality_mds(distance_matrix)
    elif args.method == "tsne":
        reduced_data = reduce_dimensionality_tsne(distance_matrix)
    elif args.method == "umap":
        reduced_data = reduce_dimensionality_umap(distance_matrix)
    elif args.method == "pca":
        reduced_data = reduce_dimensionality_pca(distance_matrix)
    elif args.method == "fruchterman":
        reduced_data = reduce_dimensionality_fruchterman(distance_matrix)

    plot_scatter(reduced_data, args.method.upper())