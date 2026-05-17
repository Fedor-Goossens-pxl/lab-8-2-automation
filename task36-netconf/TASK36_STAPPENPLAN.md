# STAP-VOOR-STAP TASK 36: NETCONF (Python)

Workflow: Windows → Git → SCP → DEVASC → Python Execution

---

## FASE 1: WINDOWS - VOORBEREIDING

## Stap 1: Project folder aanmaken

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation
mkdir task36-netconf
cd task36-netconf
```

---

## Stap 2: Bestanden plaatsen

Download Task 36 bestanden en plaats in `C:\Users\fedor\lab-8-2-automation\task36-netconf\`:

1. task36_netconf.py
2. config-iosxe.xml
3. README.md

Verificatie:

```powershell
ls
# Output verwacht:
# task36_netconf.py
# config-iosxe.xml
# README.md
```

---

## Stap 3: Git commit en push

```powershell
cd C:\Users\fedor\lab-8-2-automation

git add .
git commit -m "Add Task 36 NETCONF Python - Network as Code automation"
git push
```

Output verwacht:

```
[main xxxxx] Add Task 36 NETCONF Python
 3 files changed
 create mode 100644 task36-netconf/task36_netconf.py
 create mode 100644 task36-netconf/config-iosxe.xml
 create mode 100644 task36-netconf/README.md

To https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
   xxxx -> main
```

---

## FASE 2: WINDOWS - SCP NAAR DEVASC

## Stap 4: Kopieer bestanden naar DEVASC

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation\task36-netconf

scp task36_netconf.py devasc@192.168.19.140:~/task36-netconf/
scp config-iosxe.xml devasc@192.168.19.140:~/task36-netconf/
scp README.md devasc@192.168.19.140:~/task36-netconf/
```

Output verwacht:

```
task36_netconf.py         100%  10KB   2.5MB/s   00:00
config-iosxe.xml          100%   2KB   500KB/s   00:00
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
mkdir -p ~/task36-netconf
cd ~/task36-netconf

ls
# Output verwacht:
# task36_netconf.py
# config-iosxe.xml
# README.md
```

---

## Stap 7: Python libraries installeren op DEVASC

```bash
pip3 install ncclient
```

Verificatie:

```bash
pip3 show ncclient
# Output: Name: ncclient, Version: 0.x.x
```

---

## FASE 4: DEVASC - DEVICE VOORBEREIDING

## Stap 8: Verify NETCONF op CSR1000v

```bash
ssh admin@192.168.19.139

show run | include netconf
# Output: netconf ssh

exit
```

Als NETCONF niet enabled is:

```bash
configure terminal
netconf ssh
exit
write memory
```

---

## FASE 5: DEVASC - PYTHON EXECUTION

## Stap 9: Script uitvoeren

Op DEVASC in task36-netconf folder:

```bash
cd ~/task36-netconf
python3 task36_netconf.py
```

Output verwacht:

```
======================================================================
TASK 36: NETCONF (Python) - Network as Code
======================================================================

STAP 1: Configuratie ingeladen uit config-iosxe.xml

STAP 2: Verbinding maken met CSR1000v via NETCONF (poort 830)...
Verbinding succesvol!

STAP 3: Edit-config naar candidate datastore...
Edit-config succesvol!

STAP 4: Commit naar running datastore...
Commit succesvol!

STAP 5: Configuratie verifiëren...
Hostname: NETCONF-Router-PE
GigabitEthernet1 IP: 10.255.255.1
GigabitEthernet2 IP: 192.168.1.1
Loopback0 IP: 172.16.1.1

======================================================================
TASK 36 VOLTOOID - Network as Code succesvol!
======================================================================
```

---

## FASE 6: DEVASC - DEVICE VERIFICATIE

## Stap 10: Verificatie op CSR1000v

```bash
ssh admin@192.168.19.139

show run | grep hostname
# Output: hostname NETCONF-Router-PE

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
cat task36_netconf.log
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
git commit -m "Add Task 36 NETCONF Python"
git push

cd task36-netconf
scp task36_netconf.py devasc@192.168.19.140:~/task36-netconf/
scp config-iosxe.xml devasc@192.168.19.140:~/task36-netconf/
scp README.md devasc@192.168.19.140:~/task36-netconf/
```

### DEVASC - Python uitvoeren

```bash
ssh devasc@192.168.19.140
mkdir -p ~/task36-netconf
cd ~/task36-netconf
pip3 install ncclient
python3 task36_netconf.py
cat task36_netconf.log
exit
```

---

## TROUBLESHOOTING

### Connection refused (poort 830)

Oorzaak: NETCONF niet enabled
Oplossing op CSR1000v:

```bash
configure terminal
netconf ssh
exit
write memory
```

### ncclient not found

Oplossing:

```bash
pip3 install ncclient
```

### XML parse error

Oorzaak: Syntax error in config-iosxe.xml
Oplossing:

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('config-iosxe.xml'); print('XML OK')"
```

### Authentication failed

Oorzaak: Fout credentials
Oplossing: Check in script: host=192.168.19.139, username=admin, password=123

---

## CHECKLIST TASK 36

- [ ] Folder task36-netconf op Windows aangemaakt
- [ ] 3 bestanden geplaatst
- [ ] Git commit gemaakt
- [ ] GitHub gepusht
- [ ] Files via SCP naar DEVASC
- [ ] DEVASC folder verified
- [ ] pip3 install ncclient uitgevoerd
- [ ] NETCONF enabled op CSR1000v (poort 830)
- [ ] python3 task36_netconf.py uitgevoerd
- [ ] Output OK
- [ ] Log file OK
- [ ] Device config verified

---

**Task 36 WORKFLOW VOLTOOID!**
