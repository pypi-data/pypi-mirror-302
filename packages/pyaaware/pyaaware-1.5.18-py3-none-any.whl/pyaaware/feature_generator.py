from itertools import pairwise

import numpy as np

from .constants import GF_BE
from .constants import MF_BE
from .constants import ML_BE
from .constants import STACKED_BIN_TYPES


class FeatureMode:
    def __init__(self, feature_mode: str):
        if len(feature_mode) < 8:
            raise ValueError("Invalid feature mode")

        self.name = feature_mode
        self.type = feature_mode[0:2]
        self.twin = feature_mode[2]
        self.bands = feature_mode[3:5]
        self.bwin = feature_mode[5]
        self.rctype = feature_mode[6]
        self.rcval = int(feature_mode[7:])

        if self.name != f"{self.type}{self.twin}{self.bands}{self.bwin}{self.rctype}{self.rcval}":
            raise ValueError("Invalid feature mode")

    def __str__(self):
        return f"{self.name:<9}: {self.type}, {self.twin}, {self.bands:<2}, {self.bwin}, {self.rctype}, {self.rcval}"


class FeatureGenerator:
    def __init__(self, feature_mode: str, num_classes: int = 1, truth_mutex: bool = False) -> None:
        self._feature_mode = FeatureMode(feature_mode)
        self._num_classes = num_classes
        self._truth_mutex = truth_mutex

        self._parse_feature_mode()

        self._decimation_count = 0
        self._stride_count = 0
        self._step_count = 0
        self._feature_history = np.zeros((self.stride, self.feature_parameters), dtype=np.float32)
        self._truth_decimation_history = np.zeros((self.decimation, self.num_classes), dtype=np.complex64)
        self._truth_stride_history = np.zeros((self.stride, self.num_classes), dtype=np.complex64)

        self._eof = False
        self._feature = np.empty((self.stride, self.feature_parameters), dtype=np.float32)
        self._truth = np.empty(self.num_classes, dtype=np.complex64)

    def _parse_feature_mode(self) -> None:
        length, overlap = self._get_length_overlap()
        self._twin, ttype = self._get_twin_ttype()

        self._eftransform_length = length
        self._eftransform_overlap = overlap
        self._eftransform_ttype = ttype

        self._ftransform_length = length
        self._ftransform_overlap = overlap
        if self._twin == "hann":
            self._ftransform_ttype = "stft-olsa"
        else:
            self._ftransform_ttype = ttype

        self._itransform_length = length
        self._itransform_overlap = overlap
        self._itransform_ttype = ttype

        if self._feature_mode.type[0] == "y":
            if (self._feature_mode.rctype == "b" and self._feature_mode.rcval > 1) or (
                self._feature_mode.rctype != "b" and self._feature_mode.rcval > 2
            ):
                raise ValueError("Invalid feature mode")
            self._itransform_overlap = self._itransform_length // 2
            self._itransform_ttype = "stft-olsa-hann"

            if self._feature_mode.rctype != "s":
                self._eftransform_overlap = self._eftransform_length // 2
                self._eftransform_ttype = "stft-olsa-hann"

        self._bin_start = 0
        if ttype in ("tdac", "tdac-co"):
            self._bin_end = self._ftransform_length // 2 - 1
        else:
            self._bin_end = self._ftransform_length // 2

        self._bins = self.bin_end - self.bin_start + 1

        self._bwin = self._get_bwin()
        self._decimation, self._stride, self._step = self._get_rate_change()

        self._parse_feature_type(ttype)

    def _get_length_overlap(self) -> tuple[int, int]:
        if self._feature_mode.type in ("cm", "hm", "pm"):
            return 256, 128
        if self._feature_mode.type in ("cn", "hn", "pn"):
            return 256, 64
        if self._feature_mode.type in ("c8", "h8", "p8"):
            return 256, 32
        if self._feature_mode.type in ("cf", "hf", "pf"):
            return 256, 16
        if self._feature_mode.type in ("cq", "hq", "pq"):
            return 320, 160
        if self._feature_mode.type in ("cr", "hr", "pr"):
            return 320, 80
        if self._feature_mode.type in ("cs", "hs", "ps"):
            return 320, 40
        if self._feature_mode.type in ("ct", "ht", "pt"):
            return 400, 200
        if self._feature_mode.type in ("cu", "hu", "pu"):
            return 400, 100
        if self._feature_mode.type in ("cv", "hv", "pv"):
            return 400, 50
        if self._feature_mode.type in ("ce", "he", "pe"):
            return 512, 256
        if self._feature_mode.type in ("cd", "hd", "pd"):
            return 512, 128
        if self._feature_mode.type in ("ca", "ha", "pa"):
            return 512, 64
        if self._feature_mode.type in ("cb", "hb", "pb"):
            return 512, 32
        if self._feature_mode.type in ("cc", "hc", "pc"):
            return 512, 16
        if self._feature_mode.type in ("cj", "hj", "pj"):
            return 1024, 128
        if self._feature_mode.type in ("ck", "hk", "pk"):
            return 1024, 64
        if self._feature_mode.type in ("cl", "hl", "pl"):
            return 1024, 32
        return 256, 64

    def _get_twin_ttype(self) -> tuple[str, str]:
        if self._feature_mode.twin == "r":
            return "none", "stft-olsa-hanns"
        if self._feature_mode.twin == "m":
            return "none", "stft-olsa-hammd"
        if self._feature_mode.twin == "n":
            return "none", "stft-olsa-hannd"
        if self._feature_mode.twin == "h":
            return "hann", "stft-olsa-hann"
        if self._feature_mode.twin == "t":
            return "none", "tdac"
        if self._feature_mode.twin == "o":
            return "none", "tdac-co"

        raise ValueError("Invalid feature mode")

    def _get_bwin(self) -> str:
        if self._feature_mode.bwin == "t":
            return "tri"
        if self._feature_mode.bwin == "r":
            return "rect"
        if self._feature_mode.bwin == "n":
            return "none"

        raise ValueError("Invalid feature mode")

    def _get_rate_change(self) -> tuple[int, int, int]:
        if self._feature_mode.rctype == "d":
            decimation = self._feature_mode.rcval
            stride = 1
            step = 1
            return decimation, stride, step
        if self._feature_mode.rctype == "s":
            decimation = 1
            stride = self._feature_mode.rcval
            step = self._feature_mode.rcval
            return decimation, stride, step
        if self._feature_mode.rctype == "b":
            decimation = 2
            stride = self._feature_mode.rcval
            step = self._feature_mode.rcval
            return decimation, stride, step
        if self._feature_mode.rctype == "v":
            decimation = 1
            stride = self._feature_mode.rcval
            step = self._feature_mode.rcval // 2
            return decimation, stride, step
        if self._feature_mode.rctype == "o":
            decimation = 2
            stride = self._feature_mode.rcval
            step = self._feature_mode.rcval // 2
            return decimation, stride, step
        if self._feature_mode.rctype == "e":
            decimation = 1
            stride = self._feature_mode.rcval
            step = ceil_div(4 * self._feature_mode.rcval, 5)
            return decimation, stride, step
        if self._feature_mode.rctype == "f":
            decimation = 1
            stride = self._feature_mode.rcval
            step = ceil_div(3 * self._feature_mode.rcval, 4)
            return decimation, stride, step
        if self._feature_mode.rctype == "t":
            decimation = 1
            stride = self._feature_mode.rcval
            step = ceil_div(2 * self._feature_mode.rcval, 3)
            return decimation, stride, step

        raise ValueError("Invalid feature mode")

    def _parse_feature_type(self, ttype: str) -> None:
        self._cmptype = "cbrte"

        if self._feature_mode.type == "gf":
            if self._feature_mode.bands in GF_BE:
                self._bandedge = GF_BE[self._feature_mode.bands]
                self._num_bandedges = len(self._bandedge)
            else:
                raise ValueError("Invalid feature mode")
            self._feature_parameters = self._num_bandedges

        elif self._feature_mode.type == "mf":
            if self.feature_mode[2:5] == "cdd":
                self._bandedge = MF_BE
                self._num_bandedges = len(self._bandedge)
                self._twin = "hann"
                self._bwin = "tri"
                self._cmptype = "loge"
                self._decimation = 2
                self._stride = 1
                self._step = 1
                self._feature_parameters = 39
            else:
                raise ValueError("Invalid feature mode")

        elif self._feature_mode.type == "ml":
            self._cmptype = "loge"
            if self._feature_mode.bands in ML_BE:
                self._bandedge = ML_BE[self._feature_mode.bands]
                self._num_bandedges = len(self._bandedge)
            else:
                raise ValueError("Invalid feature mode")
            self._feature_parameters = self._num_bandedges

        elif self._feature_mode.type in ("bc", "yc"):
            self._bandedge = list(range(self.bin_start, self.bin_end + 1))
            self._num_bandedges = len(self._bandedge)
            self._feature_parameters = self._num_bandedges
            if self._bwin != "none":
                raise ValueError("Invalid feature mode")

        elif self._feature_mode.type in ("bl", "yl"):
            self._bandedge = list(range(self.bin_start, self.bin_end + 1))
            self._num_bandedges = len(self._bandedge)
            self._feature_parameters = self._num_bandedges
            self._cmptype = "loge"
            if self._bwin != "none":
                raise ValueError("Invalid feature mode")

        elif self._feature_mode.type in STACKED_BIN_TYPES:
            self._bandedge = list(range(self.bin_start, self.bin_end + 1))
            self._num_bandedges = len(self._bandedge)
            if ttype == "tdac-co":
                self._feature_parameters = self._num_bandedges
            else:
                self._feature_parameters = 2 * self._num_bandedges

            if self._feature_mode.type[0] == "h":
                self._cmptype = "plcd3"
            elif self._feature_mode.type[0] == "p":
                self._cmptype = "plcd3p"
            elif self._feature_mode.type[0] == "c":
                self._cmptype = "none"

            if self._bwin != "none":
                raise ValueError("Invalid feature mode")

        else:
            raise ValueError("Invalid feature mode")

        if self._bandedge[-1] > self.bin_end:
            self._bandedge[-1] = self.bin_end

        if self._bandedge[0] < self.bin_start:
            self._bandedge[0] = self.bin_start

        self._hbandsize = (
            [self._bandedge[0] - self.bin_start]
            + [b - a for a, b in pairwise(self._bandedge)]
            + [self.bin_end - self._bandedge[-1] + 1]
        )

    @property
    def feature_mode(self) -> str:
        return self._feature_mode.name

    @property
    def num_classes(self) -> int:
        return self._num_classes

    @property
    def truth_mutex(self) -> bool:
        return self._truth_mutex

    @property
    def bin_start(self) -> int:
        return self._bin_start

    @property
    def bin_end(self) -> int:
        return self._bin_end

    @property
    def feature_parameters(self) -> int:
        return self._feature_parameters

    @property
    def stride(self) -> int:
        return self._stride

    @property
    def step(self) -> int:
        return self._step

    @property
    def decimation(self) -> int:
        return self._decimation

    @property
    def feature_size(self) -> int:
        return self.ftransform_overlap * self.decimation * self.stride

    @property
    def ftransform_length(self) -> int:
        return self._ftransform_length

    @property
    def ftransform_overlap(self) -> int:
        return self._ftransform_overlap

    @property
    def ftransform_ttype(self) -> str:
        return self._ftransform_ttype

    @property
    def eftransform_length(self) -> int:
        return self._eftransform_length

    @property
    def eftransform_overlap(self) -> int:
        return self._eftransform_overlap

    @property
    def eftransform_ttype(self) -> str:
        return self._eftransform_ttype

    @property
    def itransform_length(self) -> int:
        return self._itransform_length

    @property
    def itransform_overlap(self) -> int:
        return self._itransform_overlap

    @property
    def itransform_ttype(self) -> str:
        return self._itransform_ttype

    def reset(self) -> None:
        self._decimation_count = 0
        self._stride_count = 0
        self._step_count = 0
        self._feature = np.zeros((self.stride, self.feature_parameters), dtype=np.float32)
        self._truth = np.zeros(self.num_classes, dtype=np.complex64)
        self._eof = False
        self._feature_history = np.zeros((self.feature_parameters, 1, self.stride), dtype=np.complex64)
        self._truth_decimation_history = np.zeros((self.num_classes, 1, self.decimation), dtype=np.complex64)
        self._truth_stride_history = np.zeros((self.num_classes, 1, self.stride), dtype=np.complex64)

    def execute_all(self, xf: np.ndarray, truth_in: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
        if xf.ndim != 2:
            raise ValueError("xf must be an 2-dimensional array")

        input_frames, bins = xf.shape

        if bins != self._bins:
            raise ValueError("bins dimension does not match configuration")

        if truth_in is not None:
            if truth_in.ndim != 2:
                raise ValueError("truth_in must be an 2-dimensional array")
            if truth_in.shape != (input_frames, self.num_classes):
                raise ValueError("truth_in shape is not compatible with xf and configuration")

        output_frames = input_frames // (self.step * self.decimation)

        feature = np.empty((output_frames, self.stride, self.feature_parameters), dtype=np.float32)
        truth = np.empty((output_frames, self.num_classes), dtype=np.complex64)

        output_frame = 0
        for input_frame in range(input_frames):
            if truth_in is not None:
                self.execute(xf[input_frame], truth_in[input_frame])
            else:
                self.execute(xf[input_frame])

            if self.eof():
                feature[output_frame] = self.feature()
                truth[output_frame] = self.truth()
                output_frame += 1

        return feature, truth

    def execute(self, xf: np.ndarray, truth_in: np.ndarray | None = None) -> None:
        if xf.ndim != 1:
            raise ValueError("xf must be a 1-dimensional array")

        bins = xf.shape[0]
        if bins != self._bins:
            raise ValueError("bins dimension does not match configuration")

        self._feature = np.zeros((self.stride, self.feature_parameters), dtype=np.float32)
        self._truth = np.zeros(self.num_classes, dtype=np.complex64)
        self._eof = False

        if truth_in is not None:
            if truth_in.ndim != 1:
                raise ValueError("truth_in must be a 1-dimensional array")
            if truth_in.shape[0] != self.num_classes:
                raise ValueError("truth_in shape does not match configuration")

        if truth_in is not None:
            self._truth_decimation_history[self._decimation_count] = truth_in

        if (self._decimation_count + 1) % self.decimation == 0:
            if truth_in is not None:
                self._truth_stride_history[self._stride_count] = np.max(self._truth_decimation_history, axis=0)

            self._feature_history[self._stride_count] = self._compute_feature(xf)

            if (self._step_count + 1) % self.step == 0:
                idx = range(self._stride_count + 1 - self.stride, self._stride_count + 1)
                self._feature = self._feature_history[idx]

                if truth_in is not None:
                    self._truth = np.max(self._truth_stride_history, axis=0)

                    if self.truth_mutex:
                        self._truth[-1] = 1 - np.sum(self._truth[:-1])

                self._eof = True

            self._stride_count = (self._stride_count + 1) % self.stride
            self._step_count = (self._step_count + 1) % self.step

        self._decimation_count = (self._decimation_count + 1) % self.decimation

    def _compute_feature(self, xf: np.ndarray) -> np.ndarray:
        if self._twin == "hann":
            tmp1 = xf / 2
            tmp2 = xf / 4
            xfw = (
                tmp1[: self._bins + 1]
                - np.append(tmp2[1 : self._bins + 1], np.conj(tmp2[self._bins - 2]))
                - np.append(np.conj(tmp2[1]), tmp2[: self._bins - 1])
            )
        elif self._twin == "none":
            xfw = xf
        else:
            raise ValueError("Invalid feature mode")

        if self._bwin == "tri":
            xfhe = np.real(xfw * np.conj(xfw))
            bando = np.zeros(self._num_bandedges, dtype=np.float32)
            for bi in range(self._num_bandedges - 1):
                for bj in range(self._hbandsize[bi + 1]):
                    tweight = bj / self._hbandsize[bi + 1]
                    bdidx = self._bandedge[bi] + bj - self.bin_start
                    bando[bi] = bando[bi] + xfhe[bdidx] * (1 - tweight)
                    bando[bi + 1] = bando[bi + 1] + xfhe[bdidx] * tweight

            if self._hbandsize[-1] > 0:
                for bj in range(self._hbandsize[-1]):
                    tweight = bj / self._hbandsize[-1]
                    bdidx = self._bandedge[-1] + bj - self.bin_start
                    bando[-1] = bando[-1] + xfhe[bdidx] * (1 - tweight)

            if self._hbandsize[0] > 0:
                for bj in range(self._hbandsize[0], 0, -1):
                    tweight = bj / (self._hbandsize[0] + 1)
                    bando[0] = bando[0] + xfhe[bj - 1] * tweight

            if self._bandedge[0] <= self.bin_start:
                bando[0] = bando[0] * 2

            if self._bandedge[-1] >= self.bin_end:
                bando[-1] = bando[-1] * 2

        elif self._bwin == "rect":
            raise ValueError("Invalid feature mode")

        elif self._bwin == "none":
            if self._cmptype in ("none", "plcd3", "plcd3p"):
                bando = xfw
            elif self._cmptype in ("cbrte", "loge"):
                bando = xfw * np.conj(xfw)
            else:
                raise ValueError("Invalid feature mode")

        else:
            raise ValueError("Invalid feature mode")

        if self._cmptype == "cbrte":
            feature = np.cbrt(np.real(bando))
        elif self._cmptype == "loge":
            feature = np.log(np.real(bando) * 2**16 + 2**-46)
        elif self._cmptype == "plcd3":
            cmag = np.power(np.abs(bando), 0.3)
            if self.ftransform_ttype == "tdac-co":
                feature = cmag
            else:
                phase = np.angle(bando)
                feature = np.concatenate((cmag * np.cos(phase), cmag * np.sin(phase)))
        elif self._cmptype == "plcd3p":
            cmag = np.power(np.abs(bando), 0.3)
            if self.ftransform_ttype == "tdac-co":
                feature = cmag
            else:
                phase = np.angle(bando)
                feature = np.concatenate((cmag, phase))
        elif self._cmptype == "none":
            if self.ftransform_ttype == "tdac-co":
                feature = np.real(bando)
            else:
                feature = np.concatenate((np.real(bando), np.imag(bando)))
        else:
            raise ValueError("Invalid feature mode")

        feature.clip(-(2**15), 2**15 - 1, out=feature)
        return feature

    def eof(self) -> bool:
        return self._eof

    def feature(self) -> np.ndarray:
        return self._feature

    def truth(self) -> np.ndarray:
        return self._truth


def ceil_div(a: int, b: int) -> int:
    return -(a // -b)
