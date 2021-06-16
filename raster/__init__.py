
try:
    from . import tiff
    print("full tiff support")
except:
    print("no tiff support")

try:
    import hdf5
    print("full hdf5 support")
except:
    print("no hdf5 support")

