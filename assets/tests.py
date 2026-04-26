from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Asset, Tag, ChangeLog


class TagTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_tag(self):
        res = self.client.post('/api/tags/', {'name': 'Hero Shot'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['slug'], 'hero-shot')


class AssetCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'title':       'Promo Banner',
            'description': 'Main promo banner for campaign',
            'asset_type':  'image',
            'file_url':    'https://cdn.dre.rw/promo-q2.png',
            'status':      'draft',
        }

    def test_create_asset_returns_201(self):
        res = self.client.post('/api/assets/', self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asset.objects.count(), 1)

    def test_create_asset_auto_creates_changelog(self):
        self.client.post('/api/assets/', self.payload)
        self.assertEqual(ChangeLog.objects.count(), 1)
        self.assertEqual(ChangeLog.objects.first().change_summary, 'Asset created')

    def test_update_asset_adds_changelog_entry(self):
        res      = self.client.post('/api/assets/', self.payload)
        asset_id = res.data['id']
        self.client.patch(f'/api/assets/{asset_id}/', {'status': 'review'})
        self.assertEqual(ChangeLog.objects.filter(asset_id=asset_id).count(), 2)

    def test_search_assets_by_title(self):
        self.client.post('/api/assets/', self.payload)
        res = self.client.get('/api/assets/?search=Promo')
        self.assertEqual(len(res.data), 1)

    def test_history_endpoint(self):
        res      = self.client.post('/api/assets/', self.payload)
        asset_id = res.data['id']
        history  = self.client.get(f'/api/assets/{asset_id}/history/')
        self.assertEqual(history.status_code, status.HTTP_200_OK)
        self.assertEqual(len(history.data), 1)


class QualityTagTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_suggest_tags_for_incomplete_asset(self):
        res      = self.client.post('/api/assets/', {'title': 'X', 'asset_type': 'other'})
        asset_id = res.data['id']
        suggest  = self.client.get(f'/api/assets/{asset_id}/suggest-tags/')
        self.assertIn('needs-better-title', suggest.data['suggestions'])
        self.assertIn('needs-description',  suggest.data['suggestions'])
        self.assertIn('untagged',           suggest.data['suggestions'])