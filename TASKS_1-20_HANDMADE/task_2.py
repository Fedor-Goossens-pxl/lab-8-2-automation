#!/usr/bin/env python3
"""
FINAL NETCONF FIX - Gewoon strings gebruiken!
"""

from ncclient import manager

DEVICE = "192.168.19.139"
PORT = 830
USER = "cisco"
PASS = "cisco123!"

print("=" * 70)
print("NETCONF FINAL TEST")
print("=" * 70)

try:
    print("\n[1] Connecting...")
    mgr = manager.connect(
        host=DEVICE,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={'name': 'iosxe'},
        timeout=30,
        allow_agent=False,
        look_for_keys=False
    )
    print("✓ Connected!")
    
    print("\n[2] Sending NETCONF edit-config...")
    
    # ✅ GEWOON STRING!
    response = mgr.edit_config(
        target='running',
        config="""<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <hostname>CSR1kv-AUTO</hostname>
</native>
</config>"""
    )
    
    print("✓ Sent!")
    print(response.xml)
    
    print("\n[3] Verifying...")
    get_resp = mgr.get_config('running')
    
    if 'CSR1kv-AUTO' in get_resp.xml:
        print("✓✓✓ SUCCESS! It works!")
    else:
        print("Check SSH to verify")
    
    mgr.close_session()
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()