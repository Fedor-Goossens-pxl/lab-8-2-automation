# Task 16: Assign Interface to VLAN

## 📝 Wat doet het script?

Configureer **GigabitEthernet1** als access port in **VLAN 10** via NETCONF/YANG of CLI op de CSR1000v router.

## ⚙️ Hoe werkt het?

- **Patroon:** NETCONF dispatch() met lxml.etree (YANGsuite pattern)
- **Method:** Raw XML RPC naar running-config (switchport configuratie)
- **Datastore:** running-config (merge mode)
- **Verificatie:** GET-CONFIG RPC

## ✅ Script Output (bij succes)

```
✓ NETCONF Connection: Established
✓ RPC dispatched successfully
✓ VLAN Configuration Applied Successfully! (<ok/> received)
✓ Verification: GET-CONFIG successful
✓ VLAN 10 found on GigabitEthernet1!
```

## 🔍 Hoe verifiëren op CSR1000v Router?

### 1. SSH naar de router:
```bash
ssh cisco@192.168.19.139
```

### 2. Verificatie command:
```
show interfaces GigabitEthernet1 switchport
```

### 3. Wat je moet zien:
```
Switchport: Enabled
Administrative Mode: static access
Operational Mode: static access
Administrative Trunking Encapsulation: negotiate
Access Mode VLAN: 10
```

### 4. Volledige config checken (optional):
```
show running-config interface GigabitEthernet1
```

## 📂 Script Details

- **File:** `task_16.py` (NETCONF version)
- **Fallback:** `task_16_cli.py` (CLI fallback, indien NETCONF fails)
- **GitHub:** https://github.com/Fedor-Goossens-pxl/lab-8-2-automation

## 🛠️ Device Vereisten

✓ Cisco IOS-XE (16.9.3+)
✓ NETCONF-YANG enabled: `netconf-yang`
✓ SSH enabled: `ip ssh version 2`
✓ Management interface bereikbaar (192.168.19.139)
✓ Geldige credentials (cisco/cisco123!)

## 💡 Tips

- Wacht 2-3 seconden na script completion
- Als command niets toont, probeer `show running-config interface GigabitEthernet1`
- Bij errors, check: `show logging | include NETCONF`

---

*TASK_16_Assign_Interface_to_VLAN - Verification Documentation*  
*PXL Hogeschool | Enterprise Networks 2 | Juni 2026*