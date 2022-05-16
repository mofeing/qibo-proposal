from functools import singledispatch
import qibo.operator
import numpy as np


__all__ = ["asarray"]


@singledispatch
def asarray(op):
    raise TypeError()


@asarray.register
def asarray_op(op: qibo.operator.Operator, dtype=np.csingle):
    raise NotImplementedError()


@asarray.register
def asarray_i(_: qibo.operator.I, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, 1],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_x(_: qibo.operator.X, dtype=np.csingle):
    return np.array(
        [
            [0, 1],
            [1, 0],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_y(_: qibo.operator.Y, dtype=np.csingle):
    return np.array(
        [
            [0, -1j],
            [1j, 0],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_z(_: qibo.operator.Z, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, -1],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_rz(op: qibo.operator.Rz, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, np.exp(1j * op.theta)],
        ],
        dtype=dtype,
    )
