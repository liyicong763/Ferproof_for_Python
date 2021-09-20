import os
import hashlib
import time

import pybitcointools as B

from functools import reduce
from typing import List, Union, Dict

from pybp.Lagrangian import numSquares, Gcd, floatGcd, int_numSquares
from pybp.utils import get_blinding_value, get_blinding_vector, getNUMS, modinv, fiat_shamir
from pybp.pederson import PedersonCommitment
from pybp.types import Scalar, Point
from pybp.vectors import Vector, to_bitvector, to_powervector
from pybp.innerproduct import InnerProductCommitment


class Novel_flexible_rangeproof:
    """
    Based on Bulletproof paper: https://eprint.iacr.org/2017/1066.pdf
    """

    def __init__(self, bitlength):
         self.bitlength = bitlength

    def generate_proof(self, m: Scalar, a: int, b: int):
        """
        Given a value, follow the algorithm laid out
        on p.16, 17 (section 4.2) of paper for prover side
        """
        co_di = Gcd(a, b, m)
        print(co_di)
        w = int((b - m) * (m - a) / co_di ** 2)
        #w = (b - m) * (m - a)
        numSquares_start = time.time()
        a1, self.bitlength = int_numSquares(w)

        numSquares_end = time.time()
        a = Vector(a1)
        w1 = a @ a
        fs_state = b''

        # Vector of all 1's or 0's
        # Mainly for readability
        zeros = Vector([0] * self.bitlength)
        ones = Vector([1] * self.bitlength)
        twos = Vector([2] * self.bitlength)
        power_of_twos = to_powervector(2, self.bitlength)


        # Pederson Commitment to fulfill the hiding and binding properties
        # of bulletproof. Binding value is automatically created
        gamma = get_blinding_value()
        pc = PedersonCommitment(w1, b=gamma)

        V: Point = pc.get_commitment()

        alpha: Scalar = get_blinding_value()
        A = InnerProductCommitment(a, a, c=alpha, U=getNUMS(255))
        P_a: Point = A.get_commitment()

        sL = get_blinding_vector(self.bitlength)
        sR = get_blinding_vector(self.bitlength)
        rho = get_blinding_value()

        S = InnerProductCommitment(sL, sR, c=rho, U=getNUMS(255))
        #ps = PedersonCommitment(sL * sR, b=gamma)
        P_s: Point = S.get_commitment()

        fs_state, fs_challanges = fiat_shamir(fs_state, [V, P_a, P_s])
        y: Point = fs_challanges[0]
        z: Point = fs_challanges[1]

        z2 = pow(z, 2, B.N)
        zv = Vector([z] * self.bitlength)
        yn: Vector = to_powervector(y, self.bitlength)

        # Construct l(x) and r(x) coefficients;
        # l[0] = constant term
        # l[1] = linear term
        # same for r(x)

        l: List[Vector] = [
            a * z - yn,
            sL
            #a * yn,
            #sL * yn * yn
        ]
        # yn: Vector = to_powervector(y, self.bitlength)

        # 0th coeff is y^n ⋅ (aR + z ⋅ 1^n) + (z^2 ⋅ 2^n)
        # operators have been overloaded, so all good
        r: List[Vector] = [
            # operator overloading works if vector is first
            a * z + yn,
            sR
            #a * to_divide_vector(ones, yn),
            #sR * to_divide_vector(ones, yn)
        ]

        # Constant term of t(x) = <l(x), r(x)> is the inner product
        # of the constant terms of l(x)and r(x)
        #t0: Scalar = l[0] * r[0] + l[1] * r[0]
        #t2: Scalar = l[1] * r[0]
        #t1: Scalar = l[0] * r[1] + l[1] * r[1]

        t0: Scalar = l[0] @ r[0]
        t2: Scalar = l[1] @ r[1]
        t1: Scalar = (((l[0] + l[1]) @ (r[0] + r[1])) - t0 - t2) % B.N


        tau1 = get_blinding_value()
        T1 = PedersonCommitment(t1, b=tau1)

        tau2 = get_blinding_value()
        T2 = PedersonCommitment(t2, b=tau2)

        fs_state, fs_challanges = fiat_shamir(
            fs_state, [T1.get_commitment(), T2.get_commitment()], nret=1
        )
        x_1: Scalar = fs_challanges[0]
        mu = ((alpha * z) + (rho * x_1)) % B.N
        tau_x = (z2 * gamma + tau1 * x_1 + tau2 * x_1 * x_1) % B.N

        # lx and rx are vetor-value first degree polynomials evaluated at
        # the challenge value x_1
        lx: Vector = l[0] + (l[1] * x_1)
        #lx: Vector = (l[0] * (1 / x_1)) + (l[1] * (1 / x_1))
        rx: Vector = r[0] + (r[1] * x_1)
        #rx: Vector = (r[0] * (x_1)) + (r[1] * (x_1 * x_1))
        t: Scalar = (t0 + t1 * x_1 + t2 * (x_1 * x_1)) % B.N
        #t: Scalar = (t0 + t1 * x_1) % B.N
        assert t == lx @ rx

        # Prover can new send tau_x, mu and t to verifier
        # inner product argument can be verified from this data
        hprime = []
        yinv = modinv(y, B.N)

        for i in range(self.bitlength):
            hprime.append(
                B.multiply(A.H[i], 1 % B.N)
            )

        fs_state, fs_challanges = fiat_shamir(fs_state, [tau_x, mu, t], nret=1)
        uchallenge = fs_challanges[0]
        
        U = B.multiply(B.G, uchallenge)

        # On the prover side, need to construct an inner product argument
        iproof = InnerProductCommitment(lx, rx, U=U, H=hprime)
        proof = iproof.generate_proof()

        ak: Scalar = proof[0]
        bk: Scalar = proof[1]
        lk: List[Point] = proof[2]
        rk: List[Point] = proof[3]

        # At this point we have a valid data set, but here is included a
        # sanity check that the inner product proof we've generated actually verifies
        iproof2 = InnerProductCommitment(ones, twos, H=hprime, U=U)

        assert iproof2.verify_proof(ak, bk, iproof.get_commitment(), lk, rk)

        self.proof = proof
        self.tau_x = tau_x
        self.gamma = gamma
        self.mu = mu
        self.T1 = T1
        self.T2 = T2
        self.A = A
        self.S = S
        self.t = t
        self.V = V
        return numSquares_end - numSquares_start

    def get_proof_dict(self) -> Dict:
        """
        Returns the rangeproof that's been created in dictionary format.
        And all scalars are fixed length 32 bytes, including the (a, b)
        components of the inner pdocut proof. The exception is L, R which are
        arrays of EC points, length log_2(bitlength).

        So total size of proof is 33*4 + 32*3 + (32*2 + 33*2*log_2(bitlength)).
        This agrees with the last sentence of 4.2 in the paper
        """

        return {
            'proof': self.proof,
            't': self.t,
            'mu': self.mu,
            'tau_x': self.tau_x,
            'Ap': self.A.get_commitment(),
            'Sp': self.S.get_commitment(),
            'T1p': self.T1.get_commitment(),
            'T2p': self.T2.get_commitment()
        }

    def verify(self, Ap, Sp, T1p, T2p, tau_x, mu, t, proof, V):
        fs_state = b''
        # Compute challenges to find x, y, z
        fs_state, fs_challenge = fiat_shamir(fs_state, [V, Ap, Sp])
        y: Scalar = fs_challenge[0]
        z: Scalar = fs_challenge[1]
        z2 = pow(z, 2, B.N)
        fs_state, fs_challenge = fiat_shamir(fs_state, [T1p, T2p], nret=1)
        x_1 = fs_challenge[0]
        # Construct verification equation (61)
        power_of_ones = to_powervector(1, self.bitlength)
        power_of_twos = to_powervector(2, self.bitlength)
        yn = to_powervector(y, self.bitlength)

        # k: Scalar = ((yn @ power_of_ones) * (-z2)) % B.N
        # k = (k - (power_of_ones @ power_of_twos) * pow(z, 3, B.N)) % B.N

        gexp: Scalar = (-(yn @ yn)) % B.N

        lhs = PedersonCommitment(t, b=tau_x).get_commitment()

        rhs = B.multiply(B.G, gexp)
        rhs = B.add_pubkeys(rhs, B.multiply(V, z2))
        rhs = B.add_pubkeys(rhs, B.multiply(T1p, x_1))
        rhs = B.add_pubkeys(rhs, B.multiply(T2p, pow(x_1, 2, B.N)))

        if not lhs == rhs:
            print('(61) verification check failed')
            return False
        # HPrime
        hprime = []
        #yinv = modinv(y, B.N)
        for i in range(1, self.bitlength + 1):
            hprime.append(
                B.multiply(getNUMS(self.bitlength + i), 1 % B.N)
            )
        # Reconstruct P
        P = B.add_pubkeys(
            B.multiply(Sp, x_1),
            B.multiply(Ap, z)
        )
        fyn = []
        for i in range(self.bitlength):
            fyn.append(-yn[i])
        # Add g*^(-y)
        for i in range(self.bitlength):
            P = B.add_pubkeys(
                B.multiply(getNUMS(i + 1), fyn[i] % B.N),
                P
            )
        # hy is the exponent of hprime
        # zynz22n = (yn * z) + (power_of_twos * z2)
        for i in range(self.bitlength):
            P = B.add_pubkeys(
                B.multiply(hprime[i], yn[i]),
                P
            )
        fs_state, fs_challenge = fiat_shamir(
            fs_state, [tau_x, mu, t], nret=1)
        uchallenge: Scalar = fs_challenge[0]
        U = B.multiply(B.G, uchallenge)
        P = B.add_pubkeys(
            B.multiply(U, t),
            P
        )
        # P should now be : A + xS + -zG* + (zy^n+z^2.2^n)H'* + tU
        # One can show algebraically (the working is omitted from the paper)
        # that this will be the same as an inner product commitment to
        # (lx, rx) vectors (whose inner product is t), thus the variable 'proof'
        # can be passed into the IPC verify call, which should pass.
        # input to inner product proof is P.h^-(mu)
        p_prime = B.add_pubkeys(
            P,
            B.multiply(getNUMS(255), -mu % B.N)
        )
        a, b, L, R = proof
        iproof = InnerProductCommitment(
            power_of_ones,
            power_of_twos,
            H=hprime,
            U=U
        )
        return iproof.verify_proof(a, b, p_prime, L, R)
