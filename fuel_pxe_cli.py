import argparse
import requests
import json

BOND_INTERFACE = {u'name': u'bond0', u'interface_properties': {u'disable_offloading': True, u'mtu': None}, u'state': None, u'mac': None, u'bond_properties': {u'lacp_rate': u'fast', u'type__': u'linux', u'mode': u'802.3ad', u'xmit_hash_policy': u'layer2+3'}, u'mode': u'802.3ad', u'slaves': [], u'assigned_networks': [], u'type': u'bond'}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Configure Bonding and PXE network")
    parser.add_argument("-node", "--node-id", type=int, help="Node id.", required=True)
    parser.add_argument("--pxe", type=str, help="Name of PXE interface.", required=True)
    parser.add_argument("--slave1", type=str, help="Name of Bond Slave1 interface.", required=True)
    parser.add_argument("--slave2", type=str, help="Name of Bond Slave2 interface.", required=True)
    args = parser.parse_args()

    keystoneauth={"auth":{"passwordCredentials":{"username": "admin", "password": "admin"},"tenantName": "admin"}}
    token = requests.post('http://127.0.0.1:5000/v2.0/tokens', headers={'Content-Type': 'application/json'}, data=json.dumps(keystoneauth))
    token = json.loads(token.text)['access']['token']['id']

    interfaces = requests.get('http://127.0.0.1:8000/api/nodes/{0}/interfaces/'.format(args.node_id), headers={'X-Auth-Token': token})
    interfaces = json.loads(interfaces.text)

    osnetworks = []
    for interface in interfaces:
        for net in interface['assigned_networks']:
            osnetworks.append(net)

    for interface in interfaces:
        if len(interface['assigned_networks']) > 0:
            interface['assigned_networks'] = []

    slaves = [dict({u'name': unicode(slave1)}), dict({u'name': unicode(slave2)})]

    for interface in interfaces:
        if interface['name'] == unicode(pxe):
            interface['assigned_networks'] = [(item for item in osnetworks if item['name'] == u'fuelweb_admin').next()]

    if interfaces[-1]['name'] != 'bond0':
        interfaces.append(BOND_INTERFACE)

    interfaces[-1]['slaves'] = list(slaves)

    for net in osnetworks:
        if net['name'] != u'fuelweb_admin':
            interfaces[-1]['assigned_networks'].append(net)

    interfaces = requests.put('http://127.0.0.1:8000/api/nodes/{0}/interfaces/'.format(args.node_id), headers={'X-Auth-Token': token}, data=json.dumps(interfaces))
    print interfaces.text