import numpy as np
import os
import pandas as pd

from . import HandlerBase


class ElectrometerBinFileHandler(HandlerBase):
    """Read electrometer *.bin files"""

    def __init__(self, fpath):
        # It's a text config file, which we don't store in the resources yet, parsing for now
        fpath_txt = f'{os.path.splitext(fpath)[0]}.txt'

        with open(fpath_txt, 'r') as fp:
            N = int(fp.readline().split(':')[1])
            Gains = [int(x) for x in fp.readline().split(':')[1].split(',')]
            Offsets = [int(x) for x in fp.readline().split(':')[1].split(',')]
            FAdiv = float(fp.readline().split(':')[1])
            fp.readline()
            Ranges = [int(x) for x in fp.readline().split(':')[1].split(',')]
            FArate = float(fp.readline().split(':')[1])
            # trigger_timestamp = float(fp.readline().split(':')[1].strip().replace(',', '.'))

            def Range(val):
                ranges = {1: 1,
                          2: 10,
                          4: 100,
                          8: 1000,
                          16: 100087}
                try:
                    ret = ranges[val]
                except:
                    raise ValueError(f'The value "val" can be one of {ranges.keys()}')
                return ret
            # 1566332720 366808768 -4197857 11013120 00
            raw_data = np.fromfile(fpath, dtype=np.int32)

            A = []
            B = []
            C = []
            D = []
            T = []
            Ra = Range(Ranges[0])
            Rb = Range(Ranges[1])
            Rc = Range(Ranges[2])
            Rd = Range(Ranges[3])
            # dt = 1.0 / FArate / 1000.0

            num_columns = 6
            raw_data = raw_data.reshape((raw_data.size // num_columns, num_columns))

            derived_data = np.zeros((raw_data.shape[0], raw_data.shape[1] - 1))
            derived_data[:, 0] = raw_data[:, -2] + raw_data[:, -1] * 8.0051232 * 1e-9  # Unix timestamp with nanoseconds
            derived_data[:, 1] = Ra * ((raw_data[:, 0] / FAdiv) - Offsets[0]) / Gains[0]
            derived_data[:, 2] = Rb * ((raw_data[:, 1] / FAdiv) - Offsets[1]) / Gains[1]
            derived_data[:, 3] = Rc * ((raw_data[:, 2] / FAdiv) - Offsets[2]) / Gains[2]
            derived_data[:, 4] = Rd * ((raw_data[:, 3] / FAdiv) - Offsets[3]) / Gains[3]

            # for i in range(0, len(X), 4):
            #     A.append(Ra * ((X[i + 0] / FAdiv) - Offsets[0]) / Gains[0])
            #     B.append(Rb * ((X[i + 1] / FAdiv) - Offsets[1]) / Gains[1])
            #     C.append(Rc * ((X[i + 2] / FAdiv) - Offsets[2]) / Gains[2])
            #     D.append(Rd * ((X[i + 3] / FAdiv) - Offsets[3]) / Gains[3])
            #     T.append(i * dt / 4.0)

        # data = np.vstack((np.array(T) + trigger_timestamp,
        #                   np.array(A),
        #                   np.array(B),
        #                   np.array(C),
        #                   np.array(D))).T

        self.df = pd.DataFrame(data=derived_data, columns=['timestamp', 'i0', 'it', 'ir', 'iff'])
        self.raw_data = raw_data

    def __call__(self):
        return self.df, self.raw_data
