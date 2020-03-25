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

from typing import TYPE_CHECKING, Union, Any, Tuple, TypeVar, Optional, Dict, \
    Iterable

TDefault = TypeVar('TDefault')

RaiseTypeErrorIfNotProvided = ([],)

def quil(val,
         *,
         qubits: Optional[Iterable['cirq.Qid']] = None,
         default: TDefault = RaiseTypeErrorIfNotProvided):
    method = getattr(val, '_quil_', None)
    result = NotImplemented
    if method is not None:
        kwargs = {}  # type: Dict[str, Any]
        if qubits is not None:
            kwargs['qubits'] = tuple(qubits)
        result = method(**kwargs)
    if result is not None and result is not NotImplemented:
        return result

    return None
