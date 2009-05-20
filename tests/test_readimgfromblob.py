import numpy as np
import readmagick

_testimg = 'tests/data/testimage.jp2'
def test_readimgfromblob():
    img0 = readmagick.readimg(_testimg)
    img1 = readmagick.readimgfromblob(file(_testimg).read())
    assert img0.shape == img1.shape
    assert np.all(img0 == img1)

