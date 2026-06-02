# Task 02 Enable Disable Interface

## 📝 Wat doet het script?

Configureer deze NETCONF/YANG setting op de CSR1000v router.

## ⚙️ Hoe werkt het?

- **Patroon:** NETCONF dispatch() met lxml.etree (YANGsuite pattern)
- **Method:** Raw XML RPC naar running-config
- **Datastore:** running-config (merge mode)
- **Verificatie:** GET-CONFIG RPC

## ✅ Script Output (bij succes)

```
✓ NETCONF Connection: Established
✓ RPC dispatched successfully
✓ Configuration Applied Successfully! (<ok/> received)
✓ Verification: GET-CONFIG successful
```

## 🔍 Hoe verifiëren op CSR1000v Router?

### 1. SSH naar de router:
```bash
ssh cisco@192.168.19.139
```

### 2. Verificatie command:
```
show interface status
```

### 3. Wat je moet zien:
Controleer of interface 'up' of 'down' staat

### 4. Volledige config checken (optional):
```
show running-config
```

## 📂 Script Details

- **File:** `task_2.py` (NETCONF version)
- **Fallback:** `task_2_cli.py` (CLI fallback, indien NETCONF fails)
- **GitHub:** https://github.com/Fedor-Goossens-pxl/lab-8-2-automation

## 🛠️ Device Vereisten

✓ Cisco IOS-XE (16.9.3+)
✓ NETCONF-YANG enabled: `netconf-yang`
✓ SSH enabled: `ip ssh version 2`
✓ Management interface bereikbaar (192.168.19.139)
✓ Geldige credentials (cisco/cisco123!)

## 💡 Tips

- Wacht 2-3 seconden na script completion
- Als command niets toont, probeer `show running-config`
- Bij errors, check: `show logging | include NETCONF`

---

*TASK_02_Enable_Disable_Interface - Verification Documentation*  
*PXL Hogeschool | Enterprise Networks 2 | Mei 2026*
