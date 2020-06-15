from . import HandlerBase

import h5py


class ZebraHDF5Handler(HandlerBase):
    specs = {'ZEBRA_HDF51', 'SIS_HDF51'}

    def __init__(self, resource_fn):
        self._resource_fn = resource_fn
        self._handle = h5py.File(resource_fn, 'r')

    def __call__(self, *, column):
        return self._handle[column][:]

    def get_file_list(self, datum_kwarg_gen):
        return [self._resource_fn]
