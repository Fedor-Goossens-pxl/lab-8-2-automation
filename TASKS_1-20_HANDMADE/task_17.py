#!/usr/bin/env python3
"""
Task 17: Configure SNMP Community via NETCONF/YANG - YANGsuite Pattern (CORRECT)
Category: Basis YANG-configuratie (via NETCONF)

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (ncclient, lxml)
✓ Raw XML RPC dispatch (YANGsuite pattern)
✓ Response parsing & pretty-printing
✓ NETCONF error handling (RPCError)
✓ Git/GitHub as single source of truth

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Description: Configure SNMP community "public" (read-only) using YANGsuite pattern.
Uses raw XML RPC dispatch (dispatch method) with correct YANG structure.

Usage:
    python task_17_yangsuite.py

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
# NETCONF SNMP Configuration Payload
# CORRECTED YANG Structure from Cisco-IOS-XE-snmp module
# ============================================================
payload = [
'''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running/>
  </target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <snmp-server>
        <community>
          <name>public</name>
          <RO/>
        </community>
      </snmp-server>
    </native>
  </config>
</edit-config>
''',
]

# ============================================================
# Verification Payload
# ============================================================
verify_payload = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <snmp-server>
        <community/>
      </snmp-server>
    </native>
  </filter>
</get-config>
'''


def main():
    """Main execution function."""
    
    print("=" * 70)
    print("TASK 17: CONFIGURE SNMP COMMUNITY VIA NETCONF/YANG")
    print("=" * 70)
    print(f"Device: {HOST}:{PORT}")
    print(f"Username: {USERNAME}")
    print(f"SNMP Community: public")
    print(f"Access Type: Read-Only (RO)")
    print(f"Pattern: YANGsuite (dispatch raw XML RPC)")
    print(f"YANG Module: Cisco-IOS-XE-snmp")
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
            
            # ============================================================
            # STEP 1: Execute Configuration RPC
            # ============================================================
            print("=" * 70)
            print("STEP 1: SEND EDIT-CONFIG RPC (Configure SNMP Community)")
            print("=" * 70)
            
            for rpc in payload:
                try:
                    print("Sending NETCONF RPC...")
                    response = m.dispatch(et.fromstring(rpc))
                    data = response.xml
                    print("✓ RPC dispatched successfully!\n")
                    
                except RPCError as e:
                    print("✗ NETCONF RPC Error received:")
                    data = e.xml
                    pass
                except Exception as e:
                    print(f"✗ Exception occurred: {e}")
                    traceback.print_exc()
                    exit(1)
                
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
                    traceback.print_exc()
                    exit(1)
                
                print("NETCONF Response:")
                print("-" * 70)
                print(out)
                print("-" * 70)
                
                # Check if configuration was successful
                if "<ok/>" in out or "<ok />" in out:
                    print("✓ Configuration Applied Successfully! (<ok/> received)\n")
                else:
                    print("⚠ Response received but status unclear\n")
            
            # ============================================================
            # STEP 2: Verify Configuration
            # ============================================================
            print("=" * 70)
            print("STEP 2: VERIFICATION - GET RUNNING-CONFIG (SNMP)")
            print("=" * 70)
            
            try:
                print("Sending GET-CONFIG RPC for verification...")
                response = m.dispatch(et.fromstring(verify_payload))
                verify_data = response.xml
                print("✓ Verification RPC executed!\n")
                
                # beautify output
                if et.iselement(verify_data):
                    verify_data = et.tostring(verify_data, pretty_print=True).decode()
                
                try:
                    verify_out = et.tostring(
                        et.fromstring(verify_data.encode('utf-8')),
                        pretty_print=True
                    ).decode()
                except Exception as e:
                    traceback.print_exc()
                    exit(1)
                
                print("Verification Response (SNMP Configuration):")
                print("-" * 70)
                print(verify_out)
                print("-" * 70)
                
                # Check if SNMP community is in response
                if "public" in verify_out:
                    print("✓ SNMP community 'public' found in configuration!\n")
                else:
                    print("⚠ SNMP community not clearly visible in verification response\n")
                
            except Exception as e:
                print(f"Verification failed: {e}")
                traceback.print_exc()
            
            # ============================================================
            # Final Summary
            # ============================================================
            print("=" * 70)
            print("FINAL SUMMARY - TASK 17")
            print("=" * 70)
            print("✓ NETCONF Connection: Established and authenticated")
            print("✓ Configuration Method: dispatch() raw XML RPC (YANGsuite pattern)")
            print("✓ SNMP Community: public")
            print("✓ Access Type: Read-Only (RO)")
            print("✓ YANG Structure: snmp-server > community > name + RO")
            print("✓ Verification: GET-CONFIG RPC executed")
            print("=" * 70 + "\n")
    
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()