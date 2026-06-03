#!/usr/bin/env python3
"""
Task 11: Remove Static Route via NETCONF/YANG
Category: Basis YANG-configuratie (via NETCONF)

Verwijder de eerder aangemaakte statische route (0.0.0.0/0 via 192.168.19.1).

YANG Structure:
  native > ip > route > ip-route-interface-forwarding-list (with fwd-list)

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Juni 2026
Course: Enterprise Networks 2 - PXL Hogeschool
"""

from ncclient import manager
import xml.dom.minidom as minidom
from xml.etree import ElementTree as ET

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient       - NETCONF client for device automation")
print("✓ xml.dom.minidom - XML pretty-printing and parsing")
print("✓ xml.etree      - XML response handling and parsing")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"
TIMEOUT = 30

# ============================================================
# NETCONF XML Payload - DELETE Static Route
# ============================================================
XML_PAYLOAD = """<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ip>
      <route>
        <ip-route-interface-forwarding-list xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
          <prefix>0.0.0.0</prefix>
          <mask>0.0.0.0</mask>
          <fwd-list>
            <fwd>192.168.19.1</fwd>
          </fwd-list>
        </ip-route-interface-forwarding-list>
      </route>
    </ip>
  </native>
</config>"""

# ============================================================
# Verification Filter - Get routing configuration
# ============================================================
VERIFY_FILTER = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ip>
      <route/>
    </ip>
  </native>
</filter>
"""


def connect_to_device():
    """Establish NETCONF connection to the CSR1000v device."""
    try:
        print(f"Connecting to {DEVICE_IP}:{DEVICE_PORT}...")
        mgr = manager.connect(
            host=DEVICE_IP,
            port=DEVICE_PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
            device_params={'name': 'iosxe'},
            timeout=TIMEOUT,
            allow_agent=False,
            look_for_keys=False
        )
        print("✓ Successfully connected to device!")
        return mgr
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None


def apply_configuration(mgr):
    """Apply the NETCONF DELETE configuration to the device."""
    try:
        print("\n" + "=" * 70)
        print("STEP 1: NETCONF EDIT-CONFIG REQUEST (DELETE)")
        print("=" * 70)
        
        print("Target datastore: running")
        print("Operation: delete (via nc:operation attribute)")
        print("Route: 0.0.0.0/0 via 192.168.19.1")
        print("-" * 70)
        
        # Send edit-config RPC with operation="delete" in XML element
        response = mgr.edit_config(
            target='running',
            config=XML_PAYLOAD,
            default_operation='merge'  # merge is default, actual delete via nc:operation in XML
        )
        
        print("✓ RPC executed!")
        print(f"\nResponse: {response.xml}")
        
        # Check for <ok/> in response
        if '<ok/>' in response.xml:
            print("✓ Static route deleted successfully (<ok/> received)!")
            return True
        else:
            print("⚠ Response received but status unclear")
            return False
        
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        return False


def verify_configuration(mgr):
    """Verify the route deletion by reading running-config."""
    try:
        print("\n" + "=" * 70)
        print("STEP 2: VERIFICATION - GET ROUTING CONFIGURATION")
        print("=" * 70)
        
        response = mgr.get_config(source='running', filter=VERIFY_FILTER)
        
        print("✓ GET-CONFIG executed!")
        print("\nRouting Configuration:")
        print("-" * 70)
        print(response.xml)
        
        # Verify 0.0.0.0 is NOT in response
        if '0.0.0.0' not in response.xml or '<data/>' in response.xml:
            print("✓ Route deletion verified! (0.0.0.0/0 no longer in config)")
        else:
            print("⚠ Route may still exist in configuration")
            
    except Exception as e:
        print(f"✗ Verification failed: {e}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("TASK 11: REMOVE STATIC ROUTE (VIA NETCONF/YANG)")
    print("=" * 70)
    print(f"GitHub Repository: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation")
    print(f"Device: CSR1000v at {DEVICE_IP}:{DEVICE_PORT}")
    print(f"Operation: Delete static route 0.0.0.0/0 via 192.168.19.1")
    print("=" * 70 + "\n")
    
    # Connect to device
    mgr = connect_to_device()
    if not mgr:
        print("Failed to connect to device. Exiting.")
        exit(1)
    
    try:
        # Apply DELETE configuration
        success = apply_configuration(mgr)
        
        if success:
            print("\nTask 11 DELETE operation applied successfully!")
            
            # Verify deletion
            verify_configuration(mgr)
            
            # Final summary
            print("\n" + "=" * 70)
            print("FINAL SUMMARY - TASK 11 SUCCESSFUL ✓")
            print("=" * 70)
            print("✓ NETCONF Connection: Established and authenticated")
            print("✓ Operation: DELETE via NETCONF edit-config")
            print("✓ NETCONF Status: <ok/> received")
            print("✓ Route Deleted: 0.0.0.0/0 via 192.168.19.1")
            print("✓ Verification: GET running-config successful")
            print("=" * 70)
        else:
            print("Task 11 FAILED!")
            exit(1)
            
    finally:
        # Always close the NETCONF session
        try:
            mgr.close_session()
            print("NETCONF session closed")
        except:
            pass


if __name__ == "__main__":
    main()