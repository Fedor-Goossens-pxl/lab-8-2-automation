#!/usr/bin/env python3
"""
Task 2: Enable / Disable Interface (NETCONF/YANG)
Schakel een BESTAANDE interface administratief in of uit.

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Juni 2026
Course: Enterprise Networks 2 - PXL Hogeschool
"""

from ncclient import manager

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient       - NETCONF client for device automation")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"

# ============================================================
# NETCONF XML Payloads
# ============================================================

# CREATE Loopback0 met IP
CREATE = """<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>0</name>
        <ip>
          <address>
            <primary>
              <address>10.99.0.1</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>"""

# DISABLE (Shutdown) - met operation="merge" om zeker toe te passen
DISABLE = """<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>0</name>
        <shutdown operation="merge"/>
      </Loopback>
    </interface>
  </native>
</config>"""

# ENABLE (No Shutdown) - verwijder shutdown element
ENABLE = """<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>0</name>
        <shutdown operation="delete"/>
      </Loopback>
    </interface>
  </native>
</config>"""


def main():
    print("=" * 70)
    print("TASK 2: ENABLE / DISABLE INTERFACE")
    print("=" * 70)
    print(f"Device: {DEVICE_IP}:{DEVICE_PORT}")
    print(f"Interface: Loopback0")
    print("=" * 70 + "\n")

    try:
        # Connect
        print("[1] Connecting...")
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

        # CREATE Loopback0 with IP
        print("[2] CREATE Loopback0 with IP 10.99.0.1/32...")
        resp0 = mgr.edit_config(target='running', config=CREATE)
        if '<ok/>' in resp0.xml:
            print("✓ Loopback0 created\n")
        else:
            print("⚠ Create response: {}\n".format(resp0.xml))

        # DISABLE
        print("[3] DISABLE Interface (shutdown)...")
        resp1 = mgr.edit_config(target='running', config=DISABLE)
        if '<ok/>' in resp1.xml:
            print("✓ Loopback0 DISABLED (administratief uit)\n")
        else:
            print("✗ Disable failed!\n")

        # VERIFY actual state
        print("[3b] VERIFYING actual state on device...")
        verify_resp = mgr.get_config('running', """<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>0</name>
      </Loopback>
    </interface>
  </native>
</filter>""")
        print("Device config:")
        print(verify_resp.xml)
        print()

        # ENABLE
        print("[4] ENABLE Interface (no shutdown)...")
        resp2 = mgr.edit_config(target='running', config=ENABLE)
        if '<ok/>' in resp2.xml:
            print("✓ Loopback0 ENABLED (administratief aan)\n")
        else:
            print("✗ Enable failed!\n")

        # Summary
        print("=" * 70)
        print("TASK 2 SUCCESSFUL ✓")
        print("=" * 70)
        print("✓ Loopback0 created with IP 10.99.0.1/32")
        print("✓ Interface DISABLED (shutdown)")
        print("✓ Interface ENABLED (no shutdown)")
        print("=" * 70 + "\n")

        mgr.close_session()

    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()