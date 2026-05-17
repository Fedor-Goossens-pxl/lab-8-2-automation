# STAP-VOOR-STAP TASK 38: RESTCONF (Python)

Workflow: Windows → Git → SCP → DEVASC → Python Execution

---

## FASE 1: WINDOWS - VOORBEREIDING

## Stap 1: Project folder aanmaken

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation
mkdir task38-restconf
cd task38-restconf
```

---

## Stap 2: Bestanden plaatsen

Download Task 38 bestanden en plaats in `C:\Users\fedor\lab-8-2-automation\task38-restconf\`:

1. task38_restconf.py
2. config-restconf.json
3. README.md

Verificatie:

```powershell
ls
# Output verwacht:
# task38_restconf.py
# config-restconf.json
# README.md
```

---

## Stap 3: Git commit en push

```powershell
cd C:\Users\fedor\lab-8-2-automation

git add .
git commit -m "Add Task 38 RESTCONF Python - Network as Code automation"
git push
```

Output verwacht:

```
[main xxxxx] Add Task 38 RESTCONF Python
 3 files changed
 create mode 100644 task38-restconf/task38_restconf.py
 create mode 100644 task38-restconf/config-restconf.json
 create mode 100644 task38-restconf/README.md

To https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
   xxxx -> main
```

---

## FASE 2: WINDOWS - SCP NAAR DEVASC

## Stap 4: Kopieer bestanden naar DEVASC

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation\task38-restconf

scp task38_restconf.py devasc@192.168.19.140:~/task38-restconf/
scp config-restconf.json devasc@192.168.19.140:~/task38-restconf/
scp README.md devasc@192.168.19.140:~/task38-restconf/
```

Output verwacht:

```
task38_restconf.py        100%   8KB   2.5MB/s   00:00
config-restconf.json      100%   1KB   500KB/s   00:00
README.md                 100%   4KB   800KB/s   00:00
```

---

## FASE 3: DEVASC - VOORBEREIDING

## Stap 5: SSH naar DEVASC

In PowerShell:

```powershell
ssh devasc@192.168.19.140
```

---

## Stap 6: Maak folder aan en verify bestanden

Op DEVASC (bash):

```bash
mkdir -p ~/task38-restconf
cd ~/task38-restconf

ls
# Output verwacht:
# task38_restconf.py
# config-restconf.json
# README.md
```

---

## Stap 7: Python libraries installeren op DEVASC

```bash
pip3 install requests
```

Verificatie:

```bash
pip3 show requests
# Output: Name: requests, Version: 2.x.x
```

---

## FASE 4: DEVASC - DEVICE VOORBEREIDING

## Stap 8: Verify RESTCONF op CSR1000v

```bash
ssh admin@192.168.19.139

show run | include restconf
# Output: restconf

show run | include ip http
# Output:
# ip http authentication local
# ip http secure-server

exit
```

---

## FASE 5: DEVASC - PYTHON EXECUTION

## Stap 9: Script uitvoeren

Op DEVASC in task38-restconf folder:

```bash
cd ~/task38-restconf
python3 task38_restconf.py
```

Output verwacht:

```
======================================================================
TASK 38: RESTCONF (Python) - Network as Code
======================================================================

STAP 1: Configuratie ingeladen uit config-restconf.json

STAP 2: Verbinding testen met CSR1000v via RESTCONF...
Status code: 200
Verbinding succesvol!

STAP 3: Hostname configureren...
Status code: 204
Hostname geconfigureerd: RESTCONF-Router-PE

STAP 4: GigabitEthernet1 configureren...
Status code: 204
Interface geconfigureerd

STAP 5: GigabitEthernet2 configureren...
Status code: 204
Interface geconfigureerd

STAP 6: Loopback0 configureren...
Status code: 204
Interface geconfigureerd

STAP 7: OSPF configureren...
Status code: 204
OSPF geconfigureerd

STAP 8: Configuratie verifiëren...
Hostname: RESTCONF-Router-PE

======================================================================
TASK 38 VOLTOOID - Network as Code succesvol!
======================================================================
```

---

## FASE 6: DEVASC - DEVICE VERIFICATIE

## Stap 10: Verificatie op CSR1000v

```bash
ssh admin@192.168.19.139

show run | grep hostname
# Output: hostname RESTCONF-Router-PE

show ip interface brief
# Output:
# GigabitEthernet1  10.255.255.1  up  up
# GigabitEthernet2  192.168.1.1   up  up
# Loopback0         172.16.1.1    up  up

show ip ospf
# Output: Routing Process "ospf 1" with ID 172.16.1.1

exit
```

---

## Stap 11: Log file bekijken

```bash
cat task38_restconf.log
```

---

## FASE 7: AFSLUITEN

## Stap 12: Logout DEVASC

```bash
exit
```

---

## COMPLETE WORKFLOW - SNEL OVERZICHT

### Windows - Git & SCP

```powershell
cd C:\Users\fedor\lab-8-2-automation
git add .
git commit -m "Add Task 38 RESTCONF Python"
git push

cd task38-restconf
scp task38_restconf.py devasc@192.168.19.140:~/task38-restconf/
scp config-restconf.json devasc@192.168.19.140:~/task38-restconf/
scp README.md devasc@192.168.19.140:~/task38-restconf/
```

### DEVASC - Python uitvoeren

```bash
ssh devasc@192.168.19.140
mkdir -p ~/task38-restconf
cd ~/task38-restconf
pip3 install requests
python3 task38_restconf.py
cat task38_restconf.log
exit
```

---

## TROUBLESHOOTING

### Connection refused (poort 443)

Oorzaak: RESTCONF niet enabled
Oplossing op CSR1000v:

```bash
configure terminal
restconf
ip http secure-server
ip http authentication local
exit
write memory
```

### SSL Certificate error

Oorzaak: Self-signed certificaat op CSR1000v
Oplossing: Script gebruikt al `verify=False`

### 401 Unauthorized

Oorzaak: Fout credentials
Oplossing: Check username/password in script (admin/123)

### Module not found: requests

Oplossing:

```bash
pip3 install requests
```

---

## CHECKLIST TASK 38

- [ ] Folder task38-restconf op Windows aangemaakt
- [ ] 3 bestanden geplaatst
- [ ] Git commit gemaakt
- [ ] GitHub gepusht
- [ ] Files via SCP naar DEVASC
- [ ] DEVASC folder verified
- [ ] pip3 install requests uitgevoerd
- [ ] RESTCONF enabled op CSR1000v
- [ ] python3 task38_restconf.py uitgevoerd
- [ ] Output OK
- [ ] Log file OK
- [ ] Device config verified

---

**Task 38 WORKFLOW VOLTOOID!**
