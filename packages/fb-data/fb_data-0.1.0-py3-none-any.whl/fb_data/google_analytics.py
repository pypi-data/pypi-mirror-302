from collections import defaultdict
import re
import pandas as pd

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class GoogleAnalytics():


    def __init__(self, credentials):
        self.credentials = credentials
        self.user_credentials = Credentials.from_authorized_user_info(info=credentials)
        self.service = build('analyticsdata', 'v1beta', credentials=self.user_credentials)


    def __camel_to_snake(self, camel_str):
        snake_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        snake_str = re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake_str).lower()
        return snake_str


    def report(self, request, property_id, pandas=False, snake_case=True, date_format=None):
        self.dimensions = [dimension['name'] for dimension in request['requests']['dimensions']]
        self.metrics = [metric['name'] for metric in request['requests']['metrics']]
        
        response = self.service.properties().batchRunReports(property=f'properties/{property_id}', body=request).execute()
        
        if pandas == True:
            from collections import defaultdict
            import pandas as pd

            report_data = defaultdict(list)
            for report in response.get('reports', []):
                rows = report.get('rows', [])
                for row in rows:
                    for i, key in enumerate(self.dimensions):
                        report_data[key].append(row.get('dimensionValues', [])[i]['value'])  # Get dimensions
                    for i, key in enumerate(self.metrics):
                        report_data[key].append(row.get('metricValues', [])[i]['value'])  # Get metrics
            
            response = pd.DataFrame(report_data)
            
            if snake_case == True:
                response = response.rename(columns={col: self.__camel_to_snake(col) for col in response.columns})
            
            if len(report_data) > 0 and date_format != None and 'date' in self.dimensions:
                response['date'] = pd.to_datetime(response['date'], format=date_format)
        
        return response