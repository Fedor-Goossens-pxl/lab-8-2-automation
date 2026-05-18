# Stappenplan - Task 23: Configure Multiple Interfaces in One Transaction

## 📋 Overzicht
Deze gids leidt je stap-voor-stap door **Task 23**: Pas configuraties toe op meerdere interfaces binnen één NETCONF transactie.

## 🎯 Doelstelling
Atomic transaction configureren op GigabitEthernet0/0/1 + 0/0/2 via NETCONF/YANG.

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
**YANG Path**: `Multiple interfaces in single edit-config`

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
nano task_23.py
```

### 3.2 Pas XML payload aan (indien nodig)
Het script bevat reeds:
```xml
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>0/0/1</name>
        <description>Interface 1 - configured atomically</description>
      </GigabitEthernet>
      <GigabitEthernet>
        <name>0/0/2</name>
        <description>Interface 2 - configured atomically</description>
      </GigabitEthernet>
    </interface>
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
python task_23.py
```

### Verwachte uitvoer:
```
============================================================
Task 23: Configure Multiple Interfaces in One Transaction
============================================================
[*] Connecting to 192.168.19.139:830...
[+] Successfully connected to device!
[*] Sending NETCONF edit-config request...
[+] edit-config successful!
[*] Committing changes...
[+] Commit successful!
[+] Task 23 completed successfully!
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
show ip interface brief
```

### 5.3 Verwachte output
```
Both interfaces configured in single transaction
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
│  (task_23.py) │
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
