import argparse
import requests
import keystoneclient
import json


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(description='Process some integers.')
    keystoneauth = {
        "auth": {"passwordCredentials": {"username": "admin", "password": "admin"}, "tenantName": "admin"}}
    token = requests.post('http://127.0.0.1:5000/v2.0/tokens', headers={'Content-Type': 'application/json'},
                          data=json.dumps(keystoneauth))
    token = json.loads(token.text)['access']['token']['id']
    nodes = requests.get('http://127.0.0.1:8000/api/nodes', headers={'X-Auth-Token': token})
    nodes = json.loads(nodes.text)

    for node in nodes:
        if (node['status'] == 'error') and (node['id'] not in [68, 77, 78, 79, 80, 81]):
            print (node['id'])
            nodeready = requests.put('http://127.0.0.1:8000/api/nodes/{0}'.format(node['id']),
                                     headers={'X-Auth-Token': token}, data=json.dumps({'status': 'ready'}))
            print(nodeready.status_code)


if __name__ == "__main__":
    main()
