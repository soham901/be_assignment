from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from core.models import Article
from core.serializers import ArticleSerializer


class ArticlePagination(PageNumberPagination):
    page_size = 10


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('created_at', 'id')
