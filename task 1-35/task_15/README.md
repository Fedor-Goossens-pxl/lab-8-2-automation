# Task 15: Create VLAN

## 📚 Categorie
Basis YANG-configuratie

## 🎯 Doel
Maak een VLAN aan via YANG.

## 📖 Uitleg
Deze oefening configureert **VLAN 10, name DATA** op VLAN 10 via NETCONF/YANG.

YANG-pad: `/native/vlan`

## 🛠️ Benodigdheden
- Python 3.8+
- ncclient library (`pip install ncclient`)
- Toegang tot CSR1000v op `192.168.19.139:830`
- Credentials: `admin / 123`
- Werkend NETCONF op poort 830

## 📥 Installatiehandleiding

```bash
# Clone repository
git clone https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
cd lab-8-2-automation/task_15

# Installeer dependencies
pip install -r requirements.txt

# Voer script uit
python task_15.py
```

## 🖥️ YANG Suite Setup

1. **Open YANG Suite**: `https://192.168.19.141:8443/yangtree/explore/`
2. **Selecteer YANG set**: `csr1000v-default-yangset`
3. **Load module**: `cisco-ios-xe-native`
4. **Navigeer naar**: `/native/vlan`
5. **Right-click** op de node → **"Get config template"**
6. **Kopieer** het gegenereerde XML payload

## 📋 Voorbeeld XML Payload

```xml
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <vlan>
      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan">
        <id>10</id>
        <name>DATA</name>
      </vlan-list>
    </vlan>
  </native>
</config>
```

## ✅ Verificatie/Testen

Na het uitvoeren van het script, verifieer met:

```bash
# SSH naar device
ssh admin@192.168.19.139

# Verificatie command
show vlan brief
```

### 🎯 Verwachte Output

```
VLAN Name                Status    Ports
10   DATA                 active
```

## 🐛 Troubleshooting

| Probleem | Oplossing |
|----------|-----------|
| Connection refused | Check of NETCONF aanstaat: `netconf-yang` in config |
| Authentication failed | Verifieer credentials: `admin/123` |
| Capability not supported | Check IOS-XE versie (min. 16.3) |
| Validation error | Check XML payload syntax |
| Commit failed | Gebruik `discard-changes` en probeer opnieuw |

## 📚 Referenties
- [LAB 8.2 Document](../docs/LAB_8_2.pdf)
- [Cisco YANG Models](https://github.com/YangModels/yang)
- [ncclient documentation](https://ncclient.readthedocs.io/)

---
**Auteur**: Fedor Goossens  
**Datum**: Mei 2026  
**Cursus**: Enterprise Networks 2 - PXL Hogeschool
