import json
from django.test import TestCase
from restlib2.http import codes
from avocado.conf import OPTIONAL_DEPS
from serrano.resources import API_VERSION


class ExporterResourceTestCase(TestCase):
    def test_get(self):
        response = self.client.get('/api/data/export/',
                                   HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, codes.ok)
        self.assertEqual(response['Content-Type'], 'application/json')

        expectedResponse = {
            'title': 'Serrano Exporter Endpoints',
            'version': API_VERSION,
            '_links': {
                'self': {'href': 'http://testserver/api/data/export/'},
                'json': {
                    'href': 'http://testserver/api/data/export/json/',
                    'description': 'JavaScript Object Notation (JSON)',
                    'title': 'JSON'
                },
                'r': {
                    'href': 'http://testserver/api/data/export/r/',
                    'description': 'R Programming Language',
                    'title': 'R'
                },
                'sas': {
                    'href': 'http://testserver/api/data/export/sas/',
                    'description': 'Statistical Analysis System (SAS)',
                    'title': 'SAS'
                },
                'csv': {
                    'href': 'http://testserver/api/data/export/csv/',
                    'description': 'Comma-Separated Values (CSV)',
                    'title': 'CSV'
                }
            },
        }

        if OPTIONAL_DEPS['openpyxl']:
            expectedResponse['_links']['excel'] = {
                'href': 'http://testserver/api/data/export/excel/',
                'description': 'Microsoft Excel 2007 Format',
                'title': 'Excel'
            }

        self.assertEqual(json.loads(response.content), expectedResponse)

    def test_export_bad_type(self):
        response = self.client.get('/api/data/export/bad_type/')
        self.assertEqual(response.status_code, codes.not_found)

    def test_export_all_pages(self):
        response = self.client.get('/api/data/export/csv/')
        self.assertEqual(response.status_code, codes.no_content)
        self.assertTrue(response.get('Content-Disposition').startswith(
            'attachment; filename="all'))
        self.assertEqual(response.get('Content-Type'), 'text/csv')

    def test_export_one_page(self):
        response = self.client.get('/api/data/export/csv/1/')
        self.assertEqual(response.status_code, codes.no_content)
        self.assertTrue(response.get('Content-Disposition').startswith(
            'attachment; filename="p1'))
        self.assertEqual(response.get('Content-Type'), 'text/csv')

    def test_export_page_range(self):
        response = self.client.get('/api/data/export/csv/1...2/')
        self.assertEqual(response.status_code, codes.no_content)
        self.assertTrue(response.get('Content-Disposition').startswith(
            'attachment; filename="p1-2'))
        self.assertEqual(response.get('Content-Type'), 'text/csv')

    def test_export_equal_page_range(self):
        response = self.client.get('/api/data/export/csv/1...1/')
        self.assertEqual(response.status_code, codes.no_content)
        self.assertTrue(response.get('Content-Disposition').startswith(
            'attachment; filename="p1'))
        self.assertEqual(response.get('Content-Type'), 'text/csv')

    def test_export_zero_page(self):
        response = self.client.get('/api/data/export/csv/0/')
        self.assertEqual(response.status_code, codes.not_found)

    def test_export_bad_page_range(self):
        response = self.client.get('/api/data/export/csv/3...1/')
        self.assertEqual(response.status_code, codes.not_found)
