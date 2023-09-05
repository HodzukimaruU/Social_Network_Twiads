from dataclasses import dataclass
from typing import Iterable

from django.core.paginator import EmptyPage, Paginator


class PageNotExists(Exception):
    ...


@dataclass
class PaginationResponse:
    data: Iterable
    next_page: int | None
    prev_page: int | None


class CustomPagination:
    def __init__(self, per_page: int) -> None:
        self._per_page = per_page

    def paginate(self, data: Iterable, page_number: int) -> PaginationResponse:
        paginator = Paginator(data, self._per_page)
        try:
            data_paginated = paginator.page(page_number)
        except EmptyPage:
            raise PageNotExists

        if data_paginated.has_next():
            next_page = data_paginated.next_page_number()
        else:
            next_page = None

        if data_paginated.has_previous():
            prev_page = data_paginated.previous_page_number()
        else:
            prev_page = None

        return PaginationResponse(data=data_paginated, next_page=next_page, prev_page=prev_page)
