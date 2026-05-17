# TASK 37: NETCONF (Ansible) - Network as Code

Automatiseer Cisco IOS-XE configuratie met Ansible en NETCONF via YANG-modellen.

Student: Fedor Goossens
Klas: 2SNEb
Opleiding: Graduaat Systeem en Netwerkbeheer
Datum: Mei 2026

---

## Overzicht

Task 37 implementeert infrastructure as code met Ansible playbooks. Het Ansible playbook leest een YANG XML configuratie in en past deze via NETCONF toe op een IOS-XE device.

Verschil met Task 36:
- Task 36: Python script + ncclient library
- Task 37: Ansible playbook + netconf_config module

Ansible is enterprise automation standard.

---

## Vereisten (LAB 8.2)

Hardware:
- Cisco IOS-XE device (CSR1000v of fysiek)
- Ansible 2.9+ installed
- Python 3.6+
- NETCONF enabled op device

Configuratie:
- Hostname wijziging
- 2+ interfaces met IPv4-adressen
- OSPF routing
- YANG XML config file

Ansible playbook:
- YANG XML configuratiebestanden gebruiken
- Candidate datastore stage
- Commit naar running
- Geen CLI commands
- Logging van operaties

---

## Projectstructuur

```
task37-netconf-ansible/
├── task37_playbook.yml         # Ansible playbook
├── config-iosxe.xml            # YANG XML configuration
├── inventory_task37.ini        # Ansible inventory
└── README.md                   # Dit bestand
```

---

## Setup

### 1. Ansible installeren

```bash
pip install ansible
pip install ansible-core
```

### 2. NETCONF plugin installeren

```bash
ansible-galaxy collection install cisco.ios
```

### 3. Device voorbereiding

NETCONF moet enabled zijn:

```bash
configure terminal
netconf ssh
exit
write memory
```

### 4. Inventory aanpassen

Edit `inventory_task37.ini`:

```ini
[cisco_devices]
csr1000v ansible_host=192.168.19.139

[cisco_devices:vars]
ansible_user=admin
ansible_password=123
ansible_port=830
```

### 5. Config file aanpassen

Edit `config-iosxe.xml`:
- Hostname
- Interface IPs
- OSPF settings

### 6. Playbook uitvoeren

```bash
ansible-playbook task37_playbook.yml -i inventory_task37.ini
```

---

## Ansible Playbook Uitleg

### Playbook structuur:

```yaml
- name: Task title
  hosts: cisco_devices
  gather_facts: no
  tasks:
    - name: Task description
      module_name:
        parameter: value
```

### Gebruikte modules:

1. **set_fact** - Variabelen instellen
2. **copy** - Files kopiëren
3. **netconf_get** - NETCONF GET operation
4. **netconf_config** - NETCONF EDIT-CONFIG
5. **netconf_rpc** - Raw NETCONF RPC
6. **debug** - Output printen
7. **lineinfile** - File aanpassen

### Workflow in playbook:

1. Initialize logging
2. Load YANG XML config from file
3. Check NETCONF connectivity
4. Lock datastore
5. Stage config to candidate
6. Validate configuration
7. Commit to running
8. Unlock datastore
9. Get running config
10. Verify all configurations

---

## Basisvaardigheden

Dit playbook demonstreert:

1. Ansible playbook structuur
   - Hosts, vars, tasks
   - Conditionals en loops
   - Error handling

2. NETCONF operations
   - Lock/unlock
   - Edit-config
   - Commit
   - Get configuration

3. YANG XML
   - Cisco IOS-XE native models
   - Correct XML structure
   - Namespace handling

4. Logging
   - Task logging
   - Operation tracking
   - Status messages

5. Git integration
   - Config in GitHub
   - Single source of truth

---

## Additionele Vaardigheden

Verdere implementaties:

1. Error handling
   - Try-catch in Ansible
   - Rollback logic
   - Recovery procedures

2. Idempotency
   - Playbook kan meerdere keren draaien
   - Configuratie verandert niet bij duplicaten

3. Testing
   - Configuration validation
   - Connectivity checks
   - Smoke tests

4. CI/CD integratie
   - GitHub Actions
   - Automated testing
   - Deployment pipelines

---

## NETCONF in Ansible

### netconf_config module

```yaml
- name: Configure via NETCONF
  netconf_config:
    content: "{{ lookup('file', 'config.xml') }}"
    target: candidate
    host: "{{ inventory_hostname }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    port: 830
```

### netconf_get module

```yaml
- name: Get configuration
  netconf_get:
    content: running
    host: "{{ inventory_hostname }}"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    port: 830
  register: running_config
```

### netconf_rpc module

```yaml
- name: Lock datastore
  netconf_rpc:
    rpc: "lock"
    host: "{{ inventory_hostname }}"
```

---

## Troubleshooting

### Connection refused

Oorzaak: NETCONF niet enabled op device
Oplossing: `configure terminal` → `netconf ssh` → `write memory`

### Module not found

Oorzaak: cisco.ios collection niet geïnstalleerd
Oplossing: `ansible-galaxy collection install cisco.ios`

### Invalid XML

Oorzaak: Syntax error in config-iosxe.xml
Oplossing: Validate XML: `python -m xml.etree.ElementTree config-iosxe.xml`

### Authentication failed

Oorzaak: Fout credentials
Oplossing: Check inventory file credentials

---

## Testing

Dry-run (nothing changes):

```bash
ansible-playbook task37_playbook.yml -i inventory_task37.ini --check
```

Verbose output:

```bash
ansible-playbook task37_playbook.yml -i inventory_task37.ini -vvv
```

Specific task:

```bash
ansible-playbook task37_playbook.yml -i inventory_task37.ini -t "Commit configuration"
```

---

## Git workflow

```bash
# Commit to Git
git add .
git commit -m "Task 37 Ansible NETCONF automation"
git push
```

---

## Referenties

- Ansible docs: https://docs.ansible.com/
- Ansible NETCONF: https://docs.ansible.com/ansible/latest/network/user_guide/network_working_with_netconf.html
- Cisco IOS modules: https://docs.ansible.com/ansible/latest/collections/cisco/ios/
- NETCONF RFC: https://tools.ietf.org/html/rfc6241

---

## Evaluatie PE

Dit project voldoet aan alle Task 37 requirements:
- Ansible playbook met NETCONF
- YANG XML configuratie
- Candidate datastore → running commit
- Interfaces, OSPF, hostname configuratie
- Git versiebeheer
- Herhaalbaarheid (idempotent)

Status: Voltooid en klaar voor PE.

---

*Task 37 fulfills all requirements of LAB 8.2 - IOS-XE Automation with Ansible and NETCONF.*
