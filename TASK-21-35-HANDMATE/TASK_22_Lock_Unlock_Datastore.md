# Task 22: Lock and Unlock Datastore

## 📝 Wat doet het script?

Demonstreer het **lock/unlock patroon** voor atomaire NETCONF transacties. Lock voorkomt dat andere clients de configuratie wijzigen terwijl jij bezig bent.

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → EDIT → UNLOCK → VERIFY (4 stappen)
- **Method:** Atomaire transactie via dispatch()
- **Datastore:** running (writable, geen candidate support op CSR1000v!)
- **Verificatie:** Check <ok/> responses

## ✅ Script Output (bij succes)

```
======================================================================
STEP 1: LOCK RUNNING DATASTORE
======================================================================
✅ LOCK successful

======================================================================
STEP 2: CONFIGURE INTERFACE
======================================================================
✅ CONFIGURATION APPLIED

======================================================================
STEP 3: UNLOCK DATASTORE
======================================================================
✅ UNLOCK successful

======================================================================
STEP 4: VERIFY CONFIGURATION
======================================================================
✅ VERIFICATION PASSED!

TASK 22 COMPLETED!
======================================================================
```

## 🔍 Hoe verifiëren op CSR1000v Router?

### 1. SSH naar router en check:
```bash
ssh cisco@192.168.19.139
```

### 2. Zien welke NETCONF session locked:
```
show netconf-yang sessions
```

### 3. Config checken:
```
show running-config interface Loopback0
```

## 📂 Script Details

- **File:** `task_22.py` (NETCONF version - FINAL)
- **Lock support:** Yes (running datastore)
- **Candidate support:** NO (CSR1000v limitation!)
- **Atomic:** Yes

## 💡 Key Insights

- **CSR1000v does NOT support candidate datastore** → Unsupported capability
- **Lock works on running datastore** → Exclusive access
- **Lock timeout:** ~30 seconds (ncclient default)
- **Unlock is MANDATORY** → Otherwise next session waits!

## ⚠️ Critical Difference

```
✓ Task 21: Just EDIT (no lock)
✓ Task 22: LOCK → EDIT → UNLOCK (atomic)

CSR1000v Capabilities:
❌ candidate datastore (not supported)
✅ running datastore (writable)
✅ startup datastore (read-only)
```

---

*TASK_22_Lock_Unlock_Datastore - Enterprise Networks 2 | Juni 2026*
