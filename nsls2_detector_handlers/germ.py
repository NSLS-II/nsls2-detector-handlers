from . import HandlerBase
import h5py
import tifffile

class AreaDetectorTiffHandlerGERM(HandlerBase):
    specs = {"AD_TIFF_GERM"}

    def __init__(self, fpath):
        self._path = os.path.join(fpath, "")

    def __call__(self):
        ret = []
        with tifffile.TiffFile(self._path) as tif:
            ret.append(tif.asarray())
        return np.array(ret)


class AreaDetectorHDF5HandlerGERM(HandlerBase):
    specs = {"AD_HDF5_GERM"}
    def __init__(self, filename):
        self._name = filename

    def __call__(self, frame):
        with h5py.File(self._name, "r") as f:
            entry = f["/entry/data/data"]
            return entry[frame, :]
