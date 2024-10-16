import sys
from collections.abc import Awaitable, Callable, Generator, Iterable
from concurrent.futures._base import Future as _ConcurrentFuture
from contextvars import Context
from typing import Any, Literal, TypeVar
from typing_extensions import Self, TypeIs

from .events import AbstractEventLoop

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = ("Future", "wrap_future", "isfuture")

_T = TypeVar("_T")

# asyncio defines 'isfuture()' in base_futures.py and re-imports it in futures.py
# but it leads to circular import error in pytype tool.
# That's why the import order is reversed.
def isfuture(obj: object) -> TypeIs[Future[Any]]: ...

class Future(Awaitable[_T], Iterable[_T]):
    """
    This class is *almost* compatible with concurrent.futures.Future.

    Differences:

    - result() and exception() do not take a timeout argument and
      raise an exception when the future isn't done yet.

    - Callbacks registered with add_done_callback() are always called
      via the event loop's call_soon_threadsafe().

    - This class is not compatible with the wait() and as_completed()
      methods in the concurrent.futures package.
    """
    _state: str
    @property
    def _exception(self) -> BaseException | None: ...
    _blocking: bool
    @property
    def _log_traceback(self) -> bool: ...
    @_log_traceback.setter
    def _log_traceback(self, val: Literal[False]) -> None: ...
    _asyncio_future_blocking: bool  # is a part of duck-typing contract for `Future`
    def __init__(self, *, loop: AbstractEventLoop | None = ...) -> None: ...
    def __del__(self) -> None:
        """Called when the instance is about to be destroyed."""
        ...
    def get_loop(self) -> AbstractEventLoop:
        """Return the event loop the Future is bound to."""
        ...
    @property
    def _callbacks(self) -> list[tuple[Callable[[Self], Any], Context]]: ...
    def add_done_callback(self, fn: Callable[[Self], object], /, *, context: Context | None = None) -> None:
        """
        Add a callback to be run when the future becomes done.

        The callback is called with a single argument - the future object. If
        the future is already done when this is called, the callback is
        scheduled with call_soon.
        """
        ...
    if sys.version_info >= (3, 9):
        def cancel(self, msg: Any | None = None) -> bool:
            """
            Cancel the future and schedule callbacks.

            If the future is already done or cancelled, return False.  Otherwise,
            change the future's state to cancelled, schedule the callbacks and
            return True.
            """
            ...
    else:
        def cancel(self) -> bool:
            """
            Cancel the future and schedule callbacks.

            If the future is already done or cancelled, return False.  Otherwise,
            change the future's state to cancelled, schedule the callbacks and
            return True.
            """
            ...

    def cancelled(self) -> bool:
        """Return True if the future was cancelled."""
        ...
    def done(self) -> bool:
        """
        Return True if the future is done.

        Done means either that a result / exception are available, or that the
        future was cancelled.
        """
        ...
    def result(self) -> _T:
        """
        Return the result this future represents.

        If the future has been cancelled, raises CancelledError.  If the
        future's result isn't yet available, raises InvalidStateError.  If
        the future is done and has an exception set, this exception is raised.
        """
        ...
    def exception(self) -> BaseException | None:
        """
        Return the exception that was set on this future.

        The exception (or None if no exception was set) is returned only if
        the future is done.  If the future has been cancelled, raises
        CancelledError.  If the future isn't done yet, raises
        InvalidStateError.
        """
        ...
    def remove_done_callback(self, fn: Callable[[Self], object], /) -> int:
        """
        Remove all instances of a callback from the "call when done" list.

        Returns the number of callbacks removed.
        """
        ...
    def set_result(self, result: _T, /) -> None:
        """
        Mark the future done and set its result.

        If the future is already done when this method is called, raises
        InvalidStateError.
        """
        ...
    def set_exception(self, exception: type | BaseException, /) -> None:
        """
        Mark the future done and set an exception.

        If the future is already done when this method is called, raises
        InvalidStateError.
        """
        ...
    def __iter__(self) -> Generator[Any, None, _T]:
        """Implement iter(self)."""
        ...
    def __await__(self) -> Generator[Any, None, _T]:
        """Return an iterator to be used in await expression."""
        ...
    @property
    def _loop(self) -> AbstractEventLoop: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias:
            """See PEP 585"""
            ...

def wrap_future(future: _ConcurrentFuture[_T] | Future[_T], *, loop: AbstractEventLoop | None = None) -> Future[_T]: ...
