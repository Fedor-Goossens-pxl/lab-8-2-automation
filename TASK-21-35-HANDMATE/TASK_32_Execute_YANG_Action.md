# Task 32: Execute YANG RPC Action (Clear Interface Counters)

## 📝 Wat doet het script?

Execute een **YANG RPC action** om interface counters te resetten. Toont verschil tussen configuration (edit-config) en actions (RPC).

## ⚙️ Hoe werkt het?

- **Patroon:** Dispatch RPC (clear action)
- **Type:** YANG RPC (not edit-config)
- **Action:** Clear interface counters
- **Method:** dispatch() with custom RPC payload

## ✅ Script Output (bij succes)

```
✅ Connected
✅ Clear action dispatched
✅ RPC request successful
Counters cleared for GigabitEthernet1
```

## 🔍 Hoe verifiëren?

```
show interfaces GigabitEthernet1 counters
# After task: counters reset to 0
```

## 💡 Key Insights

- **Actions != Configuration:** RPC performs operation, not stores state
- **Tail-f Actions:** CSR1000v supports Tail-f actions
- **No LOCK needed:** Actions don't modify config
- **Immediate execution:** Result returns in RPC reply

---

*TASK_32 - Enterprise Networks 2 | Juni 2026*
