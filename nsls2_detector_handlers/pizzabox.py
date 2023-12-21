from collections import namedtuple

import pandas as pd

from . import HandlerBase


class PizzaBoxAnHandlerTxt(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    encoder_row = namedtuple("encoder_row", ["ts_s", "ts_ns", "index", "adc"])
    bases = (10, 10, 10, 16)

    def __init__(self, fpath, chunk_size):
        self.chunk_size = chunk_size
        self.filename = fpath
        with open(fpath, "r") as f:
            self.lines = list(f)

    def __call__(self, chunk_num):
        cs = self.chunk_size
        return [
            self.encoder_row(*(int(v, base=b) for v, b in zip(ln.split(), self.bases)))
            for ln in self.lines[chunk_num * cs : (chunk_num + 1) * cs]  # noqa E203
        ]

    def get_file_list(self, datum_kwargs_gen):
        return [self.filename]


class PizzaBoxDIHandlerTxt(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    di_row = namedtuple("di_row", ["ts_s", "ts_ns", "encoder", "index", "di"])

    def __init__(self, fpath, chunk_size):
        self.chunk_size = chunk_size
        self.filename = fpath
        with open(fpath, "r") as f:
            self.lines = list(f)

    def __call__(self, chunk_num):
        cs = self.chunk_size
        return [
            self.di_row(*(int(v) for v in ln.split()))
            for ln in self.lines[chunk_num * cs : (chunk_num + 1) * cs]  # noqa E203
        ]

    def get_file_list(self, datum_kwargs_gen):
        return [self.filename]


class PizzaBoxEncHandlerTxt(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    encoder_row = namedtuple(
        "encoder_row", ["ts_s", "ts_ns", "encoder", "index", "state"]
    )

    def __init__(self, fpath, chunk_size):
        self.chunk_size = chunk_size
        self.filename = fpath
        with open(fpath, "r") as f:
            self.lines = list(f)

    def __call__(self, chunk_num):
        cs = self.chunk_size
        return [
            self.encoder_row(*(int(v) for v in ln.split()))
            for ln in self.lines[chunk_num * cs : (chunk_num + 1) * cs]  # noqa E203
        ]

    def get_file_list(self, datum_kwargs_gen):
        return [self.filename]


# New handlers to support reading files into a Pandas dataframe
class PizzaBoxAnHandlerTxtPD(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    def __init__(self, fpath):
        self.df = pd.read_table(fpath, names=["ts_s", "ts_ns", "index", "adc"], sep=" ")
        self.filename = fpath

    def __call__(self):
        return self.df

    def get_file_list(self, datum_kwargs_gen):
        return [self.filename]


class PizzaBoxDIHandlerTxtPD(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    def __init__(self, fpath):
        self.df = pd.read_table(
            fpath, names=["ts_s", "ts_ns", "encoder", "index", "di"], sep=" "
        )
        self.filename = fpath

    def __call__(self):
        return self.df

    def get_file_list(self, datum_kwargs_gen):
        return [self.filename]


class PizzaBoxEncHandlerTxtPD(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    def __init__(self, fpath):
        self.df = pd.read_table(
            fpath, names=["ts_s", "ts_ns", "encoder", "index", "state"], sep=" "
        )
        self.filename = fpath

    def __call__(self):
        return self.df

    def get_file_list(self, datum_kwargs_gen):
        return [self.filename]
