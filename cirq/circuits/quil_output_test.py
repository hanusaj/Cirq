# Copyright 2020 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import os
import numpy as np
import pytest

import cirq
from cirq.circuits.quil_output import QuilTwoQubitGate, QuilOneQubitGate


def _make_qubits(n):
    return [cirq.NamedQubit('q{}'.format(i)) for i in range(n)]

def test_write_operations():
    q0, = _make_qubits(1)
    output = cirq.QuilOutput((cirq.X(q0),), (q0,))
    assert(str(output) ==
        """X q0"""
    )

def test_write_operations():
    q0, = _make_qubits(1)
    output = cirq.QuilOutput((cirq.X(q0) ** 0.5,), (q0,))
    print (str(output))

def test_two_qubit_diagonal_gate():
    q0,q1, = _make_qubits(2)
    output = cirq.QuilOutput((cirq.TwoQubitDiagonalGate([0.34, 0.12, 0, 0.96]),), (q0,q1,))
    print(str(output))

# def test_quil_one_qubit_gate_repr():
#     gate = QuilOneQubitGate(np.array([[1,0],[0,1]]))
#     assert repr(gate) == ("""cirq.circuits.quil_output.QuilOneQubitGate(matrix=
# [[1 0]
#  [0 1]]
# )""")

# def test_quil_one_qubit_gate_eq():
#     gate = QuilOneQubitGate(np.array([[1,0],[0,1]]))
#     gate2 = QuilOneQubitGate(np.array([[1,0],[0,1]]))
#     assert(cirq.approx_eq(gate, gate2, atol=1e-16))
#     gate3 = QuilOneQubitGate(np.array([[1,0],[0,1]]))
#     gate4 = QuilOneQubitGate(np.array([[1,0],[0,2]]))
#     assert(not cirq.approx_eq(gate4, gate3, atol=1e-16))


# def test_quil_two_qubit_gate_repr():
#     cirq.testing.assert_equivalent_repr(QuilTwoQubitGate(
#         cirq.testing.random_unitary(4)))


# def test_quil_two_qubit_gate_unitary():
#     u = cirq.testing.random_unitary(2)
#     g = QuilOneQubitGate(u)
#     cirq.testing.assert_allclose_up_to_global_phase(cirq.unitary(g),
#                                                     u,
#                                                     atol=1e-7)

#     cirq.testing.assert_implements_consistent_protocols(g)


# def test_quil_two_qubit_gate_unitary():
#     u = cirq.testing.random_unitary(4)
#     g = QuilTwoQubitGate(u)
#     np.testing.assert_allclose(cirq.unitary(g), u)

def test_all_operations():
    qubits = tuple(_make_qubits(5))
    operations = _all_operations(*qubits, include_measurements=False)
    output = cirq.QuilOutput(operations, qubits)
    print( str(output) )

def _all_operations(q0, q1, q2, q3, q4, include_measurements=True):

    class DummyOperation(cirq.Operation):
        qubits = (q0,)
        with_qubits = NotImplemented

        def _qasm_(self, args: cirq.QasmArgs) -> str:
            return '// Dummy operation\n'

        def _decompose_(self):
            # Only used by test_output_unitary_same_as_qiskit
            return ()  # coverage: ignore

    class DummyCompositeOperation(cirq.Operation):
        qubits = (q0,)
        with_qubits = NotImplemented

        def _decompose_(self):
            return cirq.X(self.qubits[0])

        def __repr__(self):
            return 'DummyCompositeOperation()'

    return (
        cirq.Z(q0),
        cirq.Z(q0)**.625,
        cirq.Y(q0),
        cirq.Y(q0)**.375,
        cirq.X(q0),
        cirq.X(q0)**.875,
        cirq.H(q1),
        cirq.CZ(q0, q1),
        cirq.CZ(q0, q1)**0.25,  # Requires 2-qubit decomposition
        cirq.CNOT(q0, q1),
        cirq.CNOT(q0, q1)**0.5,  # Requires 2-qubit decomposition
        cirq.SWAP(q0, q1),
        cirq.SWAP(q0, q1)**0.75,  # Requires 2-qubit decomposition
        cirq.CCZ(q0, q1, q2),
        cirq.CCX(q0, q1, q2),
        cirq.CCZ(q0, q1, q2)**0.5,
        cirq.CCX(q0, q1, q2)**0.5,
        cirq.CSWAP(q0, q1, q2),
        cirq.IdentityGate(1).on(q0),
        cirq.IdentityGate(3).on(q0, q1, q2),
        cirq.ISWAP(q2, q0),  # Requires 2-qubit decomposition
        cirq.PhasedXPowGate(phase_exponent=0.111, exponent=0.25).on(q1),
        cirq.PhasedXPowGate(phase_exponent=0.333, exponent=0.5).on(q1),
        cirq.PhasedXPowGate(phase_exponent=0.777, exponent=-0.5).on(q1),
        (cirq.measure(q0, key='xX'), cirq.measure(q2, key='x_a'),
         cirq.measure(q1, key='x?'), cirq.measure(q3, key='X'),
         cirq.measure(q4, key='_x'), cirq.measure(q2, key='x_a'),
         cirq.measure(q1, q2, q3, key='multi', invert_mask=(False, True)))
        if include_measurements else (),
        DummyOperation(),
        DummyCompositeOperation(),
    )
