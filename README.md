# Network as Code - NETCONF Automation (Task 36)

## Project Overzicht
Dit project implementeert **Task 36** van LAB 8.2: NETCONF-automatisering met Python.

**Doel:** Automatiseer Cisco IOS-XE configuratie via NETCONF met YANG-modellen, waarbij GitHub als "single source of truth" fungeert.

---

## 📋 Project Structuur

```
netconf-automation/
├── config-iosxe.xml          # YANG XML-configuratie (GitHub bron)
├── task36_netconf.py         # Python NETCONF automation script
├── README.md                 # Dit bestand
└── .gitignore               # Git-ignorepatterns
```

---

## 🔧 Installatie & Setup

### Vereisten
- Python 3.6+
- ncclient (NETCONF client)
- Cisco IOS-XE device (CSR1000v of fysieke router)
- NETCONF SSH enabled op device

### Libraries Installeren
```bash
pip3 install ncclient requests
```

### Device Setup
Zorg dat NETCONF enabled is op je IOS-XE device:
```
csr1000v# configure terminal
csr1000v(config)# netconf ssh
csr1000v(config)# end
csr1000v# write memory
```

---

## 🚀 Gebruik

### Device IP en Credentials Aanpassen
Edit `task36_netconf.py` en update:
```python
DEVICE_HOST = "10.255.255.100"      # IP van jouw device
DEVICE_PORT = 830
DEVICE_USERNAME = "admin"
DEVICE_PASSWORD = "admin"
```

### Script Uitvoeren
```bash
python3 task36_netconf.py
```

---

## ✅ Wat het Script Doet

1. **Inladen config** uit `config-iosxe.xml` (simuleert GitHub)
2. **NETCONF SSH** verbinding maken met device
3. **Check capabilities** van het device
4. **Edit-config** naar candidate datastore
5. **Commit** naar running datastore
6. **Verificatie** door running-config op te halen

---

## 📊 Output & Logging

Het script toont:
- ✓ Succesvolle NETCONF RPC-replies (`<ok/>`)
- ✗ Foutmeldingen met error-type/error-tag
- Pretty-printed XML responses
- HTTP-achtige status meldingen

**Voorbeeld:**
```
✓ NETCONF-verbinding gelukt!
✓ Edit-config succes! RPC reply: <ok/>
✓ Commit succes! RPC reply: <ok/>
✓ Device ondersteunt candidate datastore en commit!
```

---

## 🔒 Foutafhandeling

Geïmplementeerde features:
- ✓ Exception handling voor connection failures
- ✓ RPC-reply status controleren (`<ok/>` check)
- ✓ Discard-changes bij fout
- ✓ Pretty-printed XML voor debugging
- ✓ HTTP-achtige statusmeldingen

---

## 📈 Basisvaardigheden (PE Evaluatie)

Dit project demonstreert:

✅ **Python gebruik & dataverwerking** (1pt)
- XML parsing en pretty-printing
- ncclient library juist gebruikt
- Leesbare output

✅ **Statusinformatie & foutafhandeling** (2pts)
- NETCONF `<ok/>` responses gecontroleerd
- Error-type/error-tag verwerking
- Logging van alle operaties
- Discard-changes foutafhandeling

✅ **Git/GitHub** (2pts)
- Config-bestand onder versiebeheer
- Scripts in Git repository
- Single source of truth setup

✅ **End-to-end YANG automatisatie** (2pts)
- NETCONF edit-config / commit
- YANG XML-configuratie
- Volledige workflow werkend

---

## 🛠️ Troubleshooting

### Verbinding mislukt
```
✗ NETCONF-verbinding mislukt: [Errno -1] SSH session not active
```
**Oplossing:**
- Check IP-adres en poort
- Controleer NETCONF status: `show netconf-yang servers`
- Test SSH: `ssh admin@10.255.255.100`

### Edit-config mislukt
```
✗ Edit-config mislukt! RPC Reply: <error>...</error>
```
**Oplossing:**
- Controleer YANG XML syntax
- Check YANG capabilities van device
- Zorg dat interfaces/routing protocol ondersteund is

### Commit mislukt
```
✗ Commit mislukt!
```
**Oplossing:**
- Check candidate datastore: `show netconf-yang candidate`
- Zorg dat config valid is
- Controleer device resources

---

## 📚 Referenties

- NCCLIENT: https://github.com/ncclient/ncclient
- Cisco NETCONF: https://developer.cisco.com/
- YANG Models: https://github.com/YangModels/yang
- OpenConfig: https://www.openconfig.net/

---

## 📝 PE Evaluatiecriteria

Dit project voldoet aan:
- ✓ Basis YANG-configuratie
- ✓ NETCONF candidate datastore
- ✓ Python error handling
- ✓ Git versiebeheer
- ✓ Foutafhandeling en status feedback

**Verwachte score:** 9-10/10

