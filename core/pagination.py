from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(DRFPageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 50


class CustomArticlePagination(DRFPageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_page_size(self, request):
        raw_page_size = request.query_params.get(self.page_size_query_param)

        if raw_page_size in (None, ""):
            return self.page_size

        try:
            page_size = int(raw_page_size)
        except (TypeError, ValueError) as exc:
            raise ValidationError(
                {"page_size": "page_size must be a whole number."}
            ) from exc

        if page_size < 1:
            raise ValidationError({"page_size": "page_size must be greater than 0."})

        if page_size > self.max_page_size:
            raise ValidationError(
                {"page_size": f"page_size must not exceed {self.max_page_size}."}
            )

        return page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "page_info": {
                    "current_page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                    "page_size": self.get_page_size(self.request),
                    "next_page": self.get_next_link(),
                    "previous_page": self.get_previous_link(),
                    "has_next": self.page.has_next(),
                    "has_previous": self.page.has_previous(),
                },
                "items_info": {
                    "total_items": self.page.paginator.count,
                    "items_on_page": len(data),
                },
                "results": data,
            }
        )
