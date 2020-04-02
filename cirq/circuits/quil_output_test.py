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
def test_quil_one_qubit_gate_repr():
    gate = QuilOneQubitGate(np.array([[1,0],[0,1]]))
    assert repr(gate) == ("""cirq.circuits.quil_output.QuilOneQubitGate(matrix=
[[1,0]
 [0,1]]
)""")

def test_quil_one_qubit_gate_eq():
    gate = QuilOneQubitGate(np.array([[1,0],[0,1]]))
    gate2 = QuilOneQubitGate(np.array([[1,0],[0,1]]))
    assert(cirq.approx_eq(gate, gate2, atol=1e-16))
    gate3 = QuilOneQubitGate(np.array([[1,0],[0,1]]))
    gate4 = QuilOneQubitGate(np.array([[1,0],[0,2]]))
    assert(not cirq.approx_eq(gate4, gate3, atol=1e-16))


def test_quil_two_qubit_gate_repr():
    cirq.testing.assert_equivalent_repr(QuilTwoQubitGate(
        cirq.testing.random_unitary(4)))


def test_quil_two_qubit_gate_unitary():
    u = cirq.testing.random_unitary(2)
    g = QuilOneQubitGate(u)
    cirq.testing.assert_allclose_up_to_global_phase(cirq.unitary(g),
                                                    u,
                                                    atol=1e-7)

    cirq.testing.assert_implements_consistent_protocols(g)


def test_quil_two_qubit_gate_unitary():
    u = cirq.testing.random_unitary(4)
    g = QuilTwoQubitGate.from_matrix(u)
    np.testing.assert_allclose(cirq.unitary(g), u)
