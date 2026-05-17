# STAP-VOOR-STAP TASK 37: NETCONF (Ansible)

Workflow: Windows → Git → SCP → DEVASC → Ansible Execution

---

## FASE 1: WINDOWS - VOORBEREIDING

## Stap 1: Project folder aanmaken

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation
mkdir task37-netconf-ansible
cd task37-netconf-ansible
```

---

## Stap 2: Bestanden plaatsen

Download Task 37 bestanden en plaats in `C:\Users\fedor\lab-8-2-automation\task37-netconf-ansible\`:

1. task37_playbook.yml
2. config-iosxe-task37.xml (rename naar config-iosxe.xml)
3. inventory_task37.ini
4. TASK37_README.md (rename naar README.md)

Verificatie:

```powershell
ls
# Output verwacht:
# task37_playbook.yml
# config-iosxe.xml
# inventory_task37.ini
# README.md
```

---

## Stap 3: Git commit

```powershell
cd C:\Users\fedor\lab-8-2-automation

git add .
git commit -m "Add Task 37 NETCONF Ansible - Network as Code automation"
git push
```

Output verwacht:

```
[main xxxxx] Add Task 37 NETCONF Ansible
 4 files changed, 350 insertions(+)
 create mode 100644 task37-netconf-ansible/task37_playbook.yml
 create mode 100644 task37-netconf-ansible/config-iosxe.xml
 create mode 100644 task37-netconf-ansible/inventory_task37.ini
 create mode 100644 task37-netconf-ansible/README.md

Enumerating objects: 8, done.
Writing objects: 100% (8/8), 7.55 KiB
To https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
   xxxx -> main
```

---

## FASE 2: WINDOWS - SCP NAAR DEVASC

## Stap 4: Kopieer folder naar DEVASC

In PowerShell (blijf in dezelfde folder):

```powershell
cd C:\Users\fedor\lab-8-2-automation\task37-netconf-ansible

scp task37_playbook.yml devasc@192.168.19.140:~/task37-netconf-ansible/
scp config-iosxe-task37.xml devasc@192.168.19.140:~/task37-netconf-ansible/
scp inventory_task37.ini devasc@192.168.19.140:~/task37-netconf-ansible/
scp README.md devasc@192.168.19.140:~/task37-netconf-ansible/
```

Output verwacht:

```
task37_playbook.yml              100%  15KB   2.5MB/s   00:00
config-iosxe.xml                 100%  2.1KB  500KB/s   00:00
inventory_task37.ini             100%  0.5KB  250KB/s   00:00
README.md                        100%  5.0KB  800KB/s   00:00
```

---

## FASE 3: DEVASC - VOORBEREIDING

## Stap 5: SSH naar DEVASC

In PowerShell:

```powershell
ssh devasc@192.168.19.140
# Password: (voer wachtwoord in)
```

---

## Stap 6: Verify files aangekomen

Op DEVASC (bash):

```bash
mkdir ~/task37-netconf-ansible/
ls ~/task37-netconf-ansible/
# Output verwacht:
# config-iosxe.xml
# inventory_task37.ini
# README.md
# task37_playbook.yml
```

---

## Stap 7: Ansible installeren op DEVASC

```bash
sudo apt-get update
sudo apt-get install ansible -y
```

Verificatie:

```bash
ansible --version
# Output: ansible [core 2.x.x]
```

---

## Stap 8: Cisco IOS collection installeren

```bash
ansible-galaxy collection install cisco.ios
```

Output verwacht:

```
Process install dependency map
Starting collection install process
Installing 'cisco.ios:x.x.x'
```

---

## FASE 4: DEVASC - VOORBEREIDING DEVICE

## Stap 9: Device NETCONF verificatie

```bash
ssh admin@192.168.19.139
# (op CSR1000v)
show run | grep netconf
# Output: netconf ssh

exit
```

---

## FASE 5: DEVASC - ANSIBLE EXECUTION

## Stap 10: Syntax check playbook

Op DEVASC (in task37-netconf-ansible folder):

```bash
cd ~/task37-netconf-ansible
ansible-playbook task37_playbook.yml --syntax-check
```

Output verwacht:

```
playbook loaded successfully
```

---

## Stap 11: Dry-run (niets verandert!)

```bash
ansible-playbook task37_playbook.yml -i inventory_task37.ini --check
```

Output verwacht:

```
PLAY [Task 37 - NETCONF IOS-XE Automation with Ansible]

TASK [Initialize log file]
ok: [csr1000v]

TASK [Load YANG XML configuration]
ok: [csr1000v]

...

PLAY RECAP
csr1000v : ok=10 changed=0 unreachable=0 failed=0
```

---

## Stap 12: Werkelijk playbook uitvoeren

```bash
ansible-playbook task37_playbook.yml -i inventory_task37.ini
```

Output verwacht:

```
PLAY [Task 37 - NETCONF IOS-XE Automation with Ansible]

TASK [Initialize log file]
ok: [csr1000v]

TASK [Load YANG XML configuration]
ok: [csr1000v]

TASK [Check NETCONF connectivity]
ok: [csr1000v]

TASK [Stage configuration to candidate datastore]
changed: [csr1000v]

TASK [Commit configuration to running datastore]
changed: [csr1000v]

TASK [Get running configuration]
ok: [csr1000v]

...

PLAY RECAP
csr1000v : ok=10 changed=2 unreachable=0 failed=0
```

---

## Stap 13: Log file bekijken

```bash
cat task37_netconf.log
```

Output bevat:

```
TASK 37: NETCONF (Ansible) - Network as Code
STAP 1: Configuratie ingeladen
STAP 2: NETCONF Connectiviteit
STAP 3: Edit-config naar CANDIDATE DATASTORE
STAP 4: Configuratie Validatie
STAP 5: Commit naar RUNNING DATASTORE
STAP 6: Verificatie - Running Config Opgehaald
STAP 7: Configuratie Verificatie
TASK 37 VOLTOOID - Network as Code succesvol!
```

---

## FASE 6: DEVASC - DEVICE VERIFICATIE

## Stap 14: Verificatie op device

Op DEVASC:

```bash
ssh admin@192.168.19.139
# (op CSR1000v)

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

## FASE 7: DEVASC - AFSLUITEN

## Stap 15: Logout DEVASC

```bash
exit
```

---

## COMPLETE WORKFLOW COMMANDS

### Windows - Git & SCP
```powershell
cd C:\Users\fedor\lab-8-2-automation
git add .
git commit -m "Add Task 37 NETCONF Ansible"
git push

cd task37-netconf-ansible
scp *.yml devasc@192.168.19.140:~/task37-netconf-ansible/
scp *.xml devasc@192.168.19.140:~/task37-netconf-ansible/
scp *.ini devasc@192.168.19.140:~/task37-netconf-ansible/
scp *.md devasc@192.168.19.140:~/task37-netconf-ansible/
```

### DEVASC - Ansible
```bash
ssh devasc@192.168.19.140
cd ~/task37-netconf-ansible

sudo apt-get update && sudo apt-get install ansible -y
ansible-galaxy collection install cisco.ios

ansible-playbook task37_playbook.yml -i inventory_task37.ini
cat task37_netconf.log

exit
```

---

## CHECKLIST TASK 37

- [ ] Folder task37-netconf-ansible op Windows aangemaakt
- [ ] 4 bestanden geplaatst
- [ ] Git commit gemaakt
- [ ] GitHub pushed
- [ ] Files via SCP naar DEVASC
- [ ] DEVASC folder verified
- [ ] Ansible geïnstalleerd op DEVASC
- [ ] cisco.ios collection geïnstalleerd
- [ ] NETCONF enabled op CSR1000v
- [ ] Syntax check OK
- [ ] Dry-run succesful
- [ ] Playbook executed
- [ ] Log file OK
- [ ] Device config verified

---

**Task 37 WORKFLOW VOLTOOID!**
