import pandas as pd

from collections import namedtuple
from . import HandlerBase


class PizzaBoxAnHandlerTxt(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    encoder_row = namedtuple('encoder_row', ['ts_s', 'ts_ns', 'index', 'adc'])
    bases = (10, 10, 10, 16)

    def __init__(self, fpath, chunk_size):
        self.chunk_size = chunk_size
        with open(fpath, 'r') as f:
            self.lines = list(f)

    def __call__(self, chunk_num):
        cs = self.chunk_size
        return [self.encoder_row(*(int(v, base=b) for v, b in zip(ln.split(), self.bases)))
                for ln in self.lines[chunk_num*cs:(chunk_num+1)*cs]]


class PizzaBoxDIHandlerTxt(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    di_row = namedtuple('di_row', ['ts_s', 'ts_ns', 'encoder', 'index', 'di'])

    def __init__(self, fpath, chunk_size):
        self.chunk_size = chunk_size
        with open(fpath, 'r') as f:
            self.lines = list(f)

    def __call__(self, chunk_num):
        cs = self.chunk_size
        return [self.di_row(*(int(v) for v in ln.split()))
                for ln in self.lines[chunk_num*cs:(chunk_num+1)*cs]]


class PizzaBoxEncHandlerTxt(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    encoder_row = namedtuple('encoder_row',
                             ['ts_s', 'ts_ns', 'encoder', 'index', 'state'])

    def __init__(self, fpath, chunk_size):
        self.chunk_size = chunk_size
        with open(fpath, 'r') as f:
            self.lines = list(f)

    def __call__(self, chunk_num):
        cs = self.chunk_size
        return [self.encoder_row(*(int(v) for v in ln.split()))
                for ln in self.lines[chunk_num*cs:(chunk_num+1)*cs]]


# New handlers to support reading files into a Pandas dataframe
class PizzaBoxAnHandlerTxtPD(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    def __init__(self, fpath):
        self.df = pd.read_table(fpath, names=['ts_s', 'ts_ns', 'index', 'adc'], sep=' ')

    def __call__(self):
        return self.df


class PizzaBoxDIHandlerTxtPD(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    def __init__(self, fpath):
        self.df = pd.read_table(fpath, names=['ts_s', 'ts_ns', 'encoder', 'index', 'di'], sep=' ')

    def __call__(self):
        return self.df


class PizzaBoxEncHandlerTxtPD(HandlerBase):
    """Read PizzaBox text files using info from filestore."""

    def __init__(self, fpath):
        self.df = pd.read_table(fpath, names=['ts_s', 'ts_ns', 'encoder', 'index', 'state'], sep=' ')

    def __call__(self):
        return self.df
