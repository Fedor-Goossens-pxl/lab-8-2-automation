#!/usr/bin/env python3
"""
Task 9: Configure NTP Server (NETCONF/YANG)
Configureer een NTP server op de router via NETCONF.

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Juni 2026
Course: Enterprise Networks 2 - PXL Hogeschool
"""

from ncclient import manager
from lxml import etree as ET

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient       - NETCONF client library")
print("✓ lxml.etree     - XML parsing and pretty-printing")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"
NTP_SERVER = "193.190.230.65"

# ============================================================
# NETCONF XML Payload - NTP Server Configuration (CORRECT!)
# ============================================================
NTP_CONFIG = """<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ntp>
      <server>
        <server-list>
          <ip-address>{}</ip-address>
        </server-list>
      </server>
    </ntp>
  </native>
</config>""".format(NTP_SERVER)

# Verification filter
NTP_FILTER = """<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ntp/>
  </native>
</filter>"""


def pretty_print(xml_string):
    """Pretty print XML."""
    try:
        root = ET.fromstring(xml_string.encode() if isinstance(xml_string, str) else xml_string)
        return ET.tostring(root, pretty_print=True, encoding='unicode')
    except:
        return xml_string


def main():
    print("=" * 70)
    print("TASK 9: CONFIGURE NTP SERVER (VIA NETCONF/YANG)")
    print("=" * 70)
    print(f"Device: {DEVICE_IP}:{DEVICE_PORT}")
    print(f"NTP Server: {NTP_SERVER}")
    print("=" * 70 + "\n")

    try:
        # ============================================================
        # STEP 1: Connect to device
        # ============================================================
        print("[1] Connecting to device...")
        mgr = manager.connect(
            host=DEVICE_IP,
            port=DEVICE_PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
            device_params={'name': 'iosxe'},
            timeout=30,
            allow_agent=False,
            look_for_keys=False
        )
        print("✓ Connected!\n")

        # ============================================================
        # STEP 2: Configure NTP Server
        # ============================================================
        print("[2] Configuring NTP Server {}...".format(NTP_SERVER))
        print("-" * 70)
        
        response = mgr.edit_config(
            target='running',
            config=NTP_CONFIG,
            default_operation='merge'
        )
        
        if '<ok/>' in response.xml:
            print("✓ NTP Server configured successfully!")
            print("Response: {}\n".format(response.xml))
        else:
            print("⚠ Response received:")
            print(response.xml)
            print()

        # ============================================================
        # STEP 3: Verify Configuration
        # ============================================================
        print("[3] Verifying NTP Configuration...")
        print("-" * 70)
        
        verify_resp = mgr.get_config('running', NTP_FILTER)
        
        print("NTP Configuration on device:")
        print(pretty_print(verify_resp.xml))
        
        if NTP_SERVER in verify_resp.xml:
            print("✓ NTP Server {} found in configuration!\n".format(NTP_SERVER))
        else:
            print("⚠ NTP Server not clearly visible\n")

        # ============================================================
        # FINAL SUMMARY
        # ============================================================
        print("=" * 70)
        print("TASK 9 SUMMARY")
        print("=" * 70)
        print("✓ NETCONF Connection: Established")
        print("✓ Configuration Method: edit-config (running datastore, merge)")
        print("✓ NTP Server: {}".format(NTP_SERVER))
        print("✓ Verification: GET-CONFIG executed")
        print("=" * 70)
        print("\n💡 To verify on device: ssh cisco@{} -> show run | include ntp\n".format(DEVICE_IP))

        mgr.close_session()

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()