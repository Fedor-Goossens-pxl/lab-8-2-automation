# Task 24: Rollback Configuration

## 📝 Wat doet het script?

Gebruik NETCONF **discard-changes** RPC om configuratie wijzigingen terug te draaien (rollback).

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → EDIT → VERIFY → DISCARD → VERIFY AGAIN
- **Method:** discard-changes RPC (NETCONF native)
- **Datastore:** running
- **Result:** Config returns to state before edit

## ✅ Script Output (bij succes)

```
✅ LOCK successful
✅ CONFIGURATION APPLIED
✅ Configuration before rollback visible
✅ DISCARD SUCCESSFUL
✅ Configuration rolled back!
```

## 💡 Key Insights

- **Rollback via discard-changes:** Not undo, but discards pending changes
- **Running datastore:** Changes are immediate, discard removes them
- **Candidate vs Running:** CSR1000v uses running (no candidate!)

---

*TASK_24 - Enterprise Networks 2 | Juni 2026*
