from . import HandlerBase

import h5py


class ZebraHDF5Handler(HandlerBase):
    HANDLER_NAME = 'ZEBRA_HDF51'

    def __init__(self, resource_fn):
        self._handle = h5py.File(resource_fn, 'r')

    def __call__(self, *, column):
        return self._handle[column][:]
