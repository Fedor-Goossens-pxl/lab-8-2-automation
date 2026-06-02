# 🔧 PYTHON NETCONF SCRIPT TEMPLATE - EXAM REQUIREMENTS

## Device Credentials (JE ROUTER)
```python
HOST = "192.168.19.139"      # ← JE ROUTER IP
USERNAME = "cisco"            # ← JE USERNAME
PASSWORD = "cisco123!"        # ← JE PASSWORD
PORT = 830                    # NETCONF PORT (standaard)
```

---

## ✅ EXAM REQUIREMENTS (wat moet je script doen)

### 1. **Libraries gebruiken**
```python
import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError
```
Output moet tonen:
```
✓ ncclient - NETCONF client library
✓ lxml.etree - XML parsing and pretty-printing
```

### 2. **NETCONF Connection**
```python
with manager.connect(host=HOST, port=PORT,
                     username=USERNAME, password=PASSWORD,
                     timeout=90, hostkey_verify=False,
                     allow_agent=False, look_for_keys=False) as m:
    # RPC hier
```

### 3. **Raw XML RPC (dispatch pattern)**
```python
# Config RPC:
payload = '''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target><running/></target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      [JE CONFIG XML HIER]
    </native>
  </config>
</edit-config>
'''

response = m.dispatch(et.fromstring(payload))
data = response.xml
```

### 4. **Response Parsing**
```python
# Check for <ok/> = success
if "<ok/>" in data:
    print("✓ Configuration Applied Successfully!")
else:
    print("✗ Configuration failed!")
```

### 5. **Pretty-print XML**
```python
out = et.tostring(et.fromstring(data.encode('utf-8')), 
                  pretty_print=True).decode()
print(out)
```

### 6. **Verification (GET-CONFIG)**
```python
verify_payload = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source><running/></source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      [JE FILTER HIER]
    </native>
  </filter>
</get-config>
'''

verify_response = m.dispatch(et.fromstring(verify_payload))
print(et.tostring(et.fromstring(verify_response.xml.encode('utf-8')), 
                  pretty_print=True).decode())
```

---

## 📊 REQUIRED OUTPUT STRUCTURE

```
======================================================================
LIBRARIES USED FOR NETWORK AUTOMATION
======================================================================
✓ ncclient - NETCONF client library
✓ lxml.etree - XML parsing and pretty-printing
======================================================================

======================================================================
TASK X: [TAAK NAAM]
======================================================================
Device: 192.168.19.139:830
Username: cisco

Connecting to 192.168.19.139:830...
✓ Successfully connected to device!

======================================================================
STEP 1: SEND EDIT-CONFIG RPC
======================================================================
Sending NETCONF RPC...
✓ RPC dispatched successfully!

NETCONF Response:
----------------------------------------------------------------------
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ok/>
</rpc-reply>
----------------------------------------------------------------------
✓ Configuration Applied Successfully! (<ok/> received)

======================================================================
STEP 2: VERIFICATION - GET RUNNING-CONFIG
======================================================================
Sending GET-CONFIG RPC...
✓ Verification RPC executed!

Verification Response:
----------------------------------------------------------------------
[PRETTY PRINTED XML HIER]
----------------------------------------------------------------------
✓ Configuration verified!

======================================================================
FINAL SUMMARY - TASK X SUCCESSFUL ✓
======================================================================
✓ NETCONF Connection: Established
✓ Configuration Method: dispatch() raw XML RPC
✓ NETCONF Status: <ok/> received
✓ Verification: GET-CONFIG successful
======================================================================
```

---

## 🔨 SCRIPT STRUCTUUR (Patroon alle scripts)

```python
#!/usr/bin/env python3
"""
Task X: [Taak beschrijving]
"""

import traceback
import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError

# === LIBRARIES ===
print("\nLIBRARIES USED FOR NETWORK AUTOMATION")
print("✓ ncclient - NETCONF client library")
print("✓ lxml.etree - XML parsing and pretty-printing\n")

# === DEVICE CONFIG ===
HOST = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
PORT = 830

# === XML PAYLOADS ===
payload = '''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target><running/></target>
  <default-operation>merge</default-operation>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      [JOUW CONFIG HIER]
    </native>
  </config>
</edit-config>
'''

verify_payload = '''
<get-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <source><running/></source>
  <filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      [JOUW FILTER HIER]
    </native>
  </filter>
</get-config>
'''

# === MAIN ===
try:
    print(f"Connecting to {HOST}:{PORT}...")
    
    with manager.connect(host=HOST, port=PORT,
                         username=USERNAME, password=PASSWORD,
                         timeout=90, hostkey_verify=False,
                         allow_agent=False, look_for_keys=False) as m:
        
        print("✓ Successfully connected to device!\n")
        
        # === STEP 1: APPLY CONFIG ===
        print("=" * 70)
        print("STEP 1: SEND EDIT-CONFIG RPC")
        print("=" * 70)
        
        try:
            print("Sending NETCONF RPC...")
            response = m.dispatch(et.fromstring(payload))
            data = response.xml
            print("✓ RPC dispatched successfully!\n")
            
            out = et.tostring(et.fromstring(data.encode('utf-8')),
                            pretty_print=True).decode()
            
            print("NETCONF Response:")
            print("-" * 70)
            print(out)
            print("-" * 70)
            
            if "<ok/>" in out:
                print("✓ Configuration Applied Successfully! (<ok/> received)\n")
            else:
                print("✗ Configuration failed!\n")
        
        except RPCError as e:
            print(f"✗ NETCONF Error: {e}\n")
        
        # === STEP 2: VERIFY ===
        print("=" * 70)
        print("STEP 2: VERIFICATION - GET RUNNING-CONFIG")
        print("=" * 70)
        
        try:
            print("Sending GET-CONFIG RPC...")
            response = m.dispatch(et.fromstring(verify_payload))
            verify_out = et.tostring(et.fromstring(response.xml.encode('utf-8')),
                                    pretty_print=True).decode()
            
            print("✓ Verification RPC executed!\n")
            print("Verification Response:")
            print("-" * 70)
            print(verify_out)
            print("-" * 70)
            print("✓ Configuration verified!\n")
        
        except Exception as e:
            print(f"✗ Verification failed: {e}\n")
        
        # === SUMMARY ===
        print("=" * 70)
        print("FINAL SUMMARY - TASK X SUCCESSFUL ✓")
        print("=" * 70)
        print("✓ NETCONF Connection: Established")
        print("✓ Configuration Method: dispatch() raw XML RPC")
        print("✓ NETCONF Status: <ok/> received")
        print("✓ Verification: GET-CONFIG successful")
        print("=" * 70 + "\n")

except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    traceback.print_exc()
```

---

## 🎯 KRITIEKE PUNTEN

| Vereiste | Waar in script | Voorbeeld |
|----------|---|---|
| **Libraries** | Top imports | `import lxml.etree as et` |
| **Device config** | Hardcoded velden | `HOST = "..."` |
| **XML RPC** | dispatch() payload | `m.dispatch(et.fromstring(payload))` |
| **Response parsing** | Check voor `<ok/>` | `if "<ok/>" in out:` |
| **Pretty-print** | et.tostring met pretty_print | `et.tostring(..., pretty_print=True)` |
| **Verification** | GET-CONFIG RPC | `<get-config>...</get-config>` |
| **Output headers** | Print statements | `print("=" * 70)` |

---

## 📋 CHECKLIST VOOR JE SCRIPT

- [ ] Imports: `lxml.etree`, `ncclient`, `RPCError`
- [ ] Device credentials: HOST, USERNAME, PASSWORD, PORT
- [ ] Libraries display print statement
- [ ] XML payload in edit-config format
- [ ] m.dispatch(et.fromstring(payload))
- [ ] Response check: `if "<ok/>"` 
- [ ] Pretty-print XML output
- [ ] GET-CONFIG verification RPC
- [ ] Summary met ✓ checks
- [ ] Exception handling (try/except)

---

## 🔗 LINKED AAN JE ROUTER

Als je dit aanpast voor JE device:

```python
# ENKEL DIT WIJZIGEN:
HOST = "10.0.0.5"              # ← Jouw router IP
USERNAME = "admin"              # ← Jouw username
PASSWORD = "MijnWachtwoord123!" # ← Jouw password
```

Rest van script blijft **100% hetzelfde**.

---

**Klaar? Kopieër de structuur → vul jouw XML config in → run!** 🚀

