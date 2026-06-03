# Task 23: Configure Multiple Interfaces (Atomic)

## 📝 Wat doet het script?

Configureer **meerdere interfaces in één atomaire transactie**. Alle wijzigingen slagen of mislukken samen - geen halfway state!

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → EDIT (multiple interfaces) → UNLOCK → VERIFY
- **Atomicity:** All-or-nothing semantics
- **Datastore:** running
- **Interfaces:** Loopback0, Loopback1 (multiple config elements in één payload)

## ✅ Script Output (bij succes)

```
✅ LOCK successful
✅ CONFIGURATION APPLIED (multiple interfaces)
✅ UNLOCK successful
✅ VERIFICATION PASSED!
```

## 🔍 Hoe verifiëren?

```
show interfaces | include Loopback
show running-config interface Loopback
```

## 💡 Key Insights

- **Batch configuration:** Multiple interfaces in one edit-config RPC
- **Atomic guarantee:** Succeeds entirely or rolls back
- **Performance:** More efficient than multiple single edits
- **Error handling:** Device validates entire config before applying

---

*TASK_23 - Enterprise Networks 2 | Juni 2026*
