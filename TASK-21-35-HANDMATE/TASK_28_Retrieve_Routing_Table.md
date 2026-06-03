# Task 28: Retrieve Routing Table

## 📝 Wat doet het script?

Retrieve de **routing table** van de router via GET-DATA RPC. Toont hoe je operational data opvraagt (niet configuratie).

## ⚙️ Hoe werkt het?

- **Patroon:** GET-DATA (not get-config)
- **Method:** get-data RPC met filter
- **Datastore:** operational (read-only)
- **Content:** Dynamic routing table entries

## ✅ Script Output (bij succes)

```
✅ Connected
✅ Retrieving routing table...
✅ Routing table retrieved!
Routes found: [X entries]
```

## 🔍 Hoe verifiëren?

```
show ip route
show ip route ospf
```

## 💡 Key Insights

- **GET-DATA vs GET-CONFIG:** get-data retrieves operational state
- **Filter syntax:** XPath or subtree for filtering
- **No LOCK needed:** Operational data is read-only
- **Large responses:** Filters help reduce data transfer

---

*TASK_28 - Enterprise Networks 2 | Juni 2026*
