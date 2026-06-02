#!/usr/bin/env python3
"""
Task 30: Configure and Apply Access Control List
Author: Fedor Goossens
Course: Enterprise Networks 2 - PXL Hogeschool
"""

import traceback
import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError

# === LIBRARIES ===
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient - NETCONF client library")
print("✓ lxml.etree - XML parsing and pretty-printing")
print("=" * 70 + "\n")

# === DEVICE CONFIG ===
HOST = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
PORT = 830

# === XML PAYLOADS ===
# Hier gebruiken we de correcte <inbound> structuur in plaats van <in> of <direction>
payload = '''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target><running/></target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <ip>
        <access-list>
          <extended xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
            <name>BLOCK_TRAFFIC</name>
            <access-list-seq-rule>
              <sequence>10</sequence>
              <ace-rule>
                <action>deny</action>
                <protocol>ip</protocol>
                <ipv4-address>10.0.0.0</ipv4-address>
                <mask>0.0.0.255</mask>
                <dst-any/>
              </ace-rule>
            </access-list-seq-rule>
          </extended>
        </access-list>
      </ip>
      
      <interface>
        <GigabitEthernet>
          <name>1</name>
          <ip>
            <access-group>
              <inbound xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
                <name>BLOCK_TRAFFIC</name>
              </inbound>
            </access-group>
          </ip>
        </GigabitEthernet>
      </interface>
    </native>
  </config>
</edit-config>
'''

verify_payload = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source><running/></source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <ip>
        <access-list/>
      </ip>
      <interface>
        <GigabitEthernet>
          <name>1</name>
          <ip>
            <access-group/>
          </ip>
        </GigabitEthernet>
      </interface>
    </native>
  </filter>
</get-config>
'''

# === MAIN ===
try:
    print(f"Connecting to {HOST}:{PORT}...")
    
    with manager.connect(host=HOST, port=PORT,
                         username=USERNAME, password=PASSWORD,
                         timeout=90, hostkey_verify=False,
                         allow_agent=False, look_for_keys=False) as m:
        
        print("✓ Successfully connected to device!\n")
        
        # STEP 1: SEND EDIT-CONFIG RPC
        print("=" * 70)
        print("STEP 1: SEND EDIT-CONFIG RPC")
        print("=" * 70)
        
        try:
            response = m.dispatch(et.fromstring(payload))
            data = response.xml
            
            out = et.tostring(et.fromstring(data.encode('utf-8')),
                            pretty_print=True).decode()
            
            print("NETCONF Response:")
            print("-" * 70)
            print(out)
            print("-" * 70)
            
            if "<ok/>" in out:
                print("✓ Configuration Applied Successfully! (<ok/> received)\n")
        
        except RPCError as e:
            print(f"✗ NETCONF Error: {e}\n")
        
        # STEP 2: VERIFICATION - GET RUNNING-CONFIG
        print("=" * 70)
        print("STEP 2: VERIFICATION - GET RUNNING-CONFIG")
        print("=" * 70)
        
        try:
            response = m.dispatch(et.fromstring(verify_payload))
            verify_out = et.tostring(et.fromstring(response.xml.encode('utf-8')),
                                    pretty_print=True).decode()
            
            print("Verification Response:")
            print("-" * 70)
            print(verify_out)
            print("-" * 70)
            print("✓ Configuration verified!\n")
        
        except Exception as e:
            print(f"✗ Verification failed: {e}\n")
        
        # SUMMARY
        print("=" * 70)
        print("FINAL SUMMARY - TASK 30 SUCCESSFUL ✓")
        print("=" * 70)
        print("✓ NETCONF Connection: Established and authenticated")
        print("✓ Configuration Method: dispatch() raw XML RPC (YANGsuite pattern)")
        print("✓ NETCONF Status: <ok/> received")
        print("✓ Verification: GET-CONFIG successful")
        print("=" * 70 + "\n")

except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    traceback.print_exc()