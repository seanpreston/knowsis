# -*- coding: utf-8 -*-
import app_settings
import requests
import sys
import unittest

TWEET_URI = 'api/v0/tweets/count/'
TWEET_URL = '%s%s' % (app_settings.API_BASE, TWEET_URI)


class Tests(unittest.TestCase):

    def test_successful_request(self):
        start = '2014-04-01'
        end = '2014-04-05'
        params = '?startdate=%s&enddate=%s' % (start, end)
        resp = requests.get(
            '%s%s' % (TWEET_URL, params),
            headers={'Authorization': 'Bearer %s' % app_settings.ENCODED_TOKEN}
        )
        sys.stdout.write('%s\n' % resp.status_code)
        sys.stdout.write('%s\n\n' % resp.content)
        self.assertEqual(resp.status_code, 200)


    def test_unauthorized(self):
        start = '2014-04-01'
        end = '2014-04-05'
        params = '?startdate=%s&enddate=%s' % (start, end)
        resp = requests.get('%s%s' % (TWEET_URL, params))
        sys.stdout.write('%s\n' % resp.status_code)
        sys.stdout.write('%s\n\n' % resp.content)
        self.assertEqual(resp.status_code, 401)


    def test_range_too_large(self):
        start = '2014-04-01'
        end = '2014-04-16'
        params = '?startdate=%s&enddate=%s' % (start, end)
        resp = requests.get(
            '%s%s' % (TWEET_URL, params),
            headers={'Authorization': 'Bearer %s' % app_settings.ENCODED_TOKEN}
        )
        sys.stdout.write('%s\n' % resp.status_code)
        sys.stdout.write('%s\n\n' % resp.content)
        self.assertEqual(resp.status_code, 400)


    def test_range_too_far(self):
        start = '2013-04-01'
        end = '2013-04-16'
        params = '?startdate=%s&enddate=%s' % (start, end)
        resp = requests.get(
            '%s%s' % (TWEET_URL, params),
            headers={'Authorization': 'Bearer %s' % app_settings.ENCODED_TOKEN}
        )
        sys.stdout.write('%s\n' % resp.status_code)
        sys.stdout.write('%s\n\n' % resp.content)
        self.assertEqual(resp.status_code, 400)


    def test_no_start(self):
        end = '2014-04-16'
        params = '?enddate=%s' % end
        resp = requests.get(
            '%s%s' % (TWEET_URL, params),
            headers={'Authorization': 'Bearer %s' % app_settings.ENCODED_TOKEN}
        )
        sys.stdout.write('%s\n' % resp.status_code)
        sys.stdout.write('%s\n\n' % resp.content)
        self.assertEqual(resp.status_code, 400)


    def test_no_end(self):
        start = '2014-04-01'
        params = '?startdate=%s' % start
        resp = requests.get(
            '%s%s' % (TWEET_URL, params),
            headers={'Authorization': 'Bearer %s' % app_settings.ENCODED_TOKEN}
        )
        sys.stdout.write('%s\n' % resp.status_code)
        sys.stdout.write('%s\n\n' % resp.content)
        self.assertEqual(resp.status_code, 200)


    def test_start_after_end(self):
        start = '2014-04-05'
        end = '2014-04-04'
        params = '?startdate=%s&enddate=%s' % (start, end)
        resp = requests.get(
            '%s%s' % (TWEET_URL, params),
            headers={'Authorization': 'Bearer %s' % app_settings.ENCODED_TOKEN}
        )
        sys.stdout.write('%s\n' % resp.status_code)
        sys.stdout.write('%s\n\n' % resp.content)
        self.assertEqual(resp.status_code, 400)


if __name__ == '__main__':
    unittest.main()
