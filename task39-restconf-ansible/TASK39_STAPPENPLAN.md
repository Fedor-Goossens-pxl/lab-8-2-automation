# STAP-VOOR-STAP TASK 39: RESTCONF (Ansible)

Workflow: Windows → Git → SCP → DEVASC → Ansible Execution

---

## FASE 1: WINDOWS - VOORBEREIDING

## Stap 1: Project folder aanmaken

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation
mkdir task39-restconf-ansible
cd task39-restconf-ansible
```

---

## Stap 2: Bestanden plaatsen

Download Task 39 bestanden en plaats in de folder:

1. task39_playbook.yml
2. config-restconf-task39.json
3. README.md

Verificatie:

```powershell
ls
# Output verwacht:
# task39_playbook.yml
# config-restconf-task39.json
# README.md
```

---

## Stap 3: Git commit en push

```powershell
cd C:\Users\fedor\lab-8-2-automation

git add .
git commit -m "Add Task 39 RESTCONF Ansible - Network as Code automation"
git push
```

---

## FASE 2: WINDOWS - SCP NAAR DEVASC

## Stap 4: Kopieer bestanden naar DEVASC

In PowerShell:

```powershell
cd C:\Users\fedor\lab-8-2-automation\task39-restconf-ansible

scp task39_playbook.yml devasc@192.168.19.140:~/task39-restconf-ansible/
scp config-restconf-task39.json devasc@192.168.19.140:~/task39-restconf-ansible/
scp README.md devasc@192.168.19.140:~/task39-restconf-ansible/
```

Output verwacht:

```
task39_playbook.yml            100%  5KB   2.5MB/s   00:00
config-restconf-task39.json    100%  1KB   500KB/s   00:00
README.md                      100%  3KB   800KB/s   00:00
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
mkdir -p ~/task39-restconf-ansible
cd ~/task39-restconf-ansible

ls
# Output verwacht:
# task39_playbook.yml
# config-restconf-task39.json
# README.md
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

Als RESTCONF niet enabled is:

```bash
configure terminal
restconf
ip http secure-server
ip http authentication local
exit
write memory
```

---

## FASE 5: DEVASC - ANSIBLE EXECUTION

## Stap 9: Syntax check

Op DEVASC:

```bash
cd ~/task39-restconf-ansible

ansible-playbook task39_playbook.yml --syntax-check
```

Output verwacht:

```
playbook: task39_playbook.yml
```

---

## Stap 10: Dry-run (niets verandert!)

```bash
ansible-playbook task39_playbook.yml --check
```

---

## Stap 11: Werkelijk playbook uitvoeren

```bash
ansible-playbook task39_playbook.yml
```

Output verwacht:

```
PLAY [Task 39 - RESTCONF IOS-XE Automation with Ansible]

TASK [Load JSON configuration from file]
ok: [localhost]

TASK [Display configuration loaded]
ok: [localhost] => {
    "msg": "Configuration file loaded successfully"
}

TASK [Test RESTCONF connectivity]
ok: [localhost]

TASK [Display connectivity status]
ok: [localhost] => {
    "msg": "RESTCONF connectivity: OK"
}

TASK [Configure hostname]
ok: [localhost]

TASK [Display hostname result]
ok: [localhost] => {
    "msg": "Hostname configured: RESTCONF-Router-PE"
}

TASK [Configure GigabitEthernet1]
ok: [localhost]

TASK [Configure GigabitEthernet2]
ok: [localhost]

TASK [Configure Loopback0]
ok: [localhost]

TASK [Configure OSPF routing]
ok: [localhost]

TASK [Verify hostname via RESTCONF GET]
ok: [localhost]

TASK [Display verification result]
ok: [localhost] => {
    "msg": "Verified hostname: RESTCONF-Router-PE"
}

TASK [Save results to log file]
changed: [localhost]

TASK [Task 39 completed]
ok: [localhost] => {
    "msg": "Task 39 RESTCONF Ansible Automation Completed Successfully!"
}

PLAY RECAP
localhost : ok=14 changed=1 unreachable=0 failed=0
```

---

## Stap 12: Log file bekijken

```bash
cat task39_results.log
```

Output verwacht:

```
Task 39 RESTCONF Ansible Automation - Results
=============================================

Configuration Loading  : SUCCESS
RESTCONF Connectivity  : SUCCESS
Hostname configured    : RESTCONF-Router-PE
GigabitEthernet1       : 10.255.255.1
GigabitEthernet2       : 192.168.1.1
Loopback0              : 172.16.1.1
OSPF                   : Process 1 - Area 0
Verification           : RESTCONF-Router-PE

Status: COMPLETE
```

---

## FASE 6: DEVASC - DEVICE VERIFICATIE

## Stap 13: Verificatie op CSR1000v

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

## FASE 7: AFSLUITEN

## Stap 14: Logout DEVASC

```bash
exit
```

---

## COMPLETE WORKFLOW - SNEL OVERZICHT

### Windows - Git & SCP

```powershell
cd C:\Users\fedor\lab-8-2-automation
git add .
git commit -m "Add Task 39 RESTCONF Ansible"
git push

cd task39-restconf-ansible
scp task39_playbook.yml devasc@192.168.19.140:~/task39-restconf-ansible/
scp config-restconf-task39.json devasc@192.168.19.140:~/task39-restconf-ansible/
scp README.md devasc@192.168.19.140:~/task39-restconf-ansible/
```

### DEVASC - Ansible uitvoeren

```bash
ssh devasc@192.168.19.140
mkdir -p ~/task39-restconf-ansible
cd ~/task39-restconf-ansible

ansible-playbook task39_playbook.yml --syntax-check
ansible-playbook task39_playbook.yml

cat task39_results.log
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

Oorzaak: Self-signed certificaat
Oplossing: Playbook gebruikt al `validate_certs: no`

### 401 Unauthorized

Oorzaak: Fout credentials
Oplossing: Check vars in playbook:
```yaml
restconf_user: "admin"
restconf_password: "123"
```

### JSON parse error

Oorzaak: Syntax error in config-restconf-task39.json
Oplossing:

```bash
python3 -c "import json; json.load(open('config-restconf-task39.json')); print('JSON OK')"
```

---

## CHECKLIST TASK 39

- [ ] Folder task39-restconf-ansible op Windows aangemaakt
- [ ] 3 bestanden geplaatst
- [ ] Git commit gemaakt
- [ ] GitHub gepusht
- [ ] Files via SCP naar DEVASC
- [ ] DEVASC folder verified
- [ ] Ansible geinstalleerd
- [ ] RESTCONF enabled op CSR1000v
- [ ] Syntax check OK
- [ ] Playbook uitgevoerd
- [ ] Log file OK
- [ ] Device config verified

---

**Task 39 WORKFLOW VOLTOOID!**
