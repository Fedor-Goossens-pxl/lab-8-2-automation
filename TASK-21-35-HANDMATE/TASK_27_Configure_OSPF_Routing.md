# Task 27: Configure OSPF Routing

## 📝 Wat doet het script?

Configureer **OSPF routing process** via NETCONF YANG. Toont OSPF YANG namespace en mask (niet wildcard!) syntax.

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → EDIT (OSPF config) → UNLOCK → VERIFY
- **YANG Namespace:** `xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf"`
- **Key concept:** Use `<mask>` NOT `<wildcard>` for OSPF networks!
- **Example:** Process 1, Network 10.0.0.0/24, Area 0

## ✅ Script Output (bij succes)

```
✅ LOCK successful
✅ OSPF PROCESS 1 CONFIGURED
✅ Network 10.0.0.0/24 in area 0
✅ UNLOCK successful
✅ VERIFICATION PASSED!
```

## 🔍 Hoe verifiëren?

```
show ip ospf
show ip ospf neighbor
show ip route ospf
```

## ⚠️ CRITICAL: mask vs wildcard

```xml
<!-- CORRECT: Cisco native YANG uses <mask> -->
<network>
  <ip>10.0.0.0</ip>
  <mask>0.0.0.255</mask>      <!-- THIS! Not wildcard -->
  <area>0</area>
</network>

<!-- WRONG: This is OpenConfig syntax -->
<network>
  <ip>10.0.0.0</ip>
  <wildcard>0.0.0.255</wildcard>  <!-- DON'T USE! -->
  <area>0</area>
</network>
```

## 💡 Key Insights

- **OSPF element requires own namespace:** xmlns attribute!
- **Mask not wildcard:** Cisco native syntax difference
- **Area mandatory:** Must specify OSPF area
- **No candidate:** Writes directly to running

---

*TASK_27 - Enterprise Networks 2 | Juni 2026*
