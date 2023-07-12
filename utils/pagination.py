from rest_framework.pagination import PageNumberPagination



class PaginationWithPageNumber(PageNumberPagination):
    page_size = 10