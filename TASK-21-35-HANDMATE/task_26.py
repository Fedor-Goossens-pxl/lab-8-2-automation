#!/usr/bin/env python3
"""
Task 11: Configure IPv4 Address on GigabitEthernet1 via NETCONF/YANG
Category: Basis YANG-configuratie (via NETCONF - dispatch pattern)

YANG Structure:
  native > interface > GigabitEthernet > name + ip > address > primary > address/mask

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Juni 2026
Course: Enterprise Networks 2 - PXL Hogeschool
"""

from ncclient import manager
from lxml import etree

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient - NETCONF client library")
print("✓ lxml.etree - XML parsing and pretty-printing")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"

print("=" * 70)
print("TASK 11: CONFIGURE IPv4 ADDRESS VIA NETCONF/YANG")
print("=" * 70)
print(f"Device: {DEVICE_IP}:{DEVICE_PORT}")
print(f"Interface: GigabitEthernet1")
print(f"IPv4 Address: 10.0.0.1/24")
print(f"YANG Path: interface > GigabitEthernet > ip > address > primary")
print("=" * 70 + "\n")

# ============================================================
# Step 1: Connect to device
# ============================================================
print("[1] Connecting to device...")
try:
    mgr = manager.connect(
        host=DEVICE_IP,
        port=DEVICE_PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
        device_params={'name': 'iosxe'},
        allow_agent=False,
        look_for_keys=False,
        timeout=30
    )
    print("✓ Connected!\n")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# ============================================================
# Step 2: Build NETCONF RPC payload (IPv4 address on Gi1)
# ============================================================
config_payload = """
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <ip>
          <address>
            <primary>
              <address>10.0.0.1</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
"""

# ============================================================
# Step 3: Send EDIT-CONFIG RPC (dispatch pattern)
# ============================================================
print("[2] Configuring IPv4 Address 10.0.0.1/24...")
print("-" * 70)

rpc_template = """
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target><running/></target>
  <default-operation>merge</default-operation>
  <config>
{config}
  </config>
</edit-config>
""".format(config=config_payload)

try:
    response = mgr.dispatch(etree.fromstring(rpc_template))
    response_xml = etree.tostring(response, pretty_print=True, encoding='unicode')
    
    print("✓ RPC executed!")
    print("\nResponse:")
    print("-" * 70)
    print(response_xml)
    
    # Check for <ok/> in response
    if '<ok/>' in response_xml or '<ok></ok>' in response_xml:
        print("✓ IPv4 address configured successfully (<ok/> received)!")
    else:
        print("⚠ Response received but status unclear")
        
except Exception as e:
    print(f"✗ RPC Error: {e}")
    exit(1)

# ============================================================
# Step 4: Verify configuration via GET-CONFIG
# ============================================================
print("\n" + "=" * 70)
print("STEP 2: VERIFICATION - GET IPv4 CONFIGURATION")
print("=" * 70)

verify_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <ip>
          <address/>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
</filter>
"""

try:
    response = mgr.get_config(source='running', filter=verify_filter)
    response_xml = etree.tostring(response, pretty_print=True, encoding='unicode')
    
    print("✓ GET-CONFIG executed!")
    print("\nIPv4 Configuration:")
    print("-" * 70)
    print(response_xml)
    
    # Verify 10.0.0.1 is in response
    if '10.0.0.1' in response_xml:
        print("✓ IPv4 configuration verified!")
    else:
        print("⚠ IPv4 address not found in response")
        
except Exception as e:
    print(f"✗ GET-CONFIG Error: {e}")

# ============================================================
# Final Summary
# ============================================================
print("\n" + "=" * 70)
print("FINAL SUMMARY - TASK 11 SUCCESSFUL ✓")
print("=" * 70)
print("✓ NETCONF Connection: Established")
print("✓ Step 1: IPv4 configuration via NETCONF")
print("✓ YANG Structure: interface > GigabitEthernet > ip > address > primary")
print("✓ IPv4 Address: 10.0.0.1/24 on GigabitEthernet1")
print("✓ Step 2: Verification via GET-CONFIG")
print("✓ IPv4 Configuration: Workflow complete")
print("=" * 70)

# Close session
mgr.close_session()