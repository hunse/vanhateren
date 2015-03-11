import numpy as np

from vanhateren import VanHateren


def test_download():
    vh = VanHateren()
    vh.download_image(8)


def test_image_list():
    vh = VanHateren()
    print(vh.image_list())


def test_max():
    vh = VanHateren()
    images = vh.images(vh.image_list())
    print(images.max())


def test_image(plt):
    vh = VanHateren(calibrated=True)
    image = vh.image(1)
    print image.max()
    plt.subplot(211)
    plt.imshow(image, cmap='gray')
    plt.subplot(212)
    plt.hist(image.ravel(), bins=51)


def test_patches(plt):
    r, c = 3, 4
    n = r * c
    shape = (64, 64)

    vh = VanHateren(calibrated=True)
    patches = vh.patches(n, shape, rng=np.random.RandomState(8))

    axes = [plt.subplot(r, c, i+1) for i in range(n)]
    for k, ax in enumerate(axes):
        ax.imshow(patches[k], cmap='gray')
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
