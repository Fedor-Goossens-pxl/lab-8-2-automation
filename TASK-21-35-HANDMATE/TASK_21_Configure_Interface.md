# Task 21: Configure Interface via NETCONF/YANG

## 📝 Wat doet het script?

Configureer een interface description op de CSR1000v router via **NETCONF met native Cisco YANG models**. Dit is de basis task die het dispatch() patroon introduceert.

## ⚙️ Hoe werkt het?

- **Patroon:** NETCONF `dispatch()` met `lxml.etree` (niet `edit_config()`)
- **Method:** Raw XML RPC naar running-config
- **Datastore:** running-config (merge mode - geen candidate!)
- **Interface:** Loopback0 (veilig te modificeren op CSR1000v)
- **YANG Namespace:** `http://cisco.com/ns/yang/Cisco-IOS-XE-native`
- **Verificatie:** GET-CONFIG met filter

## ✅ Script Output (bij succes)

```
======================================================================
LIBRARIES USED FOR NETWORK AUTOMATION
======================================================================
✓ ncclient - NETCONF client library
======================================================================
======================================================================
TASK 21: CONFIGURE INTERFACE VIA NETCONF/YANG
======================================================================
Device: 192.168.19.139:830
Interface: Loopback0
Configuration: description "Configured via NETCONF - Task 21"
======================================================================
Connecting to 192.168.19.139:830...
✓ Connected!
✓ LOCK successful
✓ CONFIGURATION APPLIED
✓ UNLOCK successful
✓ VERIFICATION PASSED!

TASK 21 COMPLETED!
======================================================================
```

## 🔍 Hoe verifiëren op CSR1000v Router?

### 1. SSH naar de router:
```bash
ssh cisco@192.168.19.139
```

### 2. Verificatie commands:
```
show interfaces Loopback0 description
show running-config interface Loopback0
```

### 3. Wat je moet zien:
```
Interface                      Status         Description
Lo0                            up             Configured via NETCONF - Task 21
```

### 4. NETCONF verificatie (optional):
```
show netconf-yang sessions brief
```

## 📂 Script Details

- **File:** `task_21.py` (NETCONF version - FINAL)
- **Lock/Unlock:** Yes (atomic transaction)
- **Verify:** Yes (get-config after config)
- **GitHub:** https://github.com/Fedor-Goossens-pxl/lab-8-2-automation

## 🛠️ Device Vereisten

✓ Cisco IOS-XE 16.9.3+  
✓ NETCONF-YANG enabled: `netconf-yang`  
✓ SSH enabled: `ip ssh version 2`  
✓ Management interface bereikbaar (192.168.19.139)  
✓ Geldige credentials (cisco/cisco123!)  
✓ Loopback0 interface moet bestaan  

## 💡 Key Insights

- **NO `edit_config()` method** → Use `dispatch()` instead!
- **NO manual `<rpc>` wrapper** → ncclient adds it automatically
- **NO logging module** → Keep code clean
- **Lock/Unlock pattern** → Ensures atomicity
- **YANG namespaces matter** → Must specify xmlns correctly

## 🔑 NETCONF Pattern (Task 21)

```python
# Connect
m = manager.connect(host=HOST, port=PORT, username=USERNAME, 
                   password=PASSWORD, timeout=90, 
                   hostkey_verify=False, allow_agent=False, 
                   look_for_keys=False)

# Lock
m.dispatch(et.fromstring(lock_payload))

# Configure
response = m.dispatch(et.fromstring(config_payload))

# Unlock
m.dispatch(et.fromstring(unlock_payload))

# Verify
m.dispatch(et.fromstring(verify_payload))
```

---

*TASK_21_Configure_Interface - Enterprise Networks 2 | PXL Hogeschool | Juni 2026*
