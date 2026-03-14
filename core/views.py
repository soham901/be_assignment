from rest_framework import generics

from core.models import Article
from core.serializers import ArticleSerializer


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('created_at', 'id')
