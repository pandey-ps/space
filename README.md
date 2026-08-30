visual embeddings of multiples images in a scatter plot.
uses [facebookresearch/dinov2](https://arxiv.org/abs/2212.14936) for embeddings.

the input images are passed through the vision transformer to get semantic feature vectors(and are cached).

the embeddings are projected down to 2d coordinates using umap/tsne/pca. (choice can be done at the webapp as per number of images).

on the very first run, model weights are downloaded and dumped to cache.