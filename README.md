# vanhateren
Work with [Van Hateren's natural image database](
http://cin-11.medizin.uni-tuebingen.de:61280/vanhateren/)

## Example

```python
import vanhateren

# Use the calibrated or uncalibrated dataset
vh = vanhateren.VanHateren(calibrated=True)

# Get the first image (downloads automatically)
image1 = vh.image(1)

# Create 100 64x64 image patches (downloads first 10 images)
patches = vh.patches(100, (64, 64))

# Scale the patches to fall nicely in the range [-1, 1]
patches = vh.preprocess.scale(patches)
```

To explicitly download more images or to download specific images,
use `VanHateren.download_image` or `VanHateren.download_images`:

```python
import vanhateren
vh = vanhateren.VanHateren(calibrated=True)
vh.download_images(range(1, 101))  # download first 100 images
```
