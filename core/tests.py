from django.urls import reverse
from rest_framework.test import APITestCase

from core.models import Article


class ArticlePaginationTests(APITestCase):
    fixtures = ['articles.json']

    def test_article_list_uses_global_default_pagination(self):
        response = self.client.get(reverse('article-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 15)

    def test_article_list_honors_page_size_query_param(self):
        response = self.client.get(reverse('article-list'), {'page_size': 5})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 5)

    def test_article_list_caps_page_size_at_max_limit(self):
        Article.objects.bulk_create(
            [
                Article(
                    title=f'Extra Article {index}',
                    content='Extra content',
                    author='Load Test',
                    is_published=True,
                )
                for index in range(1, 31)
            ]
        )

        response = self.client.get(reverse('article-list'), {'page_size': 100})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 50)

    def test_invalid_page_size_falls_back_to_default_page_size(self):
        response = self.client.get(reverse('article-list'), {'page_size': 'abc'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 15)
