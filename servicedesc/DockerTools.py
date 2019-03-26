import json
import logging
import paramiko


class DockerTools:
    hosts = None
    user = None

    def __init__(self, hosts, user):
        self.hosts = hosts
        self.user = user

    def fetch(self):
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        logging.getLogger('paramiko').setLevel(logging.WARNING)

        cfgs = []
        for host in self.hosts:
            client.connect(host, username=self.user)

            stdin, files, stderr = client.exec_command('ls -1 /home/*/config.json')
            for i in files:
                stdin, config, stderr = client.exec_command('cat ' + i)
                user = i.split('/')[2]
                try:
                    tmp = json.load(config)
                    for j in tmp:
                        j['User'] = user
                        j['Host'] = host
                        cfgs.append(j)
                except json.decoder.JSONDecodeError:
                    pass

            client.close()
        return cfgs

