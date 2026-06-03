# Task 26: Configure IPv6 Address

## 📝 Wat doet het script?

Configureer **IPv6 addressing** op interface via NETCONF YANG. Toont verschil tussen IPv4 en IPv6 YANG syntax.

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → EDIT (IPv6) → UNLOCK → VERIFY
- **YANG:** IPv6 element structure (prefix-list, not just primary)
- **Datastore:** running
- **Address example:** 2001:db8::1/64

## ✅ Script Output (bij succes)

```
✅ LOCK successful
✅ IPV6 CONFIGURED: 2001:db8::1/64
✅ UNLOCK successful
✅ VERIFICATION PASSED!
```

## 🔍 Hoe verifiëren?

```
show interfaces Loopback0
show ipv6 interface brief
```

## ⚠️ IPv6 vs IPv4 YANG Syntax

```xml
<!-- IPv4 -->
<ip>
  <address>
    <primary>
      <address>10.0.0.1</address>
      <mask>255.255.255.0</mask>
    </primary>
  </address>
</ip>

<!-- IPv6 -->
<ipv6>
  <address>
    <prefix-list>
      <prefix>2001:db8::1/64</prefix>
    </prefix-list>
  </address>
</ipv6>
```

---

*TASK_26 - Enterprise Networks 2 | Juni 2026*
