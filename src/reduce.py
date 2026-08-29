def reduce(embeddings, method="umap"):
    if method == "umap":
        from umap import UMAP
        return UMAP(n_components=2).fit_transform(embeddings)
    if method == "tsne":
        from sklearn.manifold import TSNE
        return TSNE(n_components=2).fit_transform(embeddings)
    if method == "pca":
        from sklearn.decomposition import PCA
        return PCA(n_components=2).fit_transform(embeddings)
