# TASK 38: RESTCONF (Python) - Network as Code

Task 38 automatiseert Cisco IOS-XE configuratie via RESTCONF protocol met Python.

Student: Fedor Goossens
Klas: 2SNEb
Opleiding: Graduaat Systeem en Netwerkbeheer
Datum: Mei 2026

---

## Overzicht

Task 38 implementeert end-to-end RESTCONF automatisering. Het Python script haalt een JSON configuratie op en past deze toe op een IOS-XE device via REST API calls.

Verschil met Task 36:
- Task 36: NETCONF (SSH poort 830)
- Task 38: RESTCONF (HTTPS poort 443)

RESTCONF is HTTP-based en waarschijnlijk beter ondersteund op oudere IOS-XE versies.

---

## Vereisten (LAB 8.2)

Hardware:
- Cisco IOS-XE device (CSR1000v of fysiek)
- Python 3.6+ met requests library
- Git voor versiebeheer
- RESTCONF enabled op device

Configuratie:
- Hostname wijziging
- 2+ interfaces met IPv4-adressen
- OSPF routing

Python script:
- Inladen config uit JSON bestand (GitHub simulatie)
- RESTCONF PUT/PATCH requests
- HTTP status codes controleren (200, 201, 204, 4xx, 5xx)
- Logging van successen en fouten
- JSON pretty-printing

---

## Projectstructuur

```
task38-restconf/
├── task38_restconf.py      # RESTCONF automation script
├── config-restconf.json    # JSON YANG configuratie
└── README.md               # Dit bestand
```

---

## Setup

### 1. Device voorbereiding

RESTCONF is meestal standaard enabled op moderne IOS-XE versies. Controleer:

```
csr1kv# show restconf
RestAPI enabled
```

### 2. Environment setup

```bash
pip install requests
```

### 3. Script configuratie

Edit task38_restconf.py:

```python
DEVICE_HOST = "192.168.19.139"      # Device IP
DEVICE_PORT = 443
DEVICE_USERNAME = "admin"
DEVICE_PASSWORD = "123"
```

### 4. Uitvoering

```bash
python task38_restconf.py
```

Verwachte output:

```
TASK 38: RESTCONF (Python) - Network as Code
======================================================================

STAP 1: Configuratie inladen
Configuratie ingeladen uit: config-restconf.json

STAP 2: Controleer RESTCONF connectiviteit
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

STAP 6: Verificatie
Running configuration opgehaald (HTTP 200)
[JSON output van huidige config]

TASK 38 VOLTOOID - Network as Code succesvol!
======================================================================
```

---

## Basisvaardigheden

Dit script demonstreert alle basisvaardigheden:

1. Python gebruik (requests library)
   - HTTP PUT/PATCH requests
   - JSON parsing en pretty-printing
   - Exception handling

2. HTTP statusinformatie
   - Status code checking (200, 201, 204, 4xx, 5xx)
   - Error response logging
   - Success verification

3. Git versiebeheer
   - Local repository
   - Commits met naam
   - Single source of truth

4. End-to-end automatisatie
   - Config inladen
   - RESTCONF requests
   - Verificatie

---

## Additionele vaardigheden

Verdere implementaties:

- Idempotency: script kan meerdere keren gerund worden
- Error recovery: fout handling met try-except
- Logging: alle operaties gelogd
- JSON validatie: JSON schema checking
- Device capabilities check

---

## RESTCONF Basics

### Wat is RESTCONF?

RESTCONF is een HTTP-based protocol voor YANG configuratie.

Voordelen:
- HTTP/HTTPS (standaard poort 443)
- JSON support
- Geen SSH nodig
- RESTful principles

### RESTCONF URL's

```
GET    /restconf/data/[path]           - Read config/state
PUT    /restconf/data/[path]           - Replace config
PATCH  /restconf/data/[path]           - Modify config
DELETE /restconf/data/[path]           - Delete config
POST   /restconf/data/[path]           - Create entry
```

### HTTP Headers

```python
RESTCONF_HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
```

### Authenticatie

```python
auth = HTTPBasicAuth(username, password)
response = requests.put(url, auth=auth, ...)
```

---

## Troubleshooting

### Connection refused

Oorzaken:
- RESTCONF niet enabled
- Poort 443 blokkeert
- SSL certificate issue

Oplossing:
- Check: `show restconf`
- Enable: `restconf`
- Verify poort: `show ip http server status`

### JSON parsing error

Oorzaken:
- Ongeldige JSON in config-restconf.json
- Ongeldige response van device

Oplossing:
- Validate JSON: `python -m json.tool config-restconf.json`
- Check response logging in script

### HTTP 400/401

Oorzaken:
- Ongeldige credentials
- Ongeldige YANG path
- Ongeldige JSON payload

Oplossing:
- Check credentials
- Validate YANG path in script
- Pretty-print payload voor debugging

### HTTP 404

Oorzaken:
- YANG model niet ondersteund
- Verkeerde path

Oplossing:
- Check device capabilities: `/restconf/data/ietf-yang-library:modules-state`
- Verify YANG paths

---

## Git workflow

```bash
# Setup
git config --global user.name "Fedor Goossens"
git config --global user.email "fedor.goossens@student.pxl.be"

# Commit
git add .
git commit -m "Task 38 RESTCONF implementation"

# Push naar GitHub
git push origin main
```

---

## Testing

Handmatig testen met curl:

```bash
# Test connectiviteit
curl -k -u admin:123 \
  -H "Accept: application/yang-data+json" \
  https://192.168.19.139:443/restconf/data/ietf-yang-library:modules-state

# Test hostname config
curl -k -u admin:123 \
  -H "Content-Type: application/yang-data+json" \
  -X PUT \
  -d '{"Cisco-IOS-XE-native:hostname": "TEST-ROUTER"}' \
  https://192.168.19.139:443/restconf/data/Cisco-IOS-XE-native:native/hostname
```

---

## Referenties

- Requests library: https://requests.readthedocs.io/
- RESTCONF RFC: https://tools.ietf.org/html/rfc8040
- Cisco RESTCONF: https://developer.cisco.com/
- YANG Models: https://github.com/YangModels/yang

---

## Evaluatie PE

Dit project voldoet aan alle Task 38 requirements:
- RESTCONF protocol
- JSON YANG configuration
- HTTP status checking
- Error handling
- Git versiebeheer
- Idempotent en herhaalbaar

Status: Voltooid en klaar voor PE demonstratie.

---

*Task 38 fulfills all requirements of LAB 8.2 - IOS-XE Automation with RESTCONF and YANG models.*
