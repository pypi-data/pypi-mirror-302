
# Python Networking Libraries
-----------------------
Python libraries for [Netbox](https://github.com/netbox-community/netbox), [LibreNMS](https://github.com/librenms/librenms), [FreeIPA](https://github.com/freeipa/freeipa), and [SNMP](https://github.com/lextudio/pysnmp)
FreeIPA client adapted from [nordnet/python-freeipa-json](https://github.com/nordnet/python-freeipa-json)

## Install
--------
```
pip install py_network_apis
```
## Examples
--------

To use the LibreNMS client:

```python
from py_network_apis.libre_client import libre

librenms = libre(api_url="http://librenms.org/api/v0",
                 token="04ec2439-cf1b-4d1f-aa60-9b0da99b6eab")

alerts = librenms.get_alerts()

print(alerts)
```
Output:
```python
[{'hostname': 'localhost', 'id': 99, 'device_id': 1, 'rule_id': 1, 'state': 1, 'alerted': 1,
 'open': 1, 'note': '', 'timestamp': '2024-01-01 01:01:01', 'info': '', 'severity': 'critical'}]

```
--------

To use the IPA client:

```python
from py_network_apis.ipa_client import ipa

free_ipa = ipa("ipaserver.example.net")
free_ipa.login("ipa_user","ipa_password")

dns_record = free_ipa.dnsrecord_find("example.net","hostname")
print(dns_record)
```
Output:

```python
[{'idnsname': ['hostname'], 'arecord': ['127.0.0.1'], 
'dn':'idnsname=hostname,idnsname=example.net.,cn=dns,dc=example,dc=net'}]

```
--------
To use the Netbox Client:
```python
from py_network_apis.netbox_client import netbox

nb = netbox(url="http://netbox.example.com",
token="516b61e3-1b73-4f29-bdcf-f8f1ebca5371")

device = nb.get_device_by_ip("127.0.0.1")

print(dict(device))
```
Output:
```python
{'id': 1, 'url': 'https://netbox.example.com/api/dcim/devices/1/', 'display': 'hostname', 'name': 'hostname', 'description': ''}
```
--------

To use SNMP Client:
```python
from py_network_apis.snmp_client import *

resp = snmp_get(ip="127.0.0.1",oids=["sysUpTime"],version="v2",community="public",port=161)

print(resp)
```
Output:
```python
['SNMPv2-MIB::sysUpTime.0 = 118674300']
```