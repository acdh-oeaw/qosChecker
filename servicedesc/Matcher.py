import json
import re


class Matcher:
    def match(self, services):
        for srv in services['dockerTools']:
            srv['links'] = {'redmine': None, 'proxy': {}}
            if 'ID' in srv:
                for i in services['redmine']:
                    if int(i['id']) == int(srv['ID']):
                        srv['links']['redmine'] = i
                        break
            if 'ServerName' in srv:
                srv['links']['proxy'][srv['ServerName']] = []
                for i in services['proxy']:
                    if srv['ServerName'] in i['domain']:
                        srv['links']['proxy'][srv['ServerName']].append(i)
        for srv in services['redmine']:
            srv['links'] = {'dockerTools': [], 'proxy': {}}
            for i in services['dockerTools']:
                if 'ID' in i and int(i['ID']) == int(srv['id']):
                    srv['links']['dockerTools'].append(i)
            for domain in self.getRedmineDomains(srv):
                srv['links']['proxy'][domain] = []
                for i in services['proxy']:
                    if domain in i['domain']:
                        srv['links']['proxy'][domain].append(i)
        for srv in services['proxy']:
            srv['links'] = {'dockerTools': [], 'redmine': []}
            for domain in srv['domain']:
                for i in services['dockerTools']:
                    if 'ServerName' in i and i['ServerName'] == domain:
                        srv['links']['dockerTools'].append(i)
                for i in services['redmine']:
                    if domain in self.getRedmineDomains(i):
                        srv['links']['redmine'].append(i)

    def getRedmineDomains(self, srv):
        for i in srv['custom_fields']:
            if i['name'] == 'endpoint' and 'value' in i:
                domains = [x.strip() for x in i['value'].split('\n')]
                domains = [re.sub('^[^:]+://([^/]+).*$', '\\1', x) for x in domains]
                domains = [x for x in domains if ' ' not in x]
                return domains
        return []

