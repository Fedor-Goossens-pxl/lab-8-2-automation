#!/usr/bin/env python3
"""
Task 33: Retrieve and Analyze YANG Capabilities
Category: NETCONF Capability Discovery

Description: 
  Haal de YANG capabilities op die door CSR1000v ondersteund worden.
  Capabilities worden uitgewisseld tijdens de NETCONF handshake.
  Analyseer en categoriseer ze.

Author: Fedor Goossens
Course: Enterprise Networks 2 - PXL Hogeschool

Usage:
    python task_33_FINAL.py
"""

import traceback
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

def categorize_capabilities(caps):
    """Categorize capabilities for analysis."""
    categories = {
        'NETCONF Base': [],
        'NETCONF Capabilities': [],
        'Cisco Native YANG': [],
        'IETF Standard YANG': [],
        'OpenConfig YANG': [],
        'Tail-f Extensions': [],
        'Other': []
    }
    
    for cap in caps:
        if 'urn:ietf:params:netconf:base' in cap:
            categories['NETCONF Base'].append(cap)
        elif 'urn:ietf:params:netconf:capability' in cap:
            categories['NETCONF Capabilities'].append(cap)
        elif 'http://cisco.com/ns/yang/Cisco-IOS-XE' in cap:
            categories['Cisco Native YANG'].append(cap)
        elif 'urn:ietf:params:xml:ns:yang' in cap:
            categories['IETF Standard YANG'].append(cap)
        elif 'openconfig.net/yang' in cap:
            categories['OpenConfig YANG'].append(cap)
        elif 'tail-f.com' in cap:
            categories['Tail-f Extensions'].append(cap)
        else:
            categories['Other'].append(cap)
    
    return categories

def extract_module_info(cap):
    """Extract module name and revision from capability string."""
    parts = cap.split('?')
    module_part = parts[0]
    
    # Extract module name (last part after /)
    if '/' in module_part:
        module = module_part.split('/')[-1]
    else:
        module = module_part.split('/')[-1] if '/' in module_part else module_part[-20:]
    
    revision = ""
    if len(parts) > 1:
        for param in parts[1].split('&'):
            if 'revision=' in param:
                revision = param.split('=')[1]
                break
    
    return module, revision

def main():
    print("=" * 70)
    print("TASK 33: RETRIEVE AND ANALYZE YANG CAPABILITIES")
    print("=" * 70)
    print(f"Device: {HOST}:{PORT}")
    print()
    print("Workflow:")
    print("  1. Connect to device (NETCONF handshake)")
    print("  2. Retrieve server_capabilities from manager")
    print("  3. Categorize capabilities")
    print("  4. Analyze and display results")
    print("=" * 70 + "\n")
    
    try:
        print(f"Connecting to {HOST}:{PORT}...")
        
        # NETCONF handshake happens automatically
        mgr = manager.connect(
            host=HOST,
            port=PORT,
            username=USERNAME,
            password=PASSWORD,
            timeout=90,
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False
        )
        
        print("✓ Connected!\n")
        
        # ============================================================
        # STEP 1: Retrieve Capabilities
        # ============================================================
        print("=" * 70)
        print("STEP 1: RETRIEVE SERVER CAPABILITIES")
        print("=" * 70)
        print("Capabilities are exchanged during NETCONF <hello> message\n")
        
        # Get all capabilities
        capabilities = list(mgr.server_capabilities)
        
        print(f"Total capabilities: {len(capabilities)}\n")
        
        # ============================================================
        # STEP 2: Categorize Capabilities
        # ============================================================
        print("=" * 70)
        print("STEP 2: CATEGORIZE CAPABILITIES")
        print("=" * 70 + "\n")
        
        categories = categorize_capabilities(capabilities)
        
        for category, caps in categories.items():
            if caps:
                print(f"\n{category} ({len(caps)}):")
                print("-" * 70)
                for i, cap in enumerate(caps[:5], 1):  # Show first 5 of each category
                    # Shorten long capability strings
                    if len(cap) > 90:
                        cap_short = cap[:87] + "..."
                    else:
                        cap_short = cap
                    print(f"  {i}. {cap_short}")
                
                if len(caps) > 5:
                    print(f"  ... and {len(caps) - 5} more")
        
        # ============================================================
        # STEP 3: Analyze Key Capabilities
        # ============================================================
        print("\n" + "=" * 70)
        print("STEP 3: ANALYZE KEY CAPABILITIES")
        print("=" * 70 + "\n")
        
        # Check for critical capabilities
        cap_str = " ".join(capabilities)
        
        checks = {
            'writable-running': 'urn:ietf:params:netconf:capability:writable-running',
            'candidate': 'urn:ietf:params:netconf:capability:candidate',
            'rollback-on-error': 'urn:ietf:params:netconf:capability:rollback-on-error',
            'validate': 'urn:ietf:params:netconf:capability:validate',
            'xpath': 'urn:ietf:params:netconf:capability:xpath',
            'notification': 'urn:ietf:params:netconf:capability:notification',
            'YANG Library': 'urn:ietf:params:netconf:capability:yang-library',
            'Tail-f Actions': 'http://tail-f.com/ns/netconf/actions',
        }
        
        print("Critical Capabilities:")
        print("-" * 70)
        for name, capability in checks.items():
            if capability in cap_str:
                print(f"  ✓ {name:<25} - SUPPORTED")
            else:
                print(f"  ✗ {name:<25} - Not supported")
        
        # ============================================================
        # STEP 4: Module Statistics
        # ============================================================
        print("\n" + "=" * 70)
        print("STEP 4: MODULE STATISTICS")
        print("=" * 70 + "\n")
        
        cisco_modules = [c for c in capabilities if 'Cisco-IOS-XE' in c]
        ietf_modules = [c for c in capabilities if 'urn:ietf:params:xml:ns:yang' in c]
        openconfig_modules = [c for c in capabilities if 'openconfig.net' in c]
        
        print(f"Cisco IOS-XE YANG Modules:  {len(cisco_modules)}")
        print(f"IETF Standard YANG Modules: {len(ietf_modules)}")
        print(f"OpenConfig YANG Modules:    {len(openconfig_modules)}")
        print(f"Total Supported Modules:    {len(cisco_modules) + len(ietf_modules) + len(openconfig_modules)}")
        
        # Show some Cisco modules
        print("\nSample Cisco Modules:")
        print("-" * 70)
        for i, cap in enumerate(cisco_modules[:10], 1):
            module, revision = extract_module_info(cap)
            if 'native' in cap:
                print(f"  {i}. {module:<40} (native config)")
            elif 'oper' in cap:
                print(f"  {i}. {module:<40} (operational)")
            else:
                print(f"  {i}. {module:<40}")
        
        if len(cisco_modules) > 10:
            print(f"  ... and {len(cisco_modules) - 10} more Cisco modules")
        
        # ============================================================
        # FINAL SUMMARY
        # ============================================================
        print("\n" + "=" * 70)
        print("FINAL SUMMARY - TASK 33")
        print("=" * 70)
        
        print(f"✓ STEP 1: {len(capabilities)} capabilities retrieved")
        print(f"✓ STEP 2: Capabilities categorized into {len([c for c in categories.values() if c])} categories")
        print(f"✓ STEP 3: Key capabilities analyzed")
        print(f"✓ STEP 4: Module statistics compiled")
        print()
        
        print("Key Findings:")
        print(f"  • Device supports {len(cisco_modules)} Cisco-IOS-XE YANG modules")
        print(f"  • Device supports {len(ietf_modules)} IETF standard YANG modules")
        print(f"  • Device supports {len(openconfig_modules)} OpenConfig YANG modules")
        print(f"  • Writable-running mode: {'✓' if 'writable-running' in cap_str else '✗'}")
        print(f"  • Candidate datastore: {'✓' if 'candidate' in cap_str else '✗'}")
        print(f"  • YANG actions (Tail-f): {'✓' if 'tail-f.com/ns/netconf/actions' in cap_str else '✗'}")
        print()
        
        print(" TASK 33 COMPLETED SUCCESSFULLY!")
        print()
        print("✓ Method: ncclient manager.server_capabilities")
        print("✓ Data Source: NETCONF <hello> capability exchange")
        print("✓ Analysis: Categorized by namespace and module type")
        print("=" * 70 + "\n")
        
        # Always close session
        mgr.close_session()
        print("NETCONF session closed\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()