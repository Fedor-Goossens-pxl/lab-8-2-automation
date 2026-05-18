# Task 35: Full Service Deployment

## 📚 Categorie
Geavanceerde NETCONF/RESTCONF

## 🎯 Doel
Deploy een volledige netwerkdienst (interfaces, IP-adressering, routing en ACL) in één transactie.

## 📖 Uitleg
Deze oefening configureert **Atomic full deployment** op Multiple interfaces + routing + ACL via NETCONF/YANG.

YANG-pad: `Multiple containers in single edit-config`

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
cd lab-8-2-automation/task_35

# Installeer dependencies
pip install -r requirements.txt

# Voer script uit
python task_35.py
```

## 🖥️ YANG Suite Setup

1. **Open YANG Suite**: `https://192.168.19.141:8443/yangtree/explore/`
2. **Selecteer YANG set**: `csr1000v-default-yangset`
3. **Load module**: `cisco-ios-xe-native`
4. **Navigeer naar**: `Multiple containers in single edit-config`
5. **Right-click** op de node → **"Get config template"**
6. **Kopieer** het gegenereerde XML payload

## 📋 Voorbeeld XML Payload

```xml
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>CSR1000v-FULL-DEPLOY</hostname>
    <interface>
      <GigabitEthernet>
        <name>0/0/1</name>
        <description>WAN Interface</description>
        <ip>
          <address>
            <primary>
              <address>10.0.0.1</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
        <enabled>true</enabled>
      </GigabitEthernet>
    </interface>
    <router>
      <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
        <id>1</id>
        <network>
          <ip>10.0.0.0</ip>
          <wildcard>0.0.0.255</wildcard>
          <area>0</area>
        </network>
      </ospf>
    </router>
  </native>
</config>
```

## ✅ Verificatie/Testen

Na het uitvoeren van het script, verifieer met:

```bash
# SSH naar device
ssh admin@192.168.19.139

# Verificatie command
show running-config
```

### 🎯 Verwachte Output

```
Full configuration deployed: hostname, interfaces, routing
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
