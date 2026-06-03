# Task 35: Full Service Deployment

## 📝 Wat doet het script?

Deploy een **volledige netwerkdienst** in drie atomaire transacties:
1. Interface + IP configuration
2. OSPF routing
3. ACL deployment

## ⚙️ Hoe werkt het?

- **Pattern:** 3× (LOCK → CONFIG → UNLOCK)
- **Part 1:** Loopback0 + IPv4 address (10.99.99.99/32)
- **Part 2:** OSPF Process 35 with network 10.99.99.0/24
- **Part 3:** Standard ACL with permit rule

## ✅ Script Output (bij succes)

```
======================================================================
PART 1: INTERFACE + IP CONFIGURATION
======================================================================
  LOCK... ✅
  CONFIG... ✅
  UNLOCK... ✅

======================================================================
PART 2: OSPF ROUTING CONFIGURATION
======================================================================
  LOCK... ✅
  CONFIG... ✅
  UNLOCK... ✅

======================================================================
PART 3: ACL CONFIGURATION
======================================================================
  LOCK... ✅
  CONFIG... ✅
  UNLOCK... ✅

🎉 ALL PARTS SUCCESSFUL - FULL SERVICE DEPLOYED!
```

## 🔍 Hoe verifiëren?

### Part 1: Interface + IP
```
show interfaces Loopback0
show running-config interface Loopback0
```

### Part 2: OSPF
```
show ip ospf
show ip ospf neighbor
show ip route ospf
```

### Part 3: ACL
```
show access-lists TASK35_ACL
show access-lists | include TASK35
```

## ⚠️ Critical YANG Namespaces

```xml
<!-- Part 1: Native namespace on <ip> -->
<ip>
  <address>
    <primary>
      <address>10.99.99.99</address>
      <mask>255.255.255.255</mask>
    </primary>
  </address>
</ip>

<!-- Part 2: OSPF needs own namespace! -->
<ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
  <id>35</id>
  <network>
    <ip>10.99.99.0</ip>
    <mask>0.0.0.255</mask>    <!-- NOT wildcard! -->
    <area>0</area>
  </network>
</ospf>

<!-- Part 3: Standard ACL needs own namespace! -->
<standard xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
  <name>TASK35_ACL</name>
  <access-list-seq-rule>
    <sequence>10</sequence>
    <permit>
      <std-ace>
        <host>10.99.99.99</host>
      </std-ace>
    </permit>
  </access-list-seq-rule>
</standard>
```

## 💡 Key Learnings

1. **Atomic Transactions:** Multiple parts, each atomic
2. **Namespaces are critical:** OSPF, ACL need own xmlns
3. **Production-ready:** All 3 services in one flow
4. **Error recovery:** Lock prevents partial failures
5. **Scalability:** Pattern extends to unlimited services

## 🎯 Enterprise Readiness

```
✅ Production patterns (atomic transactions)
✅ Multi-service deployment
✅ Error handling (all-or-nothing)
✅ Verification (post-deployment checks)
✅ Idempotency (safe to re-run)
```

---

*TASK_35_Full_Service_Deployment - Enterprise Networks 2 | Juni 2026*
