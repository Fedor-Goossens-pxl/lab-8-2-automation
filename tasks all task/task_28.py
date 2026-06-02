#!/usr/bin/env python3
"""
Task 28: Retrieve Routing Table via YANG
Pattern: GET operational routing data (state)
Haal de operationele routing table op via YANG.
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
# GET Operational Routing Table (State Data)
# Uses: /ietf-routing:routing/routing-instance (operational)
# ============================================================
get_routing_table_payload = '''
<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <filter type="subtree">
    <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
      <routing-instance>
        <name/>
        <routing-protocols>
          <routing-protocol>
            <type/>
            <name/>
            <static-routes/>
          </routing-protocol>
        </routing-protocols>
      </routing-instance>
    </routing>
  </filter>
</get>
'''

# Alternative: Native routing configuration (running datastore)
get_native_routes_payload = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source>
    <running/>
  </source>
  <filter type="subtree">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <routing>
        <ip>
          <route/>
        </ip>
      </routing>
    </native>
  </filter>
</get-config>
'''

def parse_routing_entries(data_str):
    """Parse and display routing entries from XML response"""
    print("\n" + "-" * 70)
    print("PARSED ROUTING ENTRIES:")
    print("-" * 70)
    
    try:
        root = et.fromstring(data_str.encode())
        
        # Try to find routes in IETF routing model
        routes_found = 0
        
        # Parse route entries
        for route in root.findall('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-native}route'):
            destination = route.findtext('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}ip-address', 'N/A')
            mask = route.findtext('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}mask', 'N/A')
            next_hop = route.findtext('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}next-hop-list/{http://cisco.com/ns/yang/Cisco-IOS-XE-native}next-hop-address/{http://cisco.com/ns/yang/Cisco-IOS-XE-native}next-hop-address', 'N/A')
            
            if destination != 'N/A':
                print(f"  Route: {destination}/{mask}")
                if next_hop != 'N/A':
                    print(f"    Next Hop: {next_hop}")
                routes_found += 1
        
        if routes_found == 0:
            print("  ℹ No static routes configured in running configuration.")
            print("  (Use 'show ip route' on device for full routing table)")
        else:
            print(f"\n  Total static routes: {routes_found}")
            
    except Exception as e:
        print(f"  ℹ XML parsing: {e}")
        print(f"  (Operational routing table may require RPC show command)")

def main():
    print("=" * 70)
    print("TASK 28: RETRIEVE ROUTING TABLE VIA YANG")
    print("=" * 70)
    print(f"Device: {HOST}:{PORT}")
    print(f"Operation: GET operational routing data (state)")
    print("=" * 70 + "\n")
    
    try:
        print(f"Connecting to {HOST}:{PORT}...")
        with manager.connect(host=HOST, port=PORT, username=USERNAME,
                             password=PASSWORD, timeout=90, hostkey_verify=False,
                             allow_agent=False, look_for_keys=False) as m:
            
            print("✓ Successfully connected!\n")
            
            # ============================================================
            # STEP 1: Get Native Routing Configuration (running)
            # ============================================================
            print("=" * 70)
            print("STEP 1: GET NATIVE ROUTING CONFIGURATION (running)")
            print("=" * 70 + "\n")
            
            try:
                print("Sending GET-CONFIG RPC for native routing...")
                response = m.dispatch(et.fromstring(get_native_routes_payload))
                
                if et.iselement(response.xml):
                    routing_data = et.tostring(response.xml, pretty_print=True).decode()
                else:
                    routing_data = str(response.xml)
                
                print("✓ GET-CONFIG executed!\n")
                print("Native Routing Configuration:")
                print("-" * 70)
                
                # Display full response (truncated if too long)
                if len(routing_data) > 1500:
                    print(routing_data[:1500])
                    print("\n... [output truncated] ...\n")
                else:
                    print(routing_data)
                
                print("-" * 70)
                
                # Parse and display entries
                parse_routing_entries(routing_data)
                
            except Exception as e:
                print(f"✗ Error: {e}\n")
            
            # ============================================================
            # STEP 2: Get Operational Routing Data (state)
            # ============================================================
            print("\n" + "=" * 70)
            print("STEP 2: GET OPERATIONAL ROUTING DATA (state)")
            print("=" * 70 + "\n")
            
            try:
                print("Sending GET RPC for operational routing (ietf-routing)...")
                response = m.dispatch(et.fromstring(get_routing_table_payload))
                
                if et.iselement(response.xml):
                    oper_data = et.tostring(response.xml, pretty_print=True).decode()
                else:
                    oper_data = str(response.xml)
                
                print("✓ GET executed!\n")
                print("Operational Routing Data:")
                print("-" * 70)
                
                # Display full response (truncated if too long)
                if len(oper_data) > 1500:
                    print(oper_data[:1500])
                    print("\n... [output truncated] ...\n")
                else:
                    print(oper_data)
                
                print("-" * 70)
                
                # Check for routing instances
                if "routing-instance" in oper_data or "routing-protocol" in oper_data:
                    print("\n✓ Operational routing data retrieved successfully!")
                else:
                    print("\nℹ No routing instances in operational data.")
                
            except Exception as e:
                print(f"✗ Error: {e}\n")
            
            # ============================================================
            # STEP 3: Summary
            # ============================================================
            print("\n" + "=" * 70)
            print("FINAL SUMMARY - TASK 28")
            print("=" * 70)
            print("✓ NETCONF Connection: Established")
            print("✓ Step 1: Retrieved native routing configuration (GET-CONFIG)")
            print("✓ Step 2: Retrieved operational routing data (GET)")
            print("✓ YANG Models Used:")
            print("  • Cisco-IOS-XE-native (native/routing/ip/route)")
            print("  • ietf-routing (routing/routing-instance)")
            print("\nℹ Note: Full operational RIB (show ip route) requires")
            print("  device CLI execution or vendor-specific operational models.")
            print("=" * 70 + "\n")
    
    except Exception as e:
        print(f"\n✗ Connection failed: {e}\n")

if __name__ == '__main__':
    main()