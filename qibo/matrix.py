from functools import singledispatch
import qibo.operator
import numpy as np


__all__ = ["asmatrix"]


@singledispatch
def asmatrix(op):
    raise TypeError()


@asmatrix.register
def asmatrix(op: qibo.operator.Operator, dtype=np.csingle):
    raise NotImplementedError()


@asmatrix.register
def asmatrix_i(op: qibo.operator.I, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, 1],
        ],
        dtype=dtype,
    )


@asmatrix.register
def asmatrix_x(op: qibo.operator.X, dtype=np.csingle):
    return np.array(
        [
            [0, 1],
            [1, 0],
        ],
        dtype=dtype,
    )


@asmatrix.register
def asmatrix_y(op: qibo.operator.Y, dtype=np.csingle):
    return np.array(
        [
            [0, -1j],
            [1j, 0],
        ],
        dtype=dtype,
    )


@asmatrix.register
def asmatrix(op: qibo.operator.Z, dtype=np.csingle):
    return np.array(
        [
            [1, 0],
            [0, -1],
        ],
        dtype=dtype,
    )
