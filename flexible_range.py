import sys
import time
import math

from pybp.flexible_rangeproof import Flexible_RangeProof
from pybp.vectors import Vector, to_bitvector, to_powervector, to_merge_vector
from pybp.pederson import PedersonCommitment
from pybp.rangeproof import RangeProof


def range_conversion(value, samllrange, bigrange):
    update_bigrange = bigrange - samllrange
    displacement = samllrange
    update_value = value - displacement
    m_len = len(format(update_value, 'b'))
    b_len = len(format(update_bigrange, 'b'))
    bitlength = m_len + b_len
    if bitlength <= 2:
        bitlength = 2
    elif 2 < bitlength <= 4:
        bitlength = 4
    elif 4 < bitlength <= 8:
        bitlength = 8
    elif 8 < bitlength <= 16:
        bitlength = 16
    elif 16 < bitlength <= 32:
        bitlength = 32
    elif 32 < bitlength <= 64:
        bitlength = 64
    return {
        'bitlength': bitlength,
        'update_value': update_value,
        'update_bigrange': update_bigrange,
        'displacement': displacement
    }


def range_transformation_inner_product(value, samllrange, bigrange, bitlength):
    m_len = len(format(value, 'b'))
    a_len = len(format(samllrange, 'b'))
    b_len = len(format(bigrange, 'b'))
    Complement_position = bitlength - b_len - m_len

    m_bit_list = to_bitvector(value, m_len)
    a_bit_list = to_bitvector(samllrange, a_len)
    b_bit_list = to_bitvector(bigrange, b_len)
    i = 0
    while i < Complement_position:
        m_bit_list.vals.append(0)
        i = i + 1
    h1 = to_merge_vector(b_bit_list, m_bit_list)
    h2 = to_merge_vector(m_bit_list, a_bit_list)
    e11 = to_powervector(2, b_len)
    e12 = to_powervector(2, bitlength - b_len)
    e12.vals = [-i for i in e12]
    e1 = to_merge_vector(e11, e12)
    return {'h1': h1, 'e1': e1, 'bitlength': b_len + m_len}


def constructing_special_yn(y, b_len, bitlength):
    y11 = to_powervector(y, b_len)
    y12 = to_powervector(y, bitlength - b_len)
    y12.vals = [-i for i in y12]
    yn = to_merge_vector(y11, y12)
    return yn


def Generate_evidence_for_w(value):
    bitlength = len(format(value, 'b'))
    if not (0 < value and value < 2 ** bitlength):
        print("Value is NOT in range; we want verification to FAIL.")
        proofval = value & (2 ** bitlength - 1)
    else:
        proofval = value
    if bitlength <= 2:
        bitlength = 2
    elif 2 < bitlength <= 4:
        bitlength = 4
    elif 4 < bitlength <= 8:
        bitlength = 8
    elif 8 < bitlength <= 16:
        bitlength = 16
    elif 16 < bitlength <= 32:
        bitlength = 32
    elif 32 < bitlength <= 64:
        bitlength = 64
    rp = RangeProof(bitlength)
    rp.generate_proof(proofval)
    proof = rp.get_proof_dict()
    return proof, bitlength
