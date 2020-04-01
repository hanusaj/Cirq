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

import cirq

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