# STAP-VOOR-STAP TASK 38: RESTCONF (Python)

## Stap 3.1: Project folder aanmaken

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation
mkdir task38-restconf
cd task38-restconf
```

---

## Stap 3.2: Bestanden plaatsen

Plaats deze 3 bestanden in `C:\Users\fedor\lab-8-2-automation\task38-restconf\`:

1. task38_restconf.py
2. config-restconf.json
3. TASK38_README.md (rename naar README.md)

Verificatie:

```powershell
ls
# Output verwacht:
# task38_restconf.py
# config-restconf.json
# README.md
```

---

## Stap 3.3: Device configuratie (op CSR1000v)

SSH naar CSR1000v en voer uit:

```bash
configure terminal
restconf
exit
write memory
```

Verificatie:

```bash
show restconf
# Output: restconf enabled
```

---

## Stap 3.4: Script credentials aanpassen

Edit `task38_restconf.py` en controleer:

```python
DEVICE_HOST = "192.168.19.139"
DEVICE_PORT = 443
DEVICE_USERNAME = "admin"
DEVICE_PASSWORD = "123"
CONFIG_FILE = "config-restconf.json"
```

---

## Stap 3.5: Test JSON syntax

In PowerShell:

```powershell
python -m json.tool config-restconf.json
# Geen errors = OK
```

---

## Stap 3.6: Test Python syntax

In PowerShell:

```powershell
python -m py_compile task38_restconf.py
# Geen output = OK
```

---

## Stap 3.7: Test RESTCONF connectiviteit (optioneel)

In PowerShell:

```powershell
$uri = "https://192.168.19.139:443/restconf/data/ietf-yang-library:modules-state"

try {
    $response = Invoke-WebRequest -Uri $uri `
        -Credential (New-Object System.Management.Automation.PSCredential("admin", (ConvertTo-SecureString "123" -AsPlainText -Force))) `
        -SkipCertificateCheck `
        -TimeoutSec 5
    Write-Host "RESTCONF bereikbaar! Status: $($response.StatusCode)"
} catch {
    Write-Host "RESTCONF niet bereikbaar: $($_.Exception.Message)"
}
```

---

## Stap 3.8: Run RESTCONF script (OPMERKING: zal mogelijk falen op CSR1000v)

In PowerShell:

```powershell
python task38_restconf.py
```

Verwachte output:

```
TASK 38: RESTCONF (Python) - Network as Code
======================================================================

STAP 1: Configuratie inladen
Configuratie ingeladen uit: config-restconf.json

Config preview:
{
  "hostname": "RESTCONF-Router-PE",
  "interfaces": [
    ...
  ]
}

STAP 2: Controleer RESTCONF connectiviteit
Verbinden met 192.168.19.139:443...
Connectiviteit OK - RESTCONF API bereikbaar

STAP 3: Configureer hostname
PUT request naar: https://192.168.19.139:443/restconf/data/...
Hostname configuratie succesvol (HTTP 201)

STAP 4: Configureer interfaces
PUT request naar: https://192.168.19.139:443/restconf/data/...
Interface 1 configuratie succesvol (HTTP 201)
Interface 2 configuratie succesvol (HTTP 201)

STAP 5: Configureer OSPF
PUT request naar: https://192.168.19.139:443/restconf/data/...
OSPF configuratie succesvol (HTTP 201)

STAP 6: Verificatie - Haal running config op
Running configuration opgehaald (HTTP 200)

======================================================================
TASK 38 VOLTOOID - Network as Code succesvol!
======================================================================
```

---

## Stap 3.9: Verificatie op device (als script succesvol)

Op CSR1000v:

```bash
show run | grep hostname
# Output: hostname RESTCONF-Router-PE

show ip interface brief
# Output:
# GigabitEthernet1  10.255.255.1  up  up
# GigabitEthernet2  192.168.1.1   up  up
# Loopback0         172.16.1.1    up  up

show ip ospf
# Output: Routing Process "ospf 1" with ID 172.16.1.1
```

---

## Stap 3.10: Git commit Task 38

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation

git add .
git commit -m "Add Task 38 RESTCONF Python - HTTP PUT/PATCH with JSON implementation"
git push
```

---

## SAMENVATTING TASK 38 COMMANDS

### Setup
```powershell
mkdir task38-restconf
cd task38-restconf
python -m json.tool config-restconf.json
python -m py_compile task38_restconf.py
```

### Run
```powershell
python task38_restconf.py
```

### Git
```powershell
cd C:\Users\fedor\lab-8-2-automation
git add .
git commit -m "Add Task 38 RESTCONF Python"
git push
```

### Device commands
```bash
configure terminal
restconf
exit
write memory
show restconf
show run | grep hostname
show ip interface brief
show ip ospf
```

---

**Volg deze stappen en Task 38 is klaar!**
