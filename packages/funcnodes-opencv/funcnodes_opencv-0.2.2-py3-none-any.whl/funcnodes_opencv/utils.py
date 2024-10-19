import numpy as np
from .imageformat import OpenCVImageFormat, ImageFormat


def normalize(img: np.ndarray, to_uint8: bool = True):
    img = img.astype(float)
    img -= img.min()
    img /= img.max()
    if to_uint8:
        img *= 255
        img = img.astype(np.uint8)
    return img


def gen_lut():
    """
    Generate a label colormap compatible with opencv lookup table, based on
    Rick Szelski algorithm in `Computer Vision: Algorithms and Applications`,
    appendix C2 `Pseudocolor Generation`.
    :Returns:
      color_lut : opencv compatible color lookup table
    """

    def tobits(x, o):
        return np.array(list(np.binary_repr(x, 24)[o::-3]), np.uint8)

    arr = np.arange(256)
    r = np.concatenate([np.packbits(tobits(x, -3)) for x in arr])
    g = np.concatenate([np.packbits(tobits(x, -2)) for x in arr])
    b = np.concatenate([np.packbits(tobits(x, -1)) for x in arr])
    return np.concatenate([[[b]], [[g]], [[r]]]).T


LUT = gen_lut()


def assert_opencvimg(img) -> OpenCVImageFormat:
    if isinstance(img, OpenCVImageFormat):
        return img
    if isinstance(img, ImageFormat):
        return img.to_cv2()

    if isinstance(img, np.ndarray):
        return OpenCVImageFormat(img)

    raise TypeError("img must be an OpenCVImageFormat, ImageFormat or np.ndarray")
