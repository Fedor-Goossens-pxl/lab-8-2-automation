# Stappenplan - Task 35: Full Service Deployment

## 📋 Overzicht
Deze gids leidt je stap-voor-stap door **Task 35**: Deploy een volledige netwerkdienst (interfaces, IP-adressering, routing en ACL) in één transactie.

## 🎯 Doelstelling
Atomic full deployment configureren op Multiple interfaces + routing + ACL via NETCONF/YANG.

---

## 📝 Stap 1: Voorbereiding

### 1.1 Verifieer NETCONF op CSR1000v
```bash
ssh admin@192.168.19.139
show running-config | include netconf
# Verwacht: netconf-yang
```

### 1.2 Test NETCONF poort
```bash
nc -zv 192.168.19.139 830
# Verwacht: succeeded
```

### 1.3 Installeer Python dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ Stap 2: YANG Suite Workflow

### 2.1 Open YANG Suite
Navigate naar: `https://192.168.19.141:8443/yangtree/explore/`

### 2.2 Selecteer YANG Set
1. Klik op dropdown **"Select a YANG set"**
2. Kies: **`csr1000v-default-yangset`**

### 2.3 Load YANG Module
1. In het input veld type: **`cisco-ios-xe-native`**
2. Klik **"Load module(s)"**
3. Wacht tot de YANG tree laadt

### 2.4 Navigeer naar de juiste node
**YANG Path**: `Multiple containers in single edit-config`

Navigeer in de tree:
```
native/
├── interface/      (of relevant container)
│   └── ...
└── (gewenste node)
```

### 2.5 Genereer XML Template
1. **Right-click** op de gewenste node
2. Selecteer **"Get config template"**
3. Het XML payload verschijnt rechts
4. **Kopieer** het volledige XML

---

## 💻 Stap 3: Script Configuratie

### 3.1 Open script
```bash
nano task_35.py
```

### 3.2 Pas XML payload aan (indien nodig)
Het script bevat reeds:
```xml
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>CSR1000v-FULL-DEPLOY</hostname>
    <interface>
      <GigabitEthernet>
        <name>0/0/1</name>
        <description>WAN Interface</description>
        <ip>
          <address>
            <primary>
              <address>10.0.0.1</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
        <enabled>true</enabled>
      </GigabitEthernet>
    </interface>
    <router>
      <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
        <id>1</id>
        <network>
          <ip>10.0.0.0</ip>
          <wildcard>0.0.0.255</wildcard>
          <area>0</area>
        </network>
      </ospf>
    </router>
  </native>
</config>
```

### 3.3 Pas credentials aan (indien anders)
```python
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "admin"
PASSWORD = "123"
```

---

## ▶️ Stap 4: Script uitvoeren

```bash
python task_35.py
```

### Verwachte uitvoer:
```
============================================================
Task 35: Full Service Deployment
============================================================
[*] Connecting to 192.168.19.139:830...
[+] Successfully connected to device!
[*] Sending NETCONF edit-config request...
[+] edit-config successful!
[*] Committing changes...
[+] Commit successful!
[+] Task 35 completed successfully!
[*] NETCONF session closed
```

---

## ✅ Stap 5: Verificatie

### 5.1 SSH naar device
```bash
ssh admin@192.168.19.139
```

### 5.2 Verificatie commando
```
show running-config
```

### 5.3 Verwachte output
```
Full configuration deployed: hostname, interfaces, routing
```

---

## 🐛 Stap 6: Debugging Tips

### Connection Problems
```python
# Verhoog timeout
mgr = manager.connect(..., timeout=60)

# Disable host key check
mgr = manager.connect(..., hostkey_verify=False)
```

### XML Validation Errors
```bash
# Test XML met YANG Suite eerst
# Of gebruik xmllint:
xmllint --noout payload.xml
```

### Commit Failed
```python
# Gebruik discard-changes
mgr.discard_changes()
```

### Logging Inschakelen
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📊 Architectuur Diagram

```
┌──────────────────┐
│  Python Script   │
│  (task_35.py) │
└────────┬─────────┘
         │ ncclient
         │ NETCONF over SSH
         ▼
┌──────────────────┐
│   CSR1000v       │
│  192.168.19.139  │
│  Port: 830       │
└────────┬─────────┘
         │ edit-config
         ▼
┌──────────────────┐
│ Candidate Store  │
└────────┬─────────┘
         │ commit
         ▼
┌──────────────────┐
│  Running Config  │
└──────────────────┘
```

---

## 🎓 Wat heb je geleerd?

- ✅ NETCONF protocol gebruik
- ✅ YANG model navigatie via YANG Suite
- ✅ XML payload constructie
- ✅ Candidate datastore workflow
- ✅ Commit/discard operaties
- ✅ Python automation met ncclient

---

**Auteur**: Fedor Goossens  
**Datum**: Mei 2026
