# Task 25: Compare Configurations

## 📝 Wat doet het script?

Maak **configuratie snapshots** en vergelijk ze. Retrieve config voor en na wijziging en vergelijk de XML.

## ⚙️ Hoe werkt het?

- **Patroon:** GET-CONFIG → EDIT → GET-CONFIG → Compare
- **Method:** get-config met filters
- **Datastore:** running
- **Comparison:** XML diff of manual comparison

## ✅ Script Output (bij succes)

```
Before config retrieved
Configuration modified
After config retrieved
Comparing: [differences shown]
✅ COMPARISON COMPLETE
```

## 🔍 Hoe verifiëren?

```
show running-config interface Loopback0
# Compare with previous snapshot
```

## 💡 Key Insights

- **Filters reduce data:** Only retrieve what you need
- **Before/after snapshots:** Good for change auditing
- **XPath filters:** Advanced filtering for complex queries

---

*TASK_25 - Enterprise Networks 2 | Juni 2026*
