# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# from exceptions import BadRequest
from itertools import groupby

import csv
import app_settings
import time


class BadRequest(Exception):

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        data = dict(self.payload or ())
        data['error_message'] = self.message
        return data


def _get_row_data():
    with open(app_settings.INPUT_FILE, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')
        rows = [row[0].split(' ')[0] for row in reader]
        row_data = dict((key,len(list(group))) for key, group in groupby(rows))
        return row_data


def _get_date(date_string):
    return datetime.fromtimestamp(time.mktime(time.strptime(date_string, '%Y-%m-%d')))


def _get_date_keys(start_date, delta):
    keys = [(start_date + timedelta(days=days)).strftime('%Y-%m-%d') for days in range(delta.days + 1)]
    return keys


def get_tweet_count(start, end=None):
    row_data = _get_row_data()

    start_date = _get_date(start)
    if (datetime.today() - relativedelta(months=9)) > start_date:
        raise BadRequest('You cannot request data from more than nine months in the past', status_code=400)

    if end:
        end_date = _get_date(end)

        delta = (end_date - start_date)
        if delta.days > app_settings.DATE_RANGE_LIMIT_DAYS:
            raise BadRequest('The date range must be two weeks or less', status_code=400)
        elif delta.days < 0:
            raise BadRequest('The start date must be before the end date', status_code=400)

        keys = _get_date_keys(start_date, delta)

    else:
        keys = [start]

    tweet_count = sum([row_data[key] for key in keys])
    return tweet_count
