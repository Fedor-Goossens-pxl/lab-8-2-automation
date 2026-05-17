# TASK 39: RESTCONF (Ansible) - Network as Code

Automatiseer Cisco IOS-XE configuratie met Ansible en RESTCONF via de `uri` module.

Student: Fedor Goossens
Klas: 2SNEb
Opleiding: Graduaat Systeem en Netwerkbeheer
Datum: Mei 2026

---

## Overzicht

Task 39 implementeert infrastructure as code met Ansible playbooks via RESTCONF.
In plaats van NETCONF (Task 37) gebruikt dit playbook HTTP/HTTPS calls via de
Ansible `uri` module.

Vergelijking van de 4 tasks:

| Task | Protocol | Tool    | Library/Module |
|------|----------|---------|----------------|
| 36   | NETCONF  | Python  | ncclient       |
| 37   | NETCONF  | Ansible | netconf_config |
| 38   | RESTCONF | Python  | requests       |
| 39   | RESTCONF | Ansible | uri            |

---

## Vereisten (LAB 8.2)

- Ansible 2.9+
- Python 3.6+
- RESTCONF enabled op IOS-XE device
- HTTPS poort 443 bereikbaar

---

## Projectstructuur

```
task39-restconf-ansible/
├── task39_playbook.yml          # Ansible playbook
├── config-restconf-task39.json  # JSON configuratie
└── README.md                    # Dit bestand
```

---

## Werking

Het playbook voert deze stappen uit:

1. JSON configuratie inladen uit bestand
2. RESTCONF connectiviteit testen (GET)
3. Hostname configureren (PUT)
4. GigabitEthernet1 configureren (PUT)
5. GigabitEthernet2 configureren (PUT)
6. Loopback0 configureren (PUT)
7. OSPF routing configureren (PUT)
8. Verificatie via RESTCONF GET
9. Resultaten opslaan in log

---

## Ansible uri Module

De `uri` module stuurt HTTP requests:

```yaml
- name: Configure hostname
  uri:
    url: "https://192.168.19.139:443/restconf/data/Cisco-IOS-XE-native:native/hostname"
    method: PUT
    user: admin
    password: "123"
    force_basic_auth: yes
    validate_certs: no
    body_format: json
    body:
      Cisco-IOS-XE-native:hostname: "RESTCONF-Router-PE"
    status_code: [200, 204]
```

---

## RESTCONF URL Structuur

```
https://<host>:443/restconf/data/<yang-model>:<path>
```

Voorbeelden:

```
# Hostname
https://192.168.19.139:443/restconf/data/Cisco-IOS-XE-native:native/hostname

# Interface
https://192.168.19.139:443/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1

# OSPF
https://192.168.19.139:443/restconf/data/Cisco-IOS-XE-native:native/router/ospf=1
```

---

## Uitvoeren op DEVASC

```bash
cd ~/task39-restconf-ansible

ansible-playbook task39_playbook.yml
```

---

## Device voorbereiding

RESTCONF moet enabled zijn op CSR1000v:

```bash
configure terminal
restconf
ip http secure-server
ip http authentication local
exit
write memory
```

---

## Git workflow

```bash
# Op Windows
git add .
git commit -m "Add Task 39 RESTCONF Ansible automation"
git push
```

---

*Task 39 voldoet aan alle vereisten van LAB 8.2 - IOS-XE Automation met Ansible en RESTCONF.*
