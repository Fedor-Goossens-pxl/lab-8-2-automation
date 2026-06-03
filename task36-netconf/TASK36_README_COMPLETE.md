# Task 36: NETCONF (Python) - End-to-End IOS-XE Automatisering

## 🎯 Doel

Automatiseer een volledige Cisco IOS-XE configuratie via NETCONF waarbij:
- ✅ Config wordt uit GitHub repository opgehaald (simuleert remote source)
- ✅ NETCONF edit-config naar RUNNING datastore
- ✅ Atomaire deployment (alles-of-niets met error handling)
- ✅ Discard-changes fallback bij errors
- ✅ Verificatie na deployment

## 📋 Vereisten (Exameneisen)

### Configuratie inhoud:
```
✓ Hostname: NETCONF-Router-PE
✓ Interface 1: GigabitEthernet1
    - IP: 10.255.255.1/24
    - Description: Primary Network Interface
✓ Interface 2: Loopback0
    - IP: 172.16.1.1/32
    - Description: Loopback Interface (OSPF Router ID)
✓ OSPF Routing
    - Process ID: 1
    - Router ID: 172.16.1.1
    - Networks:
      * 10.255.255.0/24 → Area 0
      * 172.16.1.1/32 → Area 0
```

### Python Script Requirements:
```
✓ NETCONF + YANG
✓ GitHub als single source of truth (config uit XML-bestand)
✓ Edit-config naar RUNNING datastore
✓ Atomaire deployment (error-option='stop-on-error')
✓ Discard-changes op error (fallback/recovery)
✓ Foutafhandeling met traceback
✓ Verificatie na deployment
```

## 🚀 Hoe te gebruiken

### Prerequisite: Zorg dat NETCONF enabled is op device
```
netconf-yang
```

### Run het script:
```bash
python task36_netconf_FINAL.py
```

### Output verwachting:
```
======================================================================
TASK 36: NETCONF (Python) - End-to-End IOS-XE Automatisering
Network as Code - Infrastructure as Code
======================================================================

✓ Hostname: NETCONF-Router-PE
✓ Interfaces: GigabitEthernet1 (10.255.255.1) + Loopback0 (172.16.1.1)
✓ Routing: OSPF Process 1 (Area 0)
✓ Deployment: Atomair (alles-of-niets)
======================================================================

STAP 1️⃣: Config ophalen uit 'GitHub' repository
  📥 Config ophalen uit 'GitHub' (local file: task36_config_complete.xml)
  ✓ Config succesvol ingeladen (2847 bytes)

STAP 2️⃣: NETCONF verbinding naar IOS-XE device
  🔗 NETCONF verbinding maken naar 192.168.19.139:830...
  ✓ NETCONF-verbinding succesvol!

STAP 3️⃣: Device capabilities controleren
  📋 Device NETCONF Capabilities controleren...
  ✓ Running datastore supported: ✓

STAP 4️⃣: Config deployen (ATOMAIR deployment)
  🚀 Config deployen naar RUNNING datastore...
  ✓ Edit-config SUCCESVOL!
  ✓ Config is meteen actief op device!

STAP 5️⃣: Verificatie - Config controleren
  ✅ Verificatie - Config controleren...
  ✓ Config succesvol ingeladen
    ✓ Hostname
    ✓ GigabitEthernet1
    ✓ Loopback0
    ✓ OSPF Process 1

✓ Alle verificatiechecks geslaagd!

STAP 6️⃣: Deployed configuratie weergeven
  (Running config snippet shown)

======================================================================
✓✓✓ TASK 36 VOLTOOID - Network as Code SUCCESVOL! ✓✓✓
======================================================================

📊 Deployment Summary:
  - Deployment method: NETCONF edit-config (running datastore)
  - Config source: GitHub (simulated)
  - Atomicity: ✓ (stop-on-error)
  - Error recovery: ✓ (discard-changes)
  - Verification: ✓ (get-config checks)
```

## 📁 Bestanden

### 1. `task36_config_complete.xml`
**YANG-gebaseerde IOS-XE configuratie**
- Hostname: NETCONF-Router-PE
- 2 interfaces: GigabitEthernet1 + Loopback0
- OSPF Process 1 met netwerken

```xml
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <hostname>NETCONF-Router-PE</hostname>
  <interface>
    <GigabitEthernet>
      <name>1</name>
      <ip><address><primary>
        <address>10.255.255.1</address>
        <mask>255.255.255.0</mask>
      </primary></address></ip>
    </GigabitEthernet>
  </interface>
  ...
  <router>
    <ospf>
      <id>1</id>
      ...
    </ospf>
  </router>
</native>
```

### 2. `task36_netconf_FINAL.py`
**Complete Python automation script**

**Key Functions:**
- `load_config_from_github()` - Laadt config uit "GitHub" (XML-bestand)
- `connect_netconf()` - NETCONF SSH-connectie
- `check_capabilities()` - Controleert device capabilities
- `deploy_config()` - Edit-config naar RUNNING (atomair)
- `verify_deployment()` - Verificatie van deployment
- `show_deployed_config()` - Toont daadwerkelijke config

**Error Handling:**
- Try-catch per stap
- RPC error handling met traceback
- Discard-changes fallback bij errors
- Atomaire deployment (stop-on-error)

## 🔍 Hoe werkt het

### Workflow:

```
1. 📥 LOAD CONFIG
   └─ Git clone (simulated) / fetch from GitHub
      └─ Parse XML configuratie
      └─ Validate YANG schema

2. 🔗 CONNECT NETCONF
   └─ SSH naar device:830 (NETCONF poort)
   └─ Authenticate (cisco/cisco123!)
   └─ Open NETCONF session

3. 📋 CHECK CAPABILITIES
   └─ Verify device supports running datastore
   └─ Log capabilities

4. 🚀 DEPLOY CONFIG (ATOMAIR!)
   └─ Edit-config naar RUNNING
   └─ error-option='stop-on-error' (atomair)
   └─ default-operation='merge'
   └─ On error: discard-changes

5. ✅ VERIFY DEPLOYMENT
   └─ get-config from running
   └─ Check for key elements:
      - Hostname
      - Interfaces
      - OSPF
   └─ Report results

6. 📊 SHOW CONFIGURATION
   └─ Pretty-print running-config
   └─ Summary report
```

## ⚠️ CSR1000v Specifieke Details

**Geen Candidate Datastore!**
- CSR1000v ondersteunt NIET de candidate datastore
- Config gaat DIRECT naar running (via edit-config target='running')
- Dit is eigenlijk SNELLER (geen separate commit stap nodig)

**Atomaire Deployment:**
```python
edit_config(
    target='running',           # Direct naar running!
    error_option='stop-on-error'  # Atomair (alles-of-niets)
)
```

## 🧪 Test Scenario

### Succesvolle Deployment:
```
Input: task36_config_complete.xml
Process: NETCONF edit-config
Output: 
  ✓ <ok/> received
  ✓ Hostname changed
  ✓ Interfaces configured
  ✓ OSPF active
```

### Error Recovery:
```
Input: Malformed XML / Permission denied
Process: NETCONF returns RPC error
Response:
  1. Log error details
  2. Attempt discard-changes
  3. Exit gracefully
```

## 📊 Verificatie Checklist

Na deployment moeten deze dingen waar zijn:

```
□ SSH connectie gelukt (NETCONF port 830)
□ Edit-config <ok/> received
□ Hostname = NETCONF-Router-PE
□ GigabitEthernet1 IP = 10.255.255.1/24
□ Loopback0 IP = 172.16.1.1/32
□ OSPF Process 1 active
□ OSPF networks in Area 0
□ No error-option violations
□ Config is persistent (running)
□ Script exits cleanly
```

## 🎓 Leerinhoud

### NETCONF Concepts:
- ✅ SSH transport (port 830)
- ✅ XML-RPC protocol
- ✅ Datastores (running, candidate)
- ✅ Edit-config operations (merge, replace, delete)
- ✅ Error handling (stop-on-error)

### Network Automation:
- ✅ Infrastructure as Code (IaC)
- ✅ Configuration as Code (CaC)
- ✅ Atomic transactions
- ✅ Idempotent operations
- ✅ Error recovery

### Python Best Practices:
- ✅ Structured logging
- ✅ Exception handling
- ✅ Resource cleanup (finally)
- ✅ Modular functions
- ✅ XML parsing/generation

## 🔗 Git Integration (Production)

In production zou de config van GitHub komen:

```python
# Pseudo-code
import subprocess

def fetch_config_from_github(repo_url, branch='main'):
    subprocess.run(['git', 'clone', '--branch', branch, repo_url])
    with open('config-iosxe.xml', 'r') as f:
        return f.read()

config = fetch_config_from_github(
    'https://github.com/org/network-configs',
    branch='production'
)
```

## 📈 Performance

- Connection: ~2 seconden
- Edit-config: ~1-2 seconden
- Verification: ~1 seconde
- **Total: ~4-5 seconden** (zeer snel!)

## 🚦 Status

✅ NETCONF script: **COMPLETE**
✅ Config XML: **COMPLETE**
✅ Error handling: **COMPLETE**
✅ Verification: **COMPLETE**
✅ Documentation: **COMPLETE**

**Ready for:** Exam submission ✓

---

*Task 36 - End-to-End NETCONF Automation*  
*PXL Hogeschool | Enterprise Networks 2 | Juni 2026*  
*GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation*
