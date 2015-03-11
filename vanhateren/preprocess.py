"""
Algorithms for whitening.

ZCA combines a technique used in recent papers from Andrew Ng's group at
Stanford, with techniques developed by Nicolas Pinto at MIT.
"""
import numpy as np


def flatten_imageset(images):
    if images.ndim < 2:
        return images.reshape(1, -1)
    else:
        return images.reshape(images.shape[0], -1)


def contrast_normalize(images, remove_mean=True, beta=0.01, hard_beta=True):
    """Normalize each image to have unit standard deviation

    Parameters
    ----------
    images : array_like
        Set of images to be normalized.
    remove_mean : boolean
        Whether to remove the mean of each image.
    beta : float
        Minimum on the normalizing factor.
    hard_beta : boolean
        Whether to use the maximum of
    """
    X = np.array(flatten_imageset(images))
    if remove_mean:
        X -= X.mean(axis=1)[:, None]

    std = X.std(axis=1)
    div = np.maximum(std, beta) if hard_beta else (std + beta)
    X /= div[:, None]
    return X.reshape(images.shape)


def scale(images, **kwargs):
    images = contrast_normalize(images, remove_mean=True, **kwargs)
    images /= 2.5
    return images.clip(-1, 1)


def zca(train, test=None, gamma=1e-5, dtype='float64', **kwargs):
    # -- ZCA whitening (with band-pass)

    # Algorithm from Coates' sc_vq_demo.m
    X = flatten_imageset(train).astype(dtype)
    if X.shape[0] <= 1:
        raise ValueError("Must have more than one image in the training set")

    X = contrast_normalize(X, **kwargs)

    # Remove mean of each feature
    mu = X.mean(axis=0)
    X -= mu[None, :]

    # Whiten across features
    S = np.dot(X.T, X) / (X.shape[0] - 1)
    e, V = np.linalg.eigh(S)
    Sinv = np.dot(np.sqrt(1.0 / (e + gamma)) * V, V.T)
    X = np.dot(X, Sinv)
    X = X.reshape(train.shape)

    if test is None:
        return X
    else:
        assert train.shape[1:] == test.shape[1:]
        Y = test.reshape((test.shape[0], -1)).astype(dtype)
        Y = contrast_normalize(Y, **kwargs)
        Y -= mu[None, :]
        Y = np.dot(Y, Sinv)
        Y = Y.reshape(test.shape)
        return X, Y
