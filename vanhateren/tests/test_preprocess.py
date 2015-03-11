import numpy as np

from vanhateren import VanHateren
import vanhateren.preprocess as pp


def load_patches(n, shape=(32, 32)):
    vh = VanHateren(calibrated=True)
    rng = np.random.RandomState(9)
    return vh.patches(n, shape, rng=rng)


def show_patch(ax, patch):
    ax.imshow(patch, cmap='gray')
    ax.set_xticks([])
    ax.set_yticks([])


def hist_patch(ax, patch):
    ax.hist(patch.ravel())
    ax.set_xticks([])
    ax.set_yticks([])


def test_contrast_normalize(plt):
    n = 5
    patches = load_patches(n)
    patches2 = pp.contrast_normalize(patches, beta=10.0)

    r = 2
    axes = [plt.subplot(r, n, i+1) for i in range(r * n)]
    for k in range(n):
        show_patch(axes[k], patches[k])
        show_patch(axes[n+k], patches2[k])
        # hist_patch(axes[n+k], patches[k])
        # show_patch(axes[2*n+k], patches2[k])
        # hist_patch(axes[3*n+k], patches2[k])
    plt.tight_layout()


def test_scale(plt):
    r, c = 2, 10
    patches = load_patches(r * c)
    patches2 = pp.scale(patches)

    rn = 4
    axes = [[plt.subplot2grid((rn*r, c), (rn*i+k, j)) for k in range(rn)]
            for i in range(r) for j in range(c)]
    for k in range(r * c):
        show_patch(axes[k][0], patches[k])
        show_patch(axes[k][1], patches2[k])
        hist_patch(axes[k][2], patches[k])
        hist_patch(axes[k][3], patches2[k])
    plt.tight_layout()


def test_zca(plt):
    r, c = 2, 5
    n = 1000
    patches = load_patches(n)
    patches2 = pp.zca(patches, gamma=1e-0)

    axes0 = [plt.subplot2grid((2*r, c), (2*i, j)) for i in range(r) for j in range(c)]
    axes1 = [plt.subplot2grid((2*r, c), (2*i+1, j)) for i in range(r) for j in range(c)]
    for k in range(r * c):
        show_patch(axes0[k], patches[k])
        show_patch(axes1[k], patches2[k])
    plt.tight_layout()

    # axes = [plt.subplot(r, c, i+1) for i in range(r * c)]
    # for k, ax in enumerate(axes):
    #     show_patch(ax, patches[k])
    # plt.tight_layout()
