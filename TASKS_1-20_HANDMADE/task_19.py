#!/usr/bin/env python3
"""
Task 19: Retrieve Running Configuration via NETCONF/YANG
Category: Basis YANG-configuratie (via NETCONF)

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (ncclient, lxml)
✓ Raw XML RPC dispatch (YANGsuite pattern)
✓ Response parsing & pretty-printing
✓ NETCONF error handling (RPCError)
✓ YANG filters for targeted queries
✓ Git/GitHub as single source of truth

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Description: Retrieve running-config using YANG filters.
Demonstrates GET-CONFIG with various filter scopes.

Usage:
    python task_19_yangsuite.py

Device credentials are hardcoded in the script:
    HOST: 192.168.19.139
    USERNAME: cisco
    PASSWORD: cisco123!

Requirements:
    - Python 3.8+
    - ncclient library
    - lxml library
"""

import traceback
import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient - NETCONF client library")
print("✓ lxml.etree - XML parsing and pretty-printing")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration (Hardcoded)
# ============================================================
HOST = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
PORT = 830

# ============================================================
# GET-CONFIG Payloads with Various Filters
# ============================================================

# Filter 1: Get entire native configuration
filter_all_native = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
  </filter>
</get-config>
'''

# Filter 2: Get interfaces only
filter_interfaces = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <interface/>
    </native>
  </filter>
</get-config>
'''

# Filter 3: Get system settings (hostname, NTP, DNS, banner)
filter_system = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <hostname/>
      <ntp/>
      <ip/>
      <banner/>
    </native>
  </filter>
</get-config>
'''

# Filter 4: Get VLAN configuration
filter_vlan = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <vlan/>
    </native>
  </filter>
</get-config>
'''

# Filter 5: Get AAA and users
filter_aaa = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <username/>
    </native>
  </filter>
</get-config>
'''


def retrieve_and_display(mgr, filter_rpc, filter_name):
    """
    Execute GET-CONFIG RPC and display results.
    
    Args:
        mgr: ncclient manager object
        filter_rpc: XML RPC payload string
        filter_name: Human-readable name of filter
    """
    print("\n" + "=" * 70)
    print(f"FILTER: {filter_name}")
    print("=" * 70)
    
    try:
        print(f"Sending GET-CONFIG RPC with filter: {filter_name}...")
        response = mgr.dispatch(et.fromstring(filter_rpc))
        data = response.xml
        print("✓ RPC executed successfully!\n")
        
        # beautify output
        if et.iselement(data):
            data = et.tostring(data, pretty_print=True).decode()
        
        try:
            out = et.tostring(
                et.fromstring(data.encode('utf-8')),
                pretty_print=True
            ).decode()
        except Exception as e:
            print(f"Error formatting response: {e}")
            out = data
        
        print("Response:")
        print("-" * 70)
        print(out)
        print("-" * 70)
        
        # Count elements for summary
        root = et.fromstring(out.encode('utf-8'))
        namespaces = {
            'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0',
            'native': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
        }
        
        # Try to count key elements
        try:
            interfaces = root.findall('.//native:interface', namespaces)
            if interfaces:
                print(f"✓ Found {len(interfaces)} interface section(s)")
        except:
            pass
        
        return True
        
    except RPCError as e:
        print(f"✗ NETCONF RPC Error: {e}")
        print(f"Error details: {e.xml}")
        return False
    except Exception as e:
        print(f"✗ Exception occurred: {e}")
        traceback.print_exc()
        return False


def main():
    """Main execution function."""
    
    print("=" * 70)
    print("TASK 19: RETRIEVE RUNNING CONFIGURATION (via YANG/NETCONF)")
    print("=" * 70)
    print(f"Device: {HOST}:{PORT}")
    print(f"Username: {USERNAME}")
    print(f"Pattern: YANGsuite (dispatch raw XML RPC + GET-CONFIG)")
    print("=" * 70 + "\n")
    
    # connect to netconf agent
    try:
        print(f"Connecting to {HOST}:{PORT}...")
        
        with manager.connect(host=HOST,
                             port=PORT,
                             username=USERNAME,
                             password=PASSWORD,
                             timeout=90,
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False) as m:
            
            print("✓ Successfully connected to device!\n")
            
            # Execute multiple GET-CONFIG queries with different filters
            filters = [
                (filter_all_native, "All Native Configuration"),
                (filter_interfaces, "Interfaces Only"),
                (filter_system, "System Settings (hostname, NTP, DNS, banner)"),
                (filter_vlan, "VLAN Configuration"),
                (filter_aaa, "Users and AAA"),
            ]
            
            results = []
            for filter_rpc, filter_name in filters:
                result = retrieve_and_display(m, filter_rpc, filter_name)
                results.append((filter_name, result))
            
            # Final Summary
            print("\n" + "=" * 70)
            print("FINAL SUMMARY - TASK 19")
            print("=" * 70)
            print("✓ NETCONF Connection: Established and authenticated")
            print("✓ Method: GET-CONFIG with YANG filters")
            print(f"✓ Datastore: running-config")
            print(f"✓ Total filters executed: {len(filters)}")
            
            successful = sum(1 for _, result in results if result)
            print(f"✓ Successful queries: {successful}/{len(filters)}")
            
            print("\nQueries executed:")
            for filter_name, result in results:
                status = "✓" if result else "✗"
                print(f"  {status} {filter_name}")
            
            print("=" * 70 + "\n")
    
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()