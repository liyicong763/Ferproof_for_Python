import pybitcointools as B

from pybp.types import Scalar
from typing import List, Tuple

from pybp.vectors import Vector


class Floatvector:
    """
    Vector with elements in Z_n, where n is the 'size'
    """

    def __init__(self,
                 v: List[float],
                 size: int = B.N):
        assert isinstance(v, List)
        assert len(v) in [1, 2, 4, 8, 16, 32, 64]
        # for i in v:
            # assert isinstance(i, )

        # Make sure they're in range
        self.vals = [i % size for i in v]
        self.size = size

    def operate(self, f):
        """
        Partial function used for arbitrary operations on self.vals

        Params:
        f: Lambda function
        """
        newV = [f(idx, self.vals[idx]) %
                self.size for idx in range(len(self.vals))]
        return Floatvector(newV, size=self.size)

    def __sub__(self, other):
        assert isinstance(other, Floatvector)
        return self.operate(lambda idx, x: x - other.vals[idx])

    def __add__(self, other):
        assert isinstance(other, Floatvector)
        return self.operate(lambda idx, x: x + other.vals[idx])

    def __mul__(self, other):
        if isinstance(other, Floatvector):
            return self.operate(lambda idx, x: x * other.vals[idx])
        elif isinstance(other, int):
            return self.operate(lambda _, x: x * other)
        return self.operate(lambda _, x: x * other)
        # raise Exception('Invalid multiplication type')

    def __eq__(self, other):
        assert isinstance(other, Floatvector)

        if len(other) is not len(self.vals):
            return False

        for i, j in zip(other.vals, self.vals):
            if i is not j:
                return False

        return True

    def __getitem__(self, key):
        ret = self.vals[key]

        if not isinstance(ret, List):
            return ret

        return Floatvector(ret)

    def __len__(self):
        return len(self.vals)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.vals):
            ret = self.vals[self.n]
            self.n = self.n + 1
            return ret
        raise StopIteration

    def __matmul__(self, other) -> Scalar:
        # assert isinstance(other, Floatvector)
        return sum((self * other)) % self.size

    def __repr__(self):
        return str(self.vals)


def to_bitvector(val: int, bitlength: int, size=B.N) -> Floatvector:
    """
    Returns a Vector with `val` in binary form with specified bitlength,

    E.g. self.vals in VectorBit is an element of [0, 1]
    """
    assert val >= 0

    # Convert to binary string
    # shave off '0b'
    bitstring: str = bin(val)[2:]

    # Right pad bits of '0' until
    # It matches the bitlength
    bits: List[int] = [int(x) for x in bitstring]
    padLength = bitlength - len(bits)
    vals = [0]*padLength + bits

    # Flip it as we wanna read left-to-right
    vals = vals[::-1]

    return Floatvector(vals, size)


def to_powervector(val: int, length: int, size=B.N) -> Floatvector:
    """
    A Vector constructed from powers of scalar, e.g.

    v = y^n = (y^0, y^1, ..., y^(n-1))
    """
    assert isinstance(val, int)

    vals = [pow(val, k, size) for k in range(length)]

    return Floatvector(vals, size)


def to_merge_vector(Vector_A: Floatvector, Vector_B: Floatvector) -> Floatvector:
    """
    合并两个向量
    """
    Vector_C = Floatvector(Vector_A.vals, Vector_A.size)
    for i in Vector_B:
      Vector_C.vals.append(i)
    return Vector_C

def to_divide_vector(Vector_A: Floatvector, Vector_B: Floatvector) -> Floatvector:
    lengths = len(Vector_A.vals)
    Vector_re_list = []
    for i in range(lengths):
        Vector_re_list.append(Vector_A.vals[i] / Vector_B.vals[i])
    Vector_re = Floatvector(Vector_re_list)
    return Vector_re

def to_mul_vector(Vector_A: Vector, c: float) -> Floatvector:
    lengths = len(Vector_A.vals)
    Vector_re_list = []
    for i in range(lengths):
        Vector_re_list.append(Vector_A.vals[i] * c)
    Vector_re = Floatvector(Vector_re_list)
    return Vector_re