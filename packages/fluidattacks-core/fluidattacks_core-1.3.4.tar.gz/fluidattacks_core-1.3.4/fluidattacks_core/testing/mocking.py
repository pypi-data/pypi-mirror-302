from .types import (
    T,
)
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from types import (
    ModuleType,
)
from typing import (
    Any,
    Callable,
    Literal,
)

_TargetType = Literal["sync", "async"]


def mock(
    *,
    module: ModuleType,
    target: str,
    target_type: _TargetType,
    expected: T,
) -> None:
    def _sync(*_args: tuple[Any, ...], **_kwargs: dict[Any, Any]) -> T:
        return expected

    async def _async(*_args: tuple[Any, ...], **_kwargs: dict[Any, Any]) -> T:
        return expected

    target_types: dict[_TargetType, Callable] = {
        "sync": _sync,
        "async": _async,
    }

    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(module, target, target_types[target_type])
