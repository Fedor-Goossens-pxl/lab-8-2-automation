# Task 29: Configure Interface MTU

## 📝 Wat doet het script?

Configureer **Maximum Transmission Unit (MTU)** op interface. Toont hoe je ethernet-specific parameters wijzigt.

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → EDIT (MTU) → UNLOCK → VERIFY
- **Element:** mtu leaf under interface
- **Value:** 1500-9216 bytes (range depends on interface)
- **Example:** Set MTU to 9000 for jumbo frames

## ✅ Script Output (bij succes)

```
✅ LOCK successful
✅ MTU CONFIGURED: 1500
✅ UNLOCK successful
✅ VERIFICATION PASSED!
```

## 🔍 Hoe verifiëren?

```
show interfaces Loopback0 | include MTU
show running-config interface Loopback0
```

## 💡 Key Insights

- **MTU ranges:** Different per interface type
- **Virtual interfaces:** Loopback supports wider range
- **Physical ports:** May have hardware limits
- **Impact:** Changing MTU can disrupt traffic

---

*TASK_29 - Enterprise Networks 2 | Juni 2026*
