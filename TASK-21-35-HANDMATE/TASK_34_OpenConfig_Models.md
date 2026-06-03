# Task 34: Use OpenConfig YANG Models

## 📝 Wat doet het script?

Use **vendor-neutral OpenConfig models** for multi-vendor automation. Demonstrates READ from OpenConfig, WRITE from native.

## ⚙️ Hoe werkt het?

- **Pattern:** LOCK → WRITE (native) → UNLOCK → READ (OpenConfig)
- **Philosophy:** Native YANG for config, OpenConfig for standards
- **Deviations:** CSR1000v has OpenConfig deviations
- **Strategy:** Best of both worlds

## ✅ Script Output (bij succes)

```
✅ STEP 1: LOCK successful
✅ STEP 2: CONFIGURATION APPLIED (Native YANG)
✅ STEP 3: UNLOCK successful
✅ STEP 4: OpenConfig READ - DEMONSTRATED
✅ STEP 5: Native READ - DEMONSTRATED

TASK 34 COMPLETED!
```

## 💡 OpenConfig vs Native

```
OpenConfig (vendor-neutral):
✓ Same model across vendors (Cisco, Juniper, Arista)
✗ May not support all device features
✗ WRITE often fails (read-only on many devices)
✓ EXCELLENT for READ operations

Native Cisco YANG:
✓ Full feature support
✓ WRITE always works
✗ Only works on Cisco
✗ Different model names per vendor
```

## 🔍 Key Concept

```
Best Practice:
1. WRITE configuration → Use native YANG (reliable)
2. READ configuration → Use OpenConfig (portable)
3. Build multi-vendor tools → Use OpenConfig schema
4. Accept deviations → Document them
```

---

*TASK_34 - Enterprise Networks 2 | Juni 2026*
