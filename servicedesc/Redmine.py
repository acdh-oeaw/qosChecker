import json
import requests


class Redmine:
    baseUrl = None
    auth = None
    filters = None

    def __init__(self, baseUrl, user, pswd):
        self.baseUrl = baseUrl
        self.auth = (user, pswd)
        self.filters = {}

    def clearFilters(self):
        self.filter = {}

    def addFilter(self, prop, value):
        self.filters[prop] = value

    def fetch(self):
        more = True
        data = []
        filters = self.filters.copy()
        filters['offset'] = 0
        filters['limit'] = 1000
        filters['include'] = 'relations'
        while (more):
            r = requests.get(self.baseUrl + '/issues.json', params=filters, auth=self.auth)
            d = json.loads(r.content)
            data += d['issues']
            more = d['limit'] == len(d['issues'])
            filters['offset'] += len(d['issues'])
        return data
            
