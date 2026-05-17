# STAP-VOOR-STAP TASK 36: NETCONF (Python)

## Stap 2.1: Project folder aanmaken

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation
mkdir task36-netconf
cd task36-netconf
```

---

## Stap 2.2: Bestanden plaatsen

Plaats deze 3 bestanden in `C:\Users\fedor\lab-8-2-automation\task36-netconf\`:

1. task36_netconf.py
2. config-iosxe.xml
3. TASK36_README.md (rename naar README.md)

Verificatie:

```powershell
ls
# Output verwacht:
# task36_netconf.py
# config-iosxe.xml
# README.md
```

---

## Stap 2.3: Device configuratie (op CSR1000v)

SSH naar CSR1000v en voer uit:

```bash
configure terminal
netconf ssh
exit
write memory
```

Verificatie:

```bash
show run | grep netconf
# Output: netconf ssh
```

---

## Stap 2.4: Script credentials aanpassen

Edit `task36_netconf.py` en controleer:

```python
DEVICE_HOST = "192.168.19.139"
DEVICE_PORT = 830
DEVICE_USERNAME = "admin"
DEVICE_PASSWORD = "123"
CONFIG_FILE = "config-iosxe.xml"
```

---

## Stap 2.5: Test Python syntax

In PowerShell:

```powershell
python -m py_compile task36_netconf.py
# Geen output = OK
```

---

## Stap 2.6: Run NETCONF script (OPMERKING: zal mogelijk falen op CSR1000v)

In PowerShell:

```powershell
python task36_netconf.py
```

Verwachte output:

```
TASK 36: NETCONF (Python) - Network as Code
======================================================================

STAP 1: Configuratie inladen
Configuratie ingeladen uit: config-iosxe.xml

Config preview:
<?xml version="1.0" ?>
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>NETCONF-Router-PE</hostname>
    ...
  </native>
</config>

STAP 2: Controleer NETCONF connectiviteit
Verbinden met 192.168.19.139:830...
NETCONF-verbinding gelukt!

--- DEVICE NETCONF CAPABILITIES ---
Device supports 45 NETCONF capabilities

STAP 3: Edit-config naar CANDIDATE DATASTORE
Edit-config succes! RPC reply: <ok/>

STAP 4: Commit naar RUNNING DATASTORE
Commit succes! RPC reply: <ok/>

STAP 5: Retrieve RUNNING CONFIG
Running configuration opgehaald

======================================================================
TASK 36 VOLTOOID - Network as Code succesvol!
======================================================================
```

---

## Stap 2.7: Verificatie op device (als script succesvol)

Op CSR1000v:

```bash
show run | grep hostname
# Output: hostname NETCONF-Router-PE

show ip interface brief
# Output:
# GigabitEthernet1  10.255.255.1  up  up
# GigabitEthernet2  192.168.1.1   up  up
# Loopback0         172.16.1.1    up  up

show ip ospf
# Output: Routing Process "ospf 1" with ID 172.16.1.1
```

---

## Stap 2.8: Git commit Task 36

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation

git add .
git commit -m "Add Task 36 NETCONF Python - YANG edit-config implementation"
git push
```

---

## SAMENVATTING TASK 36 COMMANDS

### Setup
```powershell
mkdir task36-netconf
cd task36-netconf
python -m py_compile task36_netconf.py
```

### Run
```powershell
python task36_netconf.py
```

### Git
```powershell
cd C:\Users\fedor\lab-8-2-automation
git add .
git commit -m "Add Task 36 NETCONF Python"
git push
```

### Device commands
```bash
configure terminal
netconf ssh
exit
write memory
show run | grep netconf
show run | grep hostname
show ip interface brief
show ip ospf
```

---

**Volg deze stappen en Task 36 is klaar!**
