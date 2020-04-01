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

class QuilOutput:
    def __init__(self,
                 operations: 'cirq.OP_TREE',
                 qubits: Tuple['cirq.Qid', ...]) -> None:
        self.operations = tuple(cirq.ops.flatten_to_ops(operations))
        self.qubits = qubits
    
    def _generate_qubit_ids(self) -> Dict['cirq.Qid', str]:
        return {qubit: str(i) for i, qubit in enumerate(self.qubits)}
    
    def __str__(self):
        output = []
        self._write_quil(lambda s: output.append(s))
        return ''.join(output)

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
                return QasmUGate.from_matrix(mat).on(*op.qubits)
            return QasmTwoQubitGate.from_matrix(mat).on(*op.qubits)

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