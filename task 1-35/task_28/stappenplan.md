# Stappenplan - Task 28: Retrieve Routing Table

## 📋 Overzicht
Deze gids leidt je stap-voor-stap door **Task 28**: Haal de operationele routing table op via YANG.

## 🎯 Doelstelling
GET operation configureren op N/A (Operational data) via NETCONF/YANG.

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
**YANG Path**: `/routing-state/routing-instance/ribs (operational)`

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
nano task_28.py
```

### 3.2 Pas XML payload aan (indien nodig)
Het script bevat reeds:
```xml
<filter>
  <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
    <routing-instance>
      <ribs/>
    </routing-instance>
  </routing-state>
</filter>
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
python task_28.py
```

### Verwachte uitvoer:
```
============================================================
Task 28: Retrieve Routing Table
============================================================
[*] Connecting to 192.168.19.139:830...
[+] Successfully connected to device!
[*] Sending NETCONF edit-config request...
[+] edit-config successful!
[*] Committing changes...
[+] Commit successful!
[+] Task 28 completed successfully!
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
show ip route
```

### 5.3 Verwachte output
```
Routing table in XML/JSON format
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
│  (task_28.py) │
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
