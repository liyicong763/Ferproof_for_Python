import sys
import time
import math
import flexible_range
from pybp.flexible_rangeproof import Flexible_RangeProof

from pybp.pederson import PedersonCommitment
from pybp.rangeproof import RangeProof

# if len(sys.argv) != 3:
# print('python main.py <value to prove> <within 2**x range>')
# exit(1)

# value = int(sys.argv[1])
# bitlength = int(sys.argv[2])

file_read = open('test.txt')
file_write = open('result.txt', mode='w')
dataMat = []
labelMat = []
for line in file_read.readlines():
    curLine = line.strip().split(" ")
    floatLine = list(map(int, curLine))  # 这里使用的是map函数直接把数据转化成为int类型
    dataMat.append(floatLine[0:3])
print('dataMat:', dataMat)
for num in dataMat:

    original_value = num[0]
    samllrange = num[1]
    bigrange = num[2]
    file_write.writelines(['value: ', str(original_value), ' [', str(samllrange), '-', str(bigrange), ']'])

    flexible_range_result = flexible_range.range_conversion(original_value, samllrange, bigrange)
    value = flexible_range_result['update_value']
    bitlength = flexible_range_result['bitlength']
    update_bigrange = flexible_range_result['update_bigrange']
    file_write.writelines([' -> update_value：', str(value), ' [0-', str(update_bigrange), ']  '])
    file_write.writelines(['problem_bit: ', str(len(format(original_value, 'b')) + len(format(samllrange, 'b')) + len(format(bigrange, 'b'))), '  '])
    # Now simulating: the serialized proof passed to the validator/receiver;
    # note that it is tacitly assumed that in the expected application (CT
    # or similar), the V value is a pedersen commitment which already exists
    # in the transaction; it's what we're validating *against*, so it's not
    # part of the proof itself. Hence we just pass rp.V into the verify call,
    # for the case of valid rangeproofs.
    fail = False
    if not (0 < value and value < 2 ** bitlength and update_bigrange - value > 0):
        print("Value is NOT in range; The program does not provide proof!")
        fail = True
        # To attempt to forge a rangeproof for a not-in-range value,
        # we'll do the following: make a *valid* proof for the truncated
        # bits of our overflowed value, and then apply a V pedersen commitment
        # to our actual value, which will (should!) fail.
        # Obviously, there are a near-infinite number of ways to create
        # invalid proofs, TODO look into others.
        proofval = value & (2 ** bitlength - 1)
        print("Using truncated bits, value: ", proofval, " to create fake proof.")
    else:
        proofval = value
    prove_time_start = time.time()
    # rp = RangeProof(bitlength)
    rp = Flexible_RangeProof(bitlength)
    rp.generate_proof(proofval, 0, update_bigrange)
    proof = rp.get_proof_dict()

    file_write.writelines(['proof_size: ', str(len(format(proof['t'], 'b')) + len(format(proof['mu'], 'b')) + len(format(proof['tau_x'], 'b'))), 'bit'])
    prove_time_end = time.time()
    # now simulating: the serialized proof passed to the validator/receiver;
    # note that it is tacitly assumed that in the expected application (CT
    # or similar), the V value is a pedersen commitment which already exists
    # in the transaction; it's what we're validating *against*, so it's not
    # part of the proof itself. Hence we just pass rp.V into the verify call,
    # for the case of valid rangeproofs.
    # Note this is a new RangeProof object:
    rp2 = Flexible_RangeProof(bitlength)
    #rp_w = RangeProof(proof['bitlength_w'])
    #print("Now attempting to verify a proof in range: 0 -", 2 ** bitlength)
    verify_time_start = time.time()

    print(proof['Ap'], '\n')
    print(proof['Sp'], '\n')
    print(proof['T1p'], '\n')
    print(proof['T2p'], '\n')
    print(proof['tau_x'], '\n')
    print(proof['mu'], '\n')
    print(proof['t'], '\n')
    print(proof['proof'], '\n')

    if fail:
        # As mentioned in comments above, here create a Pedersen commitment
        # to our actual value, which is out of range, with the same blinding
        # value.
        Varg = PedersonCommitment(value, b=rp.gamma).get_commitment()
    else:
        Varg = rp.V
    if not rp2.verify(
            proof['Ap'],
            proof['Sp'],
            proof['T1p'],
            proof['T2p'],
            proof['tau_x'],
            proof['mu'],
            proof['t'],
            proof['proof'],
            Varg,
            update_bigrange
    ):# and rp_w.verify(
          #  proof['proof_w']['Ap'],
           # proof['proof_w']['Sp'],
           # proof['proof_w']['T1p'],
          #  proof['proof_w']['T2p'],
          #  proof['proof_w']['tau_x'],
           # proof['proof_w']['mu'],
           # proof['proof_w']['t'],
          #  proof['proof_w']['proof'],
          #  Varg,
   # ):
        if not fail:
            print('Rangeproof should have verified but is invalid; bug.')
            file_write.writelines(['result: error!  '])
        else:
            print("Rangeproof failed, as it should because value is not in range.")
            file_write.writelines(['result: refuse!  '])
    else:
        print(sys.getsizeof(Varg), '\n')
        if not fail:
            print('Rangeproof verified correctly, as expected.')
            file_write.writelines(['result: pass!  '])
        else:
            print("Rangeproof succeeded but it should not have, value is not in range; bug.")
            file_write.writelines(['result: error!  '])
    verify_time_end = time.time()
    file_write.writelines(['prove time cost: ', str(prove_time_end - prove_time_start), 's  '])
    file_write.writelines(['verify time cost: ', str(verify_time_end - verify_time_start), 's\n'])
file_read.close()
file_write.close()
