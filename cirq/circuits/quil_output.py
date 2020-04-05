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
from cirq import protocols
from typing import (Callable, Dict, Optional, Sequence, Set, Tuple, Union,
                    TYPE_CHECKING)
import numpy as np

def to_quil_complex_format(num):
        cnum = complex(str(num))
        if cnum.imag == 0:
            return num
        return "{0}+{1}i".format(cnum.real, cnum.imag)

@value.value_equality(approximate=True)
class QuilOneQubitGate(ops.SingleQubitGate):

    def __init__(self, matrix: np.ndarray) -> None:
        self.matrix = matrix

    def _quil_(self, qubits: Tuple['cirq.Qid', ...]) -> str:
        return "DEFGATE USERGATE:\n\t{0}, {1}\n\t{2}, {3}\nUSERGATE {4}".format(to_quil_complex_format(self.matrix[0,0]),
                                                                                to_quil_complex_format(self.matrix[0,1]),
                                                                                to_quil_complex_format(self.matrix[1,0]),
                                                                                to_quil_complex_format(self.matrix[1,1]),
                                                                                qubits[0])

    def __repr__(self) -> str:
        return 'cirq.circuits.quil_output.QuilOneQubitGate(matrix=\n{0}\n)'.format(self.matrix)

    def _value_equality_values_(self):
        return self.matrix

@value.value_equality
class QuilTwoQubitGate(ops.TwoQubitGate):
    def __init__(self, matrix: np.ndarray) -> None:
        self.matrix = matrix

    def _value_equality_values_(self):
        return self.matrix

    def _quil_(self, qubits: Tuple['cirq.Qid', ...]) -> str:
        return "DEFGATE USERGATE:\n\t{0}, {1}, {2}, {3}\n\t{4}, {5}, {6}, {7}\n\t{8}, {9}, {10}, {11}\n\t{12}, {13}, {14}, {15}\nUSERGATE {16}".format(to_quil_complex_format(self.matrix[0,0]),
                                                                                to_quil_complex_format(self.matrix[0,1]),
                                                                                to_quil_complex_format(self.matrix[0,2]),
                                                                                to_quil_complex_format(self.matrix[0,3]),
                                                                                to_quil_complex_format(self.matrix[1,0]),
                                                                                to_quil_complex_format(self.matrix[1,1]),
                                                                                to_quil_complex_format(self.matrix[1,2]),
                                                                                to_quil_complex_format(self.matrix[1,3]),
                                                                                to_quil_complex_format(self.matrix[2,0]),
                                                                                to_quil_complex_format(self.matrix[2,1]),
                                                                                to_quil_complex_format(self.matrix[2,2]),
                                                                                to_quil_complex_format(self.matrix[2,3]),
                                                                                to_quil_complex_format(self.matrix[3,0]),
                                                                                to_quil_complex_format(self.matrix[3,1]),
                                                                                to_quil_complex_format(self.matrix[3,2]),
                                                                                to_quil_complex_format(self.matrix[3,3]),
                                                                                qubits[0])

    def __repr__(self) -> str:
        return 'cirq.circuits.quil_output.QuilTwoQubitGate({0})'.format(self.matrix)

class QuilOutput:
    def __init__(self,
                 operations: 'cirq.OP_TREE',
                 qubits: Tuple['cirq.Qid', ...]) -> None:
        print(operations)
        self.operations = tuple(cirq.ops.flatten_to_ops(operations))
        self.qubits = qubits
    
    def _generate_qubit_ids(self) -> Dict['cirq.Qid', str]:
        return {qubit: str(i) for i, qubit in enumerate(self.qubits)}
    
    def __str__(self):
        output = []
        self._write_quil(lambda s: output.append(s))
        return rename_defgates(''.join(output))

    def _write_quil(self, output_func: Callable[[str], None]) -> None:
        def keep(op: 'cirq.Operation') -> bool:
            return protocols.quil(op) is not None

        def fallback(op):
            if len(op.qubits) not in [1, 2]:
                return NotImplemented

            mat = protocols.unitary(op, None)
            if mat is None:
                return NotImplemented

            if len(op.qubits) == 1:
                return QuilOneQubitGate(mat).on(*op.qubits)
            return QuilTwoQubitGate(mat).on(*op.qubits)

        def on_stuck(bad_op):
            return ValueError(
                'Cannot output operation as QUIL: {!r}'.format(bad_op))

        for main_op in self.operations:
            decomposed = protocols.decompose(
                main_op,
                keep=keep,
                fallback_decomposer=fallback,
                on_stuck_raise=on_stuck)

            for decomposed_op in decomposed:
                output_func(protocols.quil(decomposed_op))

    def rename_defgates(output: str):
        result = output
        defString = "DEFGATE"
        nameString = "USERGATE"
        defIdx = 0
        nameIdx = 0
        gateNum = 0
        i = 0
        while i < len(output):
            if result[i] == defString[defIdx]:
                defIdx += 1
            else:
                defIdx = 0
            if result[i] == nameString[nameIdx]:
                nameIdx += 1
            else:
                nameIdx = 0
            if defIdx == len(defString):
                gateNum += 1
                defIdx = 0
            if nameIdx == len(nameString):
                result = result[:i+1] + str(gateNum) + result[i+1:]
                nameIdx = 0
                i += 1
            i += 1
        return result