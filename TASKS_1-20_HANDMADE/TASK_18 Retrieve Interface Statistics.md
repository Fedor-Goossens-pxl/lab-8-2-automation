# Task 18: Retrieve Interface Statistics

## 📝 Wat doet het script?

Haalt **operationele interface-statistieken** op van **GigabitEthernet1** via NETCONF/YANG GET RPC.
Gebruikt het **ietf-interfaces** YANG model (RFC 7223) voor het ophalen van read-only operationele data.

## ⚙️ Hoe werkt het?

- **Patroon:** NETCONF GET (niet edit-config!)
- **Method:** dispatch() raw XML RPC (YANGsuite pattern)
- **Datastore:** interfaces-state (operationeel/read-only)
- **YANG Model:** ietf-interfaces (RFC 7223)
- **Path:** `/interfaces-state/interface[name='GigabitEthernet1']/statistics`

## ✅ Script Output (bij succes)

```
✓ NETCONF Connection: Established
✓ RPC dispatched successfully
✓ Interface GigabitEthernet1 found!
✓ Found X statistics counters:
  - in-octets
  - in-unicast-pkts
  - in-errors
  - out-octets
  - out-unicast-pkts
  - out-errors
  (en meer...)
```

## 📊 Statistieken die opgehaald worden

**Inbound:**
- `in-octets` - Total bytes received
- `in-unicast-pkts` - Unicast packets received
- `in-broadcast-pkts` - Broadcast packets received
- `in-multicast-pkts` - Multicast packets received
- `in-discards` - Inbound discarded packets
- `in-errors` - Inbound error packets
- `in-unknown-protos` - Unknown protocol packets

**Outbound:**
- `out-octets` - Total bytes transmitted
- `out-unicast-pkts` - Unicast packets sent
- `out-broadcast-pkts` - Broadcast packets sent
- `out-multicast-pkts` - Multicast packets sent
- `out-discards` - Outbound discarded packets
- `out-errors` - Outbound error packets

**Meta:**
- `discontinuity-time` - Last counter reset/discontinuity

## 🔍 Hoe verifiëren op CSR1000v?

### 1. SSH naar de router:
```bash
ssh cisco@192.168.19.139
```

### 2. Verificatie command (CLI):
```
show interfaces GigabitEthernet1
```

### 3. Wat je ziet:
```
GigabitEthernet1 is up, line protocol is up
  Hardware is CSR vNIC, address is 0a09.1339.0000
  Description: VBox
  Internet address is 192.168.19.139/24
  ...
  (statistics worden getoond)
```

### 4. NETCONF verificatie:
```bash
# Script voert automatisch GET RPC uit
python task_18.py
```

## 📂 Script Details

- **File:** `task_18.py` (NETCONF GET version)
- **Pattern:** YANGsuite dispatch() raw XML RPC
- **GitHub:** https://github.com/Fedor-Goossens-pxl/lab-8-2-automation

## 🛠️ Device Vereisten

✓ Cisco IOS-XE (16.9.3+)
✓ NETCONF-YANG enabled: `netconf-yang`
✓ SSH enabled: `ip ssh version 2`
✓ Management interface bereikbaar (192.168.19.139)
✓ Geldige credentials (cisco/cisco123!)
✓ ietf-interfaces YANG model ondersteund (standaard)

## 💡 Tips

- Dit is een **GET** operatie, geen configuratie!
- Data is **read-only** (config false)
- Statistieken worden real-time opgehaald
- `discontinuity-time` geeft aan wanneer counters reset werden
- Geen errors = 0 in in-errors en out-errors (goed teken!)

## 📝 YANG Reference

**Model:** ietf-interfaces (RFC 7223)
**Namespace:** `urn:ietf:params:xml:ns:yang:ietf-interfaces`
**Container:** `interfaces-state/interface/statistics`

```yang
container interfaces-state {
  config false;
  list interface {
    key "name";
    leaf name { ... }
    container statistics {
      leaf in-octets { type yang:counter64; }
      leaf out-octets { type yang:counter64; }
      leaf in-errors { type yang:counter32; }
      leaf out-errors { type yang:counter32; }
      ... (meer statistieken)
    }
  }
}
```

---

*TASK_18_Retrieve_Interface_Statistics - Operational Data Documentation*  
*PXL Hogeschool | Enterprise Networks 2 | Juni 2026*  
*✅ WERKT 100% - Tested & Verified*