from functools import singledispatch
import qibo.gate
import numpy as np


__all__ = ["asarray"]


@singledispatch
def asarray(op):
    raise TypeError()


@asarray.register
def asarray_op(op: qibo.gate.Gate, dtype=np.csingle):
    raise NotImplementedError()


@asarray.register
def asarray_i(_: qibo.gate.I, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, 1],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_x(_: qibo.gate.X, dtype=np.csingle):
    return np.array(
        [
            [0, 1],
            [1, 0],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_y(_: qibo.gate.Y, dtype=np.csingle):
    return np.array(
        [
            [0, -1j],
            [1j, 0],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_z(_: qibo.gate.Z, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, -1],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_rz(op: qibo.gate.Rz, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, np.exp(1j * op.theta)],
        ],
        dtype=dtype,
    )
