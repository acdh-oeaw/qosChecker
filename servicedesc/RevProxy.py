import logging
import paramiko
import re


class RevProxy:
    host = None
    user = None

    def __init__(self, host, user):
        self.host = host
        self.user = user

    def fetch(self):
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        logging.getLogger('paramiko').setLevel(logging.WARNING)
        client.connect(self.host, username=self.user)

        cfgStr = ''
        stdin, files, stderr = client.exec_command('ls -1 /etc/httpd/conf.d/sites-enabled')
        for i in files:
            stdin, config, stderr = client.exec_command('cat /etc/httpd/conf.d/sites-enabled/' + i)
            cfgStr += ''.join(config)

        client.close()
        return self.parse(cfgStr)

    def parse(self, cfgStr):
        vhosts = []
        for i in re.split('</VirtualHost>', cfgStr):
            i = i.split('\n')
            port = self.find('^\s*<VirtualHost[^:]*:([0-9]+)\s*>', i, re.IGNORECASE)
            serverName = self.find('^\s*ServerName\s+([-a-zA-Z0-9._]+)', i, re.IGNORECASE)
            serverAlias = self.find('^\s*ServerAlias\s+([-a-zA-Z0-9._]+)', i, re.IGNORECASE)
            proxy = self.find('^\s*ProxyPass\s+([^ ]+)\s*([^:]+://([^/])+[^ ]*)', i, re.IGNORECASE)
            preserveHost = self.find('ProxyPreserveHost\s+On', i, re.IGNORECASE)
            if len(port) > 0 and len(serverName) > 0:
                vhost = {
                    'port': port[0][1], 
                    'domain': [serverName[0][1]], 
                    'proxy': [],
                    'preserveHost': len(preserveHost) > 0
                }
                for i in serverAlias:
                    vhost['domain'].append(i[1])
                for i in proxy:
                    vhost['proxy'].append({'path': i[1], 'url': i[2], 'domain': i[3]})
                vhosts.append(vhost)
        return vhosts

    def find(self, regex, strings, flags):
        matches = []
        for i in strings:
            match = re.search(regex, i, flags)
            if match is not None:
                matches.append(match)
        return matches
