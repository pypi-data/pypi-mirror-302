# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Any, List, Generic, TypeVar, Optional, cast
from typing_extensions import Protocol, override, runtime_checkable

from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["SyncMyCursorIDPage", "AsyncMyCursorIDPage"]

_T = TypeVar("_T")


@runtime_checkable
class MyCursorIDPageItem(Protocol):
    id: str


class SyncMyCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    my_data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        my_data = self.my_data
        if not my_data:
            return []
        return my_data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        my_data = self.my_data
        if not my_data:
            return None

        if is_forwards:
            item = cast(Any, my_data[-1])
            if not isinstance(item, MyCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.id})
        else:
            item = cast(Any, self.my_data[0])
            if not isinstance(item, MyCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.id})


class AsyncMyCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    my_data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        my_data = self.my_data
        if not my_data:
            return []
        return my_data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        is_forwards = not self._options.params.get("ending_before", False)

        my_data = self.my_data
        if not my_data:
            return None

        if is_forwards:
            item = cast(Any, my_data[-1])
            if not isinstance(item, MyCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"starting_after": item.id})
        else:
            item = cast(Any, self.my_data[0])
            if not isinstance(item, MyCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
                # TODO emit warning log
                return None

            return PageInfo(params={"ending_before": item.id})
