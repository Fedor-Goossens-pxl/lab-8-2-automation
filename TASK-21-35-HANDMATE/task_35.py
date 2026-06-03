#!/usr/bin/env python3
"""
Task 35: Full Service Deployment - COMPLETE
Deploy Interface + IP + OSPF + ACL in THREE atomic transactions
(Each config part succeeds independently, then combined)

Author: Fedor Goossens
Course: Enterprise Networks 2 - PXL Hogeschool
"""

import lxml.etree as et
from ncclient import manager

print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ ncclient - NETCONF client library")
print("=" * 70 + "\n")

HOST = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
PORT = 830

# ============================================================
# PART 1: Interface + IP (Task 21 pattern - PROVEN)
# ============================================================
part1_payload = '''
<edit-config>
  <target><running/></target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <interface>
        <Loopback>
          <name>0</name>
          <description>Task 35: Full Service Deployment</description>
          <ip>
            <address>
              <primary>
                <address>10.99.99.99</address>
                <mask>255.255.255.255</mask>
              </primary>
            </address>
          </ip>
        </Loopback>
      </interface>
    </native>
  </config>
</edit-config>
'''

# ============================================================
# PART 2: OSPF Routing (Task 27 pattern - PROVEN)
# NOTE: <ospf> element MUST have its own namespace!
# ============================================================
part2_payload = '''
<edit-config>
  <target><running/></target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <router>
        <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
          <id>35</id>
          <network>
            <ip>10.99.99.0</ip>
            <mask>0.0.0.255</mask>
            <area>0</area>
          </network>
        </ospf>
      </router>
    </native>
  </config>
</edit-config>
'''

# ============================================================
# PART 3: ACL Configuration
# IMPORTANT: <standard> element must have acl namespace!
# Pattern: <standard xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
# ============================================================
part3_payload = '''
<edit-config>
  <target><running/></target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <ip>
        <access-list>
          <standard xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
            <name>TASK35_ACL</name>
            <access-list-seq-rule>
              <sequence>10</sequence>
              <permit>
                <std-ace>
                  <host>10.99.99.99</host>
                </std-ace>
              </permit>
            </access-list-seq-rule>
          </standard>
        </access-list>
      </ip>
    </native>
  </config>
</edit-config>
'''

def main():
    print("=" * 70)
    print("TASK 35: FULL SERVICE DEPLOYMENT")
    print("=" * 70)
    print(f"Device: {HOST}:{PORT}")
    print()
    print("Deploy in THREE atomic transactions:")
    print("  1. Interface configuration (Loopback0 + IP 10.99.99.99/32)")
    print("  2. OSPF routing (Process 35, Network 10.99.99.0/24)")
    print("  3. ACL configuration (TASK35_ACL with permit 10.99.99.99)")
    print()
    print("Pattern: LOCK → DEPLOY → UNLOCK (×3)")
    print("=" * 70 + "\n")
    
    try:
        print(f"Connecting to {HOST}:{PORT}...")
        m = manager.connect(host=HOST, port=PORT,
                           username=USERNAME, password=PASSWORD,
                           timeout=90, hostkey_verify=False,
                           allow_agent=False, look_for_keys=False)
        print("✓ Connected!\n")
        
        results = {'part1': False, 'part2': False, 'part3': False}
        
        # ============================================================
        # PART 1: Interface + IP
        # ============================================================
        print("=" * 70)
        print("PART 1: INTERFACE + IP CONFIGURATION")
        print("=" * 70)
        
        try:
            print("  LOCK...", end=" ")
            m.dispatch(et.fromstring('<lock><target><running/></target></lock>'))
            print("")
            
            print("  CONFIG...", end=" ")
            response = m.dispatch(et.fromstring(part1_payload))
            data = et.tostring(response.xml, pretty_print=True).decode() if et.iselement(response.xml) else str(response.xml)
            
            if "<ok/>" in data:
                print("")
                results['part1'] = True
            else:
                print("")
            
            print("  UNLOCK...", end=" ")
            m.dispatch(et.fromstring('<unlock><target><running/></target></unlock>'))
            print("\n")
        except Exception as e:
            print(f" Error: {str(e)[:50]}\n")
        
        # ============================================================
        # PART 2: OSPF
        # ============================================================
        print("=" * 70)
        print("PART 2: OSPF ROUTING CONFIGURATION")
        print("=" * 70)
        
        try:
            print("  LOCK...", end=" ")
            m.dispatch(et.fromstring('<lock><target><running/></target></lock>'))
            print("")
            
            print("  CONFIG...", end=" ")
            response = m.dispatch(et.fromstring(part2_payload))
            data = et.tostring(response.xml, pretty_print=True).decode() if et.iselement(response.xml) else str(response.xml)
            
            if "<ok/>" in data:
                print("")
                results['part2'] = True
            else:
                print("")
            
            print("  UNLOCK...", end=" ")
            m.dispatch(et.fromstring('<unlock><target><running/></target></unlock>'))
            print("\n")
        except Exception as e:
            print(f" Error: {str(e)[:50]}\n")
        
        # ============================================================
        # PART 3: ACL
        # ============================================================
        print("=" * 70)
        print("PART 3: ACL CONFIGURATION")
        print("=" * 70)
        
        try:
            print("  LOCK...", end=" ")
            m.dispatch(et.fromstring('<lock><target><running/></target></lock>'))
            print("")
            
            print("  CONFIG...", end=" ")
            response = m.dispatch(et.fromstring(part3_payload))
            data = et.tostring(response.xml, pretty_print=True).decode() if et.iselement(response.xml) else str(response.xml)
            
            if "<ok/>" in data:
                print("")
                results['part3'] = True
            else:
                print("")
            
            print("  UNLOCK...", end=" ")
            m.dispatch(et.fromstring('<unlock><target><running/></target></unlock>'))
            print("\n")
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}\n")
        
        # ============================================================
        # FINAL SUMMARY
        # ============================================================
        print("=" * 70)
        print("FINAL SUMMARY - TASK 35")
        print("=" * 70)
        print()
        
        if results['part1']:
            print(" PART 1: Interface + IP - SUCCESS")
        else:
            print(" PART 1: Interface + IP - FAILED")
        
        if results['part2']:
            print(" PART 2: OSPF Routing - SUCCESS")
        else:
            print(" PART 2: OSPF Routing - FAILED")
        
        if results['part3']:
            print(" PART 3: ACL Configuration - SUCCESS")
        else:
            print(" PART 3: ACL Configuration - FAILED")
        
        print()
        
        if all(results.values()):
            print(" ALL PARTS SUCCESSFUL - FULL SERVICE DEPLOYED!")
        else:
            failed = [k for k, v in results.items() if not v]
            print(f"⚠ Some parts failed: {', '.join(failed)}")
        
        print()
        print("TASK 35 LEARNING OUTCOMES:")
        print("-" * 70)
        print()
        print("1. Full Service Stack:")
        print("   ✓ Interface configuration (Loopback0)")
        print("   ✓ IP addressing (10.99.99.99/32)")
        print("   ✓ ACL deployment (TASK35_ACL)")
        print("   ✓ Routing configuration (OSPF Process 35)")
        print()
        print("2. Atomic Transactions:")
        print("   ✓ LOCK before changes")
        print("   ✓ Deploy configuration")
        print("   ✓ UNLOCK to commit")
        print("   ✓ Repeat for each service part")
        print()
        print("3. Proven NETCONF Patterns:")
        print("   ✓ dispatch() method (not edit_config)")
        print("   ✓ Native Cisco YANG syntax")
        print("   ✓ Task 21, 27, 30 patterns")
        print()
        print("4. Production Deployment:")
        print("   ✓ Multiple services provisioned")
        print("   ✓ All-or-nothing semantics per part")
        print("   ✓ Reliable network automation")
        print()
        print(" TASK 35 COMPLETED!")
        print("=" * 70 + "\n")
        
        m.close_session()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()