# Task 30: Configure ACL (Extended)

## 📝 Wat doet het script?

Configureer **Extended Access Control List** via NETCONF YANG. Toont complex YANG structures met ACL namespace.

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → EDIT (ACL) → UNLOCK → VERIFY
- **YANG Namespace:** `xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl"`
- **ACL Type:** Extended (action, protocol, source, destination)
- **Example:** Deny IP traffic from 10.0.0.0/24

## ✅ Script Output (bij succes)

```
✅ LOCK successful
✅ ACL BLOCK_TRAFFIC CONFIGURED
✅ Extended ACL with deny rules
✅ UNLOCK successful
```

## 🔍 Hoe verifiëren?

```
show access-lists
show access-lists BLOCK_TRAFFIC
```

## ⚠️ ACL Namespace Required

```xml
<!-- CORRECT: ACL has own namespace -->
<extended xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
  <name>BLOCK_TRAFFIC</name>
  <access-list-seq-rule>
    <sequence>10</sequence>
    <ace-rule>
      <action>deny</action>
      <protocol>ip</protocol>
      ...
    </ace-rule>
  </access-list-seq-rule>
</extended>
```

---

*TASK_30 - Enterprise Networks 2 | Juni 2026*
