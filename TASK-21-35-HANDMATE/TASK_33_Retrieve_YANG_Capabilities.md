# Task 33: Retrieve YANG Capabilities

## 📝 Wat doet het script?

Retrieve en analyze alle **YANG capabilities** van CSR1000v. Toont welke models en features beschikbaar zijn.

## ⚙️ Hoe werkt het?

- **Patroon:** Get capabilities from server hello message
- **Method:** ncclient stores capabilities on connect
- **Result:** List of all supported YANG modules
- **Analysis:** Count by vendor (Cisco, IETF, OpenConfig)

## ✅ Script Output (bij succes)

```
✅ Connected!
✅ Capabilities retrieved: 438 total
  - Cisco modules: 129
  - IETF modules: 214
  - OpenConfig modules: 43
```

## 💡 Capabilities Analysis

```
Writable datastores:
✅ running-config
❌ candidate (NOT supported)
✅ startup-config

Specific features:
✅ NETCONF 1.0 + 1.1
✅ rollback-on-error
✅ xpath
✅ Tail-f actions
```

## 🔍 Hoe verifiëren?

```
show netconf-yang capabilities
```

## 💡 Key Insights

- **Capabilities = supported YANG models:** Different per device
- **No candidate:** CSR1000v limitation
- **Tail-f support:** Allows RPC actions
- **Deviations:** Some models have deviations (not 100% standard)

---

*TASK_33 - Enterprise Networks 2 | Juni 2026*
