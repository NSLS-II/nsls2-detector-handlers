from . import HandlerBase
import h5py

class VideoStreamHDF5Handler(HandlerBase):
    specs = {"VIDEO_STREAM_HDF5"}
    def __init__(self, filename):
        self._name = filename

    def __call__(self, frame):
        with h5py.File(self._name, "r") as f:
            entry = f["/entry/averaged"]
            return entry[frame, :]
