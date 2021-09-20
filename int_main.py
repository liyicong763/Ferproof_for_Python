import sys
import time
import math
import flexible_range
from paint import paint
from pybp.Novel_flexible_rangeproof import Novel_flexible_rangeproof
from pybp.flexible_rangeproof import Flexible_RangeProof

from pybp.pederson import PedersonCommitment

# if len(sys.argv) != 3:
# print('python main.py <value to prove> <within 2**x range>')
# exit(1)

# value = int(sys.argv[1])
# bitlength = int(sys.argv[2])
novel_resut = str(time.time())
file_read = open('test2.txt')
file_write = open('result/' + novel_resut + '.txt', mode='w')
dataMat = []
labelMat = []
prove_time = []
verify_time = []
numSquares_t = []

for line in file_read.readlines():
    curLine = line.strip().split(" ")
    floatLine = list(map(int, curLine))  # 这里使用的是map函数直接把数据转化成为int类型
    dataMat.append(floatLine[0:3])

i = 0
for num in dataMat:
    value = num[0]
    samllrange = num[1]
    bigrange = num[2]
    file_write.writelines(['value: ', str(value), ' [', str(samllrange), '-', str(bigrange), ']'])

    file_write.writelines([' -> update_value：', str(value), ' [0-', str(bigrange), ']  '])
    print("problem size:", (len(bin(value)) + len(bin(samllrange)) + len(bin(bigrange))), '\n')
    file_write.writelines(['problem_bit: ', str(len(format(value, 'b')) + len(format(samllrange, 'b')) + len(format(bigrange, 'b'))), '  '])
    # Now simulating: the serialized proof passed to the validator/receiver;
    # note that it is tacitly assumed that in the expected application (CT
    # or similar), the V value is a pedersen commitment which already exists
    # in the transaction; it's what we're validating *against*, so it's not
    # part of the proof itself. Hence we just pass rp.V into the verify call,
    # for the case of valid rangeproofs.
    fail = False
    if not (bigrange - value > 0):
        print("Value is NOT in range; The program does not provide proof!")
        fail = True
        # To attempt to forge a rangeproof for a not-in-range value,
        # we'll do the following: make a *valid* proof for the truncated
        # bits of our overflowed value, and then apply a V pedersen commitment
        # to our actual value, which will (should!) fail.
        # Obviously, there are a near-infinite number of ways to create
        # invalid proofs, TODO look into others.
        proofval = value & (2 ** 4 - 1)
        print("Using truncated bits, value: ", proofval, " to create fake proof.")
    else:
        proofval = value
    prove_time_start = time.time()
    # rp = RangeProof(bitlength)

    # rp = Novel_flexible_rangeproof(2)
    rp = Novel_flexible_rangeproof(2)
    numSquares_time = rp.generate_proof(proofval, samllrange, bigrange)
    proof = rp.get_proof_dict()
    prove_time_end = time.time()

    file_write.writelines(['proof_size: ', str(len(format(proof['t'], 'b')) + len(format(proof['mu'], 'b')) + len(format(proof['tau_x'], 'b'))), 'bit'])
    # now simulating: the serialized proof passed to the validator/receiver;
    # note that it is tacitly assumed that in the expected application (CT
    # or similar), the V value is a pedersen commitment which already exists
    # in the transaction; it's what we're validating *against*, so it's not
    # part of the proof itself. Hence we just pass rp.V into the verify call,
    # for the case of valid rangeproofs.
    # Note this is a new RangeProof object:
    # rp2 = Novel_flexible_rangeproof(rp.bitlength)
    rp2 = Novel_flexible_rangeproof(rp.bitlength)


    temp_proof = len(bin(proof['proof'][0])) / 8 + len(bin(proof['proof'][1])) / 8
    for proofs in proof['proof'][2]:
        temp_proof += len(bin(proofs[0])) / 8 + len(bin(proofs[1])) / 8
    print(len(bin(proof['Ap'][0]))/8 + len(bin(proof['Ap'][1]))/8+
          len(bin(proof['Sp'][0]))/8+len(bin(proof['Sp'][1]))/8+
          len(bin(proof['T1p'][0]))/8+len(bin(proof['T1p'][1]))/8+
          len(bin(proof['T2p'][0]))/8+len(bin(proof['T2p'][1]))/8+
          len(bin(proof['tau_x']))/8+
          len(bin(proof['mu']))/8+
          len(bin(proof['t']))/8+ temp_proof, '\n')

    verify_time_start = time.time()
    # print(sys.getsizeof(proof['Ap'])+sys.getsizeof(proof['Sp'])+sys.getsizeof(proof['T1p'])+sys.getsizeof(proof['T2p'])+sys.getsizeof(proof['tau_x'])+sys.getsizeof(proof['mu'])+sys.getsizeof(proof['t']), '\n')

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
            Varg
    ):

        verify_time_end = time.time()
        if not fail:
            print('Rangeproof should have verified but is invalid; bug.')
            file_write.writelines(['result: error!  '])
        else:
            print("Rangeproof failed, as it should because value is not in range.")
            file_write.writelines(['result: refuse!  '])
    else:
        print(sys.getsizeof(Varg), '\n')
        verify_time_end = time.time()
        if not fail:
            print('Rangeproof verified correctly, as expected.')
            file_write.writelines(['result: pass!  '])
        else:
            print("Rangeproof succeeded but it should not have, value is not in range; bug.")
            file_write.writelines(['result: error!  '])

    file_write.writelines(['prove time cost: ', str((prove_time_end - prove_time_start)*1000), 'ms  '])
    file_write.writelines(['verify time cost: ', str((verify_time_end - verify_time_start)*1000), 'ms  '])
    file_write.writelines(['numSquares time cost: ', str((prove_time_end - prove_time_start - numSquares_time)*1000), 'ms\n'])
    prove_time.append((prove_time_end - prove_time_start)*1000)
    verify_time.append((verify_time_end - verify_time_start)*1000)
    numSquares_t.append(numSquares_time*1000)
    print("finish : ", i)
    i += 1
file_read.close()
file_write.close()
paint(prove_time, verify_time, numSquares_t)
