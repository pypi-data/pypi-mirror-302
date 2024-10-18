import os
from datetime import datetime, date, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

class GoogleSearchConsole():

    def __init__(self, credentials):
        credentials = Credentials.from_authorized_user_info(credentials, ["https://www.googleapis.com/auth/webmasters.readonly"])

        request_object = Request()
        credentials.refresh(request_object)
        service = build("searchconsole", "v1", credentials=credentials)

        GoogleSearchConsole.service = service


    def find_latest_date(self, agg_type='auto', data_state='final'):
        site = 'https://fishingbooker.com/'
        request = {
            'startDate': datetime.strftime(date.today() - timedelta(days=10), '%Y-%m-%d'),
            'endDate': datetime.strftime(date.today(), '%Y-%m-%d'),
            'dimensions': ['date'],
            'aggregationType': agg_type,
            'dataState': data_state
        }

        results = GoogleSearchConsole.service.searchanalytics().query(siteUrl=site, body=request).execute()
        return results['rows'][-1]['keys'][0]


    def query(self, start_date, end_date, dimensions, row_limit=25000, filters=None, agg_type=None, search_type='web', offset=0, data_state='final'):
        site = 'https://fishingbooker.com/'
        data = []
        offset = offset

        while True:
            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': dimensions,
                'rowLimit': row_limit,
                'aggregationType': agg_type if agg_type else 'auto',
                'dimensionFilterGroups': filters if filters else [],
                'type': search_type,
                'startRow': offset,
                'dataState': data_state
            }

            results = GoogleSearchConsole.service.searchanalytics().query(siteUrl=site, body=request).execute()

            if 'rows' in results:
                if len(results["rows"]) > 0:
                    offset += len(results['rows'])
            else:
                break

            data.extend(results['rows'])

        print(f'Extraction completed - {len(data)} rows total')
        return data