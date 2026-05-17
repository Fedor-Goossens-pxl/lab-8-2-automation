# STAPPENPLAN: VASTE IP ADRES CONFIGUREREN OP CSR1000v

---

## STAP 1: SSH naar router

In PowerShell of terminal:

```bash
ssh admin@192.168.19.139
# Password: 123
```

---

## STAP 2: Configuratie mode inschakelen

Op router console:

```bash
configure terminal
```

Output verwacht:
```
csr1kv(config)#
```

---

## STAP 3: Interface kiezen en IP configureren

Kies de interface (bijv. GigabitEthernet1):

```bash
interface GigabitEthernet1
ip address 192.168.19.139 255.255.255.0
no shutdown
exit
```

Toelichting:
- `interface GigabitEthernet1` - selecteer interface
- `ip address 192.168.19.139 255.255.255.0` - zet IP en netmask
- `no shutdown` - activeer interface
- `exit` - verlaat interface mode

---

## STAP 4: Loopback interface (optioneel)

Voor OSPF/management:

```bash
interface Loopback0
ip address 172.16.1.1 255.255.255.255
no shutdown
exit
```

---

## STAP 5: Hostnaam instellen

```bash
hostname CSR1000v-Router
```

---

## STAP 6: Management SSH configureren

```bash
line vty 0 4
login local
exit
```

---

## STAP 7: Gebruiker aanmaken

```bash
username admin privilege 15 password 123
```

---

## STAP 8: NETCONF SSH enablen

```bash
netconf ssh
```

---

## STAP 9: RESTCONF enablen

```bash
restconf
```

---

## STAP 10: Konfiguratie opslaan

```bash
exit
write memory
```

Output verwacht:
```
Building configuration...
[OK]
```

---

## VERIFICATIE COMMANDO'S

Check configuratie:

```bash
show run interface GigabitEthernet1
# Output:
# interface GigabitEthernet1
#  ip address 192.168.19.139 255.255.255.0
#  no shutdown

show ip interface brief
# Output:
# GigabitEthernet1  192.168.19.139  up  up

show run | grep hostname
# Output: hostname CSR1000v-Router

show run | grep netconf
# Output: netconf ssh

show restconf
# Output: restconf enabled
```

---

## COMPLETE CONFIGURATIE SCRIPT

Zet dit alles in één keer in op router:

```bash
configure terminal

# Interfaces
interface GigabitEthernet1
 description Management Interface
 ip address 192.168.19.139 255.255.255.0
 no shutdown
exit

interface GigabitEthernet2
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit

interface Loopback0
 ip address 172.16.1.1 255.255.255.255
 no shutdown
exit

# Hostname
hostname CSR1000v-Router

# Management
line vty 0 4
 login local
exit

# User
username admin privilege 15 password 123

# NETCONF
netconf ssh

# RESTCONF
restconf

# OSPF (optioneel)
router ospf 1
 network 192.168.19.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
 network 172.16.1.0 0.0.0.255 area 0
exit

# Save
exit
write memory
```

---

## PROBLEMEN OPLOSSEN

### Probleem: Interface stays down

```bash
# Check physical status
show interface GigabitEthernet1
show interface status

# Check cabling
# (fysiek controleren)
```

### Probleem: Cannot SSH

```bash
# Check VTY lines
show run line vty 0 4

# Check user
show run username

# Test IP bereikbaarheid
ping 192.168.19.139 (van Windows)
```

### Probleem: NETCONF/RESTCONF niet bereikbaar

```bash
# Check enabled
show run | grep netconf
show restconf

# Check poorten
show ip http server status

# Enable opnieuw
configure terminal
netconf ssh
restconf
exit
write memory
```

---

## VOORBEELD VOLLEDIGE SETUP

Hieronder een compleet voorbeeld van alle IP configuraties:

```bash
# ===== INTERFACES =====
interface GigabitEthernet1
 description Management - Connected to Windows Host
 ip address 192.168.19.139 255.255.255.0
 no shutdown

interface GigabitEthernet2
 description LAN Interface
 ip address 192.168.1.1 255.255.255.0
 no shutdown

interface Loopback0
 description Loopback for OSPF
 ip address 172.16.1.1 255.255.255.255
 no shutdown

# ===== ROUTING =====
router ospf 1
 network 192.168.19.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
 network 172.16.1.0 0.0.0.255 area 0

# ===== MANAGEMENT =====
hostname CSR1000v-Router
username admin privilege 15 password 123

line vty 0 4
 login local
 transport input ssh

# ===== AUTOMATION PROTOCOLS =====
netconf ssh
restconf
```

---

## STAPPEN SAMENVATTING

1. SSH naar router
2. `configure terminal`
3. Interface IP configureren
4. Hostname zetten
5. SSH user configureren
6. NETCONF enablen
7. RESTCONF enablen
8. `exit` en `write memory`

---

## VERIFICATIE CHECKLIST

- [ ] GigabitEthernet1 heeft IP 192.168.19.139
- [ ] GigabitEthernet2 heeft IP 192.168.1.1
- [ ] Loopback0 heeft IP 172.16.1.1
- [ ] SSH werkt (kan inloggen)
- [ ] NETCONF enabled (show run | grep netconf)
- [ ] RESTCONF enabled (show restconf)
- [ ] Configuratie saved (write memory)
- [ ] Ping werkt van Windows

---

**Na deze configuratie kan je Task 36 en 38 uitvoeren!**

---

## BONUS: HETZELFDE IP OP FYSIEKE ROUTER

### Vraag: Kan ik dezelfde IP adres gebruiken?

**Antwoord: JA, maar met voorzorgen!**

---

## REGEL: IP ADRES HERGEBRUIKEN

### Scenario 1: DEZELFDE IP (Kan probleem geven!)

```
CSR1000v virtueel:    192.168.19.139
Fysieke router:       192.168.19.139 (ZELFDE NETWERK = CONFLICT!)
```

Dit werkt NIET als ze in hetzelfde netwerk actief zijn!

---

### Scenario 2: VERSCHILLENDE NETWERKEN (OK!)

```
CSR1000v virtueel:    192.168.19.139 (netwerk 192.168.19.0/24)
Fysieke router:       10.0.0.139     (netwerk 10.0.0.0/24)
```

Dit werkt prima!

---

### Scenario 3: ZELFDE IP MAAR OFFLINE (OK!)

```
CSR1000v virtueel:    192.168.19.139 (THUIS - OFFLINE)
Fysieke router:       192.168.19.139 (LAB - ONLINE)
```

Dit werkt omdat ze NIET tegelijk actief zijn!

---

## AANBEVELING VOOR DINSDAG PE

Dit is perfect voor jou:

**Thuis (offline):**
- CSR1000v: 192.168.19.139

**Dinsdag op Lab (online):**
- Fysieke router: DEZELFDE IP 192.168.19.139

Omdat CSR1000v thuis offline staat, kan je dezelfde IP gebruiken op de fysieke router zonder conflict!

---

## CONFIGURATIE DINSDAG OP FYSIEKE ROUTER

```bash
configure terminal

interface GigabitEthernet1
 description Management Interface
 ip address 192.168.19.139 255.255.255.0
 no shutdown
exit

interface GigabitEthernet2
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit

interface Loopback0
 ip address 172.16.1.1 255.255.255.255
 no shutdown
exit

hostname NETCONF-Router-PE

username admin privilege 15 password 123

line vty 0 4
 login local
exit

netconf ssh
restconf

router ospf 1
 network 192.168.19.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
 network 172.16.1.0 0.0.0.255 area 0
exit

exit
write memory
```

---

## VOORDELEN DEZELFDE IP GEBRUIKEN

- Geen script aanpassingen nodig
- Dezelfde Task 36/38 scripts werken
- Dezelfde credentials werken
- Consistente configuratie

---

## CHECKLIST DINSDAG PE

- [ ] Ga naar lab (CSR1000v thuis, offline)
- [ ] Pak fysieke router
- [ ] Configureer met dezelfde IP: 192.168.19.139
- [ ] NETCONF/RESTCONF enablen
- [ ] Run Task 36 script
- [ ] Werkt perfect!

---

**Dit is de perfecte setup voor dinsdag!**
