import os
import re
import urllib2

import numpy as np


def download(url, filename, verbose=True):
    page = urllib2.urlopen(url)
    data = page.read()
    with open(filename, 'wb+') as f:
        f.write(data)
        if verbose:
            print("Wrote '%s' (%d bytes)" % (filename, len(data)))


class VanHateren(object):

    imshape = (1024, 1536)
    base_url = "http://cin-11.medizin.uni-tuebingen.de:61280/vanhateren/"

    def __init__(self, calibrated=True):
        self.calibrated = calibrated
        vanhateren_dir = os.path.expanduser("~/data/vanhateren/")
        self.image_dir = os.path.join(vanhateren_dir, self.image_ext)

    @property
    def image_ext(self):
        return 'imc' if self.calibrated else 'iml'

    def image_list(self, server=False):
        if server:
            return list(range(1, 4213))

        pattern = 'imk([0-9]{5}).' + self.image_ext
        numbers = []
        for filename in os.listdir(self.image_dir):
            match = re.match(pattern, filename)
            if match is not None:
                numbers.append(int(match.group(1)))

        return sorted(numbers)

    def image_name(self, i):
        pattern = 'imk%05d.' + self.image_ext
        return pattern % i

    def image_url(self, i):
        url = self.base_url + self.image_ext + '/'
        return url + self.image_name(i)

    def image_path(self, i):
        return os.path.join(self.image_dir, self.image_name(i))

    def download_image(self, i, overwrite=False):
        url = self.image_url(i)
        dest = self.image_path(i)
        if overwrite or not os.path.exists(dest):
            try:
                download(url, dest)
            except urllib2.HTTPError as e:
                if e.code == 404:
                    raise ValueError(
                        "Image %d does not exist on the server" % i)
                else:
                    raise

    def download_images(self, inds):
        for i in inds:
            self.download_image(i)

    def image(self, i, normalize=True):
        path = self.image_path(i)
        if not os.path.exists(path):
            self.download_image(i)

        with open(path, 'rb') as handle:
           s = handle.read()

        img = np.fromstring(s, dtype='uint16').byteswap()

        if normalize:
            img = img.astype(float)
            img -= img.min()
            img /= img.max()

        return img.reshape(self.imshape)

    def images(self, inds, **kwargs):
        images = np.zeros((len(inds),) + self.imshape)
        for i, ind in enumerate(inds):
            images[i] = self.image(ind, **kwargs)
        return images

    def patches(self, n, shape, n_images=10, replace=True, rng=np.random):
        inds = rng.choice(self.image_list(), size=n_images, replace=replace)
        images = self.images(inds)

        im_shape = images.shape[1:]
        kk = rng.randint(0, n_images, size=n)
        ii = rng.randint(0, im_shape[0] - shape[0], size=n)
        jj = rng.randint(0, im_shape[1] - shape[1], size=n)

        patches = np.zeros((n,) + shape)
        for p, [k, i, j] in enumerate(zip(kk, ii, jj)):
            patches[p] = images[k, i:i+shape[0], j:j+shape[1]]

        return patches

    # def image(self, i, fullrange=True, log=False):
    #     filename = self.get_filename(i)
    #     with open(filename, 'rb') as handle:
    #        s = handle.read()

    #     img = np.fromstring(s, dtype='uint16').byteswap()

    #     if log:
    #         img = np.log1p(img)
    #     else:
    #         img = img.astype(float)

    #     img -= img.mean()
    #     img /= 6 * img.std()
    #     img += 0.5
    #     img[img < 0] = 0
    #     img[img > 1] = 1
    #     return img.reshape(self.imshape)

    #     if fullrange:  # ensure range of this image is [0, 1]
    #         immax = float(img.max())
    #         img = img / immax
    #         # immin = float(img.min())
    #         # img = (img - immin) / (immax - immin)
    #     else:
    #         img = (img / 6282.0).clip(0,1)

    #     img = img.reshape(self.imshape)
    #     return img


def test_image_list():
    vh = VanHateren()
    print(vh.image_list())


def test_image():
    import matplotlib.pyplot as plt
    vh = VanHateren()

    i = 16
    image0 = vh.image(i, log=False)
    image1 = vh.image(i, log=True)

    axs = [plt.subplot(2, 2, i+1) for i in range(4)]
    axs[0].imshow(image0, cmap='gray')
    axs[1].hist(image0.ravel(), bins=100)
    axs[2].imshow(image1, cmap='gray')
    axs[3].hist(image1.ravel(), bins=100)
    plt.show()


if __name__ == '__main__':
    test_image()
