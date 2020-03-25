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
        self.measurements = tuple(op for op in self.operations
                                  if isinstance(op.gate, cirq.ops.MeasurementGate))
        # self.meas_comments = meas_comments
        qubit_id_map = self._generate_qubit_ids()
    
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
            
            # should_annotate = decomposed != [main_op]
            # if should_annotate:
            #     output_line_gap(1)
            #     if isinstance(main_op, ops.GateOperation):
            #         x = str(main_op.gate).replace('\n', '\n //')
            #         output('// Gate: {!s}\n'.format(x))
            #     else:
            #         x = str(main_op).replace('\n', '\n //')
            #         output('// Operation: {!s}\n'.format(x))

            for decomposed_op in decomposed:
                output_func(protocols.quil(decomposed_op))

            # if should_annotate:
            #     output_line_gap(1)
            # output_func(cirq.protocols.quil(main_op))