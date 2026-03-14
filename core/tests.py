from django.urls import reverse
from rest_framework.test import APITestCase


class ArticlePaginationTests(APITestCase):
    fixtures = ['articles.json']

    def test_article_list_uses_custom_default_page_size(self):
        response = self.client.get(reverse('article-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['page_info']['page_size'], 8)
        self.assertEqual(response.data['items_info']['items_on_page'], 8)

    def test_article_list_returns_custom_metadata(self):
        response = self.client.get(reverse('article-list'), {'page': 2, 'page_size': 5})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['page_info']['current_page'], 2)
        self.assertEqual(response.data['page_info']['total_pages'], 8)
        self.assertEqual(response.data['page_info']['page_size'], 5)
        self.assertEqual(response.data['items_info']['total_items'], 40)
        self.assertEqual(response.data['items_info']['items_on_page'], 5)

    def test_article_list_rejects_non_numeric_page_size(self):
        response = self.client.get(reverse('article-list'), {'page_size': 'abc'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['page_size'], 'page_size must be a whole number.')

    def test_article_list_rejects_page_size_above_limit(self):
        response = self.client.get(reverse('article-list'), {'page_size': 100})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['page_size'], 'page_size must not exceed 50.')
