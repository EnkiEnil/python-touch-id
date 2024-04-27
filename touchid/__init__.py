"""
A module for accessing the Touch ID sensor in your Mac's Touch Bar.

Requires pyobjc to be installed
"""

__all__ = ("authenticate", "is_available")

import ctypes
import sys
from dataclasses import dataclass
from typing import Protocol

from LocalAuthentication import LAContext  # type: ignore[import-untyped]
from LocalAuthentication import (
    LAPolicyDeviceOwnerAuthenticationWithBiometrics as kTouchIdPolicy,
)

c = ctypes.CDLL(None)

DISPATCH_TIME_FOREVER = sys.maxsize

dispatch_semaphore_create = c.dispatch_semaphore_create
dispatch_semaphore_create.restype = ctypes.c_void_p
dispatch_semaphore_create.argtypes = [ctypes.c_int]

dispatch_semaphore_wait = c.dispatch_semaphore_wait
dispatch_semaphore_wait.restype = ctypes.c_long
dispatch_semaphore_wait.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

dispatch_semaphore_signal = c.dispatch_semaphore_signal
dispatch_semaphore_signal.restype = ctypes.c_long
dispatch_semaphore_signal.argtypes = [ctypes.c_void_p]


@dataclass()
class _Result:
    success: bool
    error: str | None


class _NSError(Protocol):
    def localizedDescription(self) -> str: ...


def is_available() -> bool:
    context = LAContext.new()
    can_evaluate: bool = context.canEvaluatePolicy_error_(kTouchIdPolicy, None)[0]
    return can_evaluate


def authenticate(reason: str = "authenticate via Touch ID") -> bool:
    if not is_available():
        raise Exception("Touch ID isn't available on this machine")

    context = LAContext.new()
    sema = dispatch_semaphore_create(0)
    res: _Result

    def cb(_success: bool, _error: _NSError | None) -> None:
        nonlocal res

        res = _Result(
            success=_success,
            error=_error.localizedDescription() if _error else None,
        )
        dispatch_semaphore_signal(sema)

    context.evaluatePolicy_localizedReason_reply_(kTouchIdPolicy, reason, cb)
    dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER)

    if res.error:
        raise Exception(res.error)

    return res.success
