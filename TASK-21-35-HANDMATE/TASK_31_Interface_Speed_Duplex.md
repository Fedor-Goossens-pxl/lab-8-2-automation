# Task 31: Configure Interface Speed and Duplex

## 📝 Wat doet het script?

Configureer **interface speed en duplex settings**. Toont device limitations (virtual vs physical interfaces).

## ⚙️ Hoe werkt het?

- **Patroon:** LOCK → DISABLE auto-negotiation → SET speed/duplex → UNLOCK
- **Step 1:** Disable auto-negotiation (prerequisite)
- **Step 2:** Configure speed (e.g., 100, 1000)
- **Step 3:** Configure duplex (full, half)

## ✅ Script Output (bij succes)

```
✅ Auto-negotiation disabled
⚠️ Speed/Duplex: Device limitation (virtual interface)
✅ STEP 1 SUCCESS, STEP 2 EXPECTED FAILURE (virtual device)
```

## ⚠️ CSR1000v Limitation

```
✓ Step 1: Auto-negotiation can be disabled
❌ Step 2: Speed/Duplex fails (virtual device has no physical ports)

Physical routers: Steps 1+2 work together
Virtual simulator: Only Step 1 works
```

## 🔍 Hoe verifiëren?

```
show interfaces GigabitEthernet1
show interfaces Loopback0
```

## 💡 Key Insights

- **Auto-negotiation must be disabled first:** Prerequisite
- **Virtual devices:** Don't have physical port capabilities
- **Physical routers:** Can configure speed/duplex
- **Order matters:** Disable negotiation before setting fixed values

---

*TASK_31 - Enterprise Networks 2 | Juni 2026*
