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
    # raise TypeError("object of type '{}' does have a _quil_ method, "
    #                 "but it returned NotImplemented or None.".format(type(val)))