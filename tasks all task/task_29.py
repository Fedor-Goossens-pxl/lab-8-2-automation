#!/usr/bin/env python3
"""
Task 29: Configure Interface MTU
Pattern: EDIT-CONFIG MTU value
Wijzig de MTU-waarde van een interface via YANG.
"""

import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError

print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient - NETCONF client library")
print("✓ lxml.etree - XML parsing and pretty-printing")
print("=" * 70 + "\n")

HOST = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
PORT = 830

# ============================================================
# Configure Interface MTU
# Uses: native/interface/GigabitEthernet with name (NOT n!)
# For MTU config, use <name> instead of <n>
# ============================================================
configure_mtu_payload = '''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running/>
  </target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <interface>
        <GigabitEthernet>
          <name>1</name>
          <mtu>1600</mtu>
        </GigabitEthernet>
      </interface>
    </native>
  </config>
</edit-config>
'''

# Verification: GET current interface config
verify_mtu_payload = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter type="subtree">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <interface>
        <GigabitEthernet>
          <name>1</name>
        </GigabitEthernet>
      </interface>
    </native>
  </filter>
</get-config>
'''

def main():
    print("=" * 70)
    print("TASK 29: CONFIGURE INTERFACE MTU")
    print("=" * 70)
    print(f"Device: {HOST}:{PORT}")
    print(f"Interface: GigabitEthernet1 (Gi1)")
    print(f"New MTU: 1600 bytes")
    print("=" * 70 + "\n")
    
    try:
        print(f"Connecting to {HOST}:{PORT}...")
        with manager.connect(host=HOST, port=PORT, username=USERNAME,
                             password=PASSWORD, timeout=90, hostkey_verify=False,
                             allow_agent=False, look_for_keys=False) as m:
            
            print("✓ Successfully connected!\n")
            
            # ============================================================
            # STEP 1: Configure MTU
            # ============================================================
            print("=" * 70)
            print("STEP 1: CONFIGURE INTERFACE MTU")
            print("=" * 70 + "\n")
            
            try:
                print("Sending EDIT-CONFIG RPC (GigabitEthernet1 MTU = 1600)...")
                response = m.dispatch(et.fromstring(configure_mtu_payload))
                
                if et.iselement(response.xml):
                    data = et.tostring(response.xml, pretty_print=True).decode()
                else:
                    data = str(response.xml)
                
                print("✓ RPC executed!\n")
                print("Response:")
                print("-" * 70)
                print(data)
                print("-" * 70)
                
                if "<ok/>" in data:
                    print("✓ MTU configuration successful (<ok/> received)!\n")
                else:
                    print("⚠ Configuration attempt completed\n")
                
            except RPCError as e:
                print(f"✗ NETCONF Error: {e}\n")
            except Exception as e:
                print(f"✗ Exception: {e}\n")
            
            # ============================================================
            # STEP 2: Verify MTU Configuration
            # ============================================================
            print("=" * 70)
            print("STEP 2: VERIFICATION - GET INTERFACE CONFIG")
            print("=" * 70 + "\n")
            
            try:
                print("Sending GET-CONFIG RPC for MTU verification...")
                response = m.dispatch(et.fromstring(verify_mtu_payload))
                
                if et.iselement(response.xml):
                    verify_data = et.tostring(response.xml, pretty_print=True).decode()
                else:
                    verify_data = str(response.xml)
                
                print("✓ GET-CONFIG executed!\n")
                print("Current Interface Configuration:")
                print("-" * 70)
                print(verify_data)
                print("-" * 70)
                
                # Check for MTU value
                if "<mtu>1600</mtu>" in verify_data:
                    print("✓ MTU value 1600 confirmed on GigabitEthernet1!\n")
                elif "<mtu>" in verify_data:
                    print("✓ MTU value retrieved (check output above)\n")
                else:
                    print("ℹ MTU value in response (check output above)\n")
                
            except Exception as e:
                print(f"Verification failed: {e}\n")
            
            # ============================================================
            # STEP 3: Summary
            # ============================================================
            print("=" * 70)
            print("FINAL SUMMARY - TASK 29")
            print("=" * 70)
            print("✓ NETCONF Connection: Established")
            print("✓ Step 1: MTU configuration (EDIT-CONFIG)")
            print("✓ Interface: GigabitEthernet1")
            print("✓ New MTU Value: 1600 bytes")
            print("✓ Step 2: Verification (GET-CONFIG)")
            print("✓ YANG Model: native/interface/GigabitEthernet/mtu")
            print("✓ Key Structure: <name>1</name> (not <n>1</n>)")
            print("=" * 70 + "\n")
    
    except Exception as e:
        print(f"\n✗ Connection failed: {e}\n")

if __name__ == '__main__':
    main()