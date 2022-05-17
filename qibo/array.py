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
def asarray_rx(op: qibo.gate.Rx, dtype=np.csingle):
    return np.array(
        [
            [np.cos(op.theta / 2), -1j * np.sin(op.theta / 2)],
            [1j * np.sin(op.theta / 2), np.cos(op.theta / 2)],
        ],
        dtype=dtype,
    )


@asarray.register
def asarray_ry(op: qibo.gate.Rz, dtype=np.csingle):
    return np.array(
        [
            [np.cos(op.theta / 2), -np.sin(op.theta / 2)],
            [np.sin(op.theta / 2), np.cos(op.theta / 2)],
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


@asarray.register
def asarray_h(_: qibo.gate.H, dtype=np.csingle):
    return 1.0 / np.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=dtype)


@asarray.register
def asarray_s(_: qibo.gate.S, dtype=np.csingle):
    return np.array([[1, 0], [0, 1j]], dtype=dtype)


@asarray.register
def asarray_sd(_: qibo.gate.Sd, dtype=np.csingle):
    return np.array([[1, 0], [0, -1j]], dtype=dtype)


@asarray.register
def asarray_t(_: qibo.gate.T, dtype=np.csingle):
    return np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=dtype)


@asarray.register
def asarray_td(_: qibo.gate.Td, dtype=np.csingle):
    return np.array([[1, 0], [0, -np.exp(1j * np.pi / 4)]], dtype=dtype)


@asarray.register
def asarray_swap(_: qibo.gate.Swap, dtype=np.csingle):
    return np.array(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ],
        dtype=dtype,
    ).reshape((2, 2, 2, 2))


@asarray.register
def asarray_iswap(_: qibo.gate.iSwap, dtype=np.csingle):
    return np.array(
        [
            [1, 0, 0, 0],
            [0, 0, 1j, 0],
            [0, 1j, 0, 0],
            [0, 0, 0, 1],
        ],
        dtype=dtype,
    ).reshape((2, 2, 2, 2))


@asarray.register
def asarray_control(op: qibo.gate.Control, dtype=np.csingle):
    assert op.U.shape == (2, 2)

    arr = np.identity(4, dtype=dtype)
    arr[2:3, 2:3] = op.U
    return arr
