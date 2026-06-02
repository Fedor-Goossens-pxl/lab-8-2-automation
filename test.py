#!/usr/bin/env python3
from ncclient import manager
import xml.dom.minidom as minidom

mgr = manager.connect(
    host='192.168.19.139',
    port=830,
    username='cisco',
    password='cisco123!',
    hostkey_verify=False,
    timeout=30,
    allow_agent=False,
    look_for_keys=False
)

# GET huidige NTP configuratie
FILTER = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ntp/>
  </native>
</filter>
"""

response = mgr.get_config(source='running', filter=FILTER)
print(minidom.parseString(response.xml).toprettyxml())

mgr.close_session()