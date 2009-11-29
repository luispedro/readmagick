==============
ReadMagick
==============

Read images into python numpy arrays using ImageMagick++.

ImageMagick++ supports many newer file formats that the Python Image
Library does not such as JPEG2000.

Compilation
-----------

::

    python setup.py build
    sudo python setup.py install


Should do the trick. You need the readmagick C++ headers. Under ubuntu, the package is called ``libmagick++-dev``.
