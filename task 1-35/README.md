# 🚀 LAB 8.2 - IOS-XE Automatisering met YANG, NETCONF en RESTCONF

## 📋 Overzicht

Dit repository bevat alle 35 oefeningen voor LAB 8.2 van het vak **Enterprise Networks 2** aan PXL Hogeschool.

Elke oefening configureert een aspect van een Cisco IOS-XE toestel via NETCONF/YANG protocollen.

## 🗂️ Repository Structuur

```
lab-8-2-automation/
├── task_1/          # Configure Interface Description
├── task_2/          # Enable / Disable Interface
├── task_3/          # Configure IPv4 Address
├── task_4/          # Remove IPv4 Address
├── task_5/          # Create Loopback Interface
├── ...
├── task_35/         # Full Service Deployment
└── README.md        # Dit bestand
```

## 📚 Categorieën

### 🟢 Deel 1: Basis YANG-configuratie (Tasks 1-20)
Eenvoudige configuratie operaties via YANG modellen.

### 🟡 Deel 2: Geavanceerde NETCONF/RESTCONF (Tasks 21-35)
Complex operaties met candidate datastore, transactions, en geavanceerde features.

## 🛠️ Algemene Vereisten

- **Python**: 3.8 of hoger
- **ncclient**: NETCONF client library
- **CSR1000v**: IOS-XE 16.3+ met NETCONF aan
- **YANG Suite**: Voor model exploration

## 📥 Quick Start

```bash
# Clone repository
git clone https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
cd lab-8-2-automation

# Naar specifieke task
cd task_1

# Installeer dependencies
pip install -r requirements.txt

# Voer task uit
python task_1.py
```

## 🖥️ Device Setup

### CSR1000v Connection Info
- **IP**: `192.168.19.139`
- **NETCONF Port**: `830`
- **RESTCONF Port**: `443`
- **Username**: `admin`
- **Password**: `123`

### YANG Suite
- **URL**: `https://192.168.19.141:8443/yangtree/explore/`
- **YANG Set**: `csr1000v-default-yangset`

## 📖 Hoe te gebruiken

1. Navigeer naar de gewenste task folder
2. Lees `README.md` voor doel en uitleg
3. Volg `stappenplan.md` voor stap-voor-stap instructies
4. Voer het Python script uit
5. Verifieer met SSH naar device

## 🎯 Tasks Overzicht

| # | Task | Categorie |
|---|------|-----------|
| 1 | [Configure Interface Description](task_1/README.md) | Basis YANG-configuratie |
| 2 | [Enable / Disable Interface](task_2/README.md) | Basis YANG-configuratie |
| 3 | [Configure IPv4 Address](task_3/README.md) | Basis YANG-configuratie |
| 4 | [Remove IPv4 Address](task_4/README.md) | Basis YANG-configuratie |
| 5 | [Create Loopback Interface](task_5/README.md) | Basis YANG-configuratie |
| 6 | [Configure Loopback IP](task_6/README.md) | Basis YANG-configuratie |
| 7 | [Change Hostname](task_7/README.md) | Basis YANG-configuratie |
| 8 | [Configure DNS Server](task_8/README.md) | Basis YANG-configuratie |
| 9 | [Configure NTP Server](task_9/README.md) | Basis YANG-configuratie |
| 10 | [Configure Static Route](task_10/README.md) | Basis YANG-configuratie |
| 11 | [Remove Static Route](task_11/README.md) | Basis YANG-configuratie |
| 12 | [Configure Banner MOTD](task_12/README.md) | Basis YANG-configuratie |
| 13 | [Create Local User](task_13/README.md) | Basis YANG-configuratie |
| 14 | [Change User Password](task_14/README.md) | Basis YANG-configuratie |
| 15 | [Create VLAN](task_15/README.md) | Basis YANG-configuratie |
| 16 | [Assign Interface to VLAN](task_16/README.md) | Basis YANG-configuratie |
| 17 | [Enable SNMP Community](task_17/README.md) | Basis YANG-configuratie |
| 18 | [Retrieve Interface Statistics](task_18/README.md) | Basis YANG-configuratie |
| 19 | [Retrieve Running Configuration](task_19/README.md) | Basis YANG-configuratie |
| 20 | [Validate Configuration Change](task_20/README.md) | Basis YANG-configuratie |
| 21 | [Use Candidate Datastore](task_21/README.md) | Geavanceerde NETCONF/RESTCONF |
| 22 | [Lock and Unlock Datastore](task_22/README.md) | Geavanceerde NETCONF/RESTCONF |
| 23 | [Configure Multiple Interfaces in One Transaction](task_23/README.md) | Geavanceerde NETCONF/RESTCONF |
| 24 | [Rollback Configuration](task_24/README.md) | Geavanceerde NETCONF/RESTCONF |
| 25 | [Compare Running vs Candidate Configuration](task_25/README.md) | Geavanceerde NETCONF/RESTCONF |
| 26 | [Configure IPv6 Address](task_26/README.md) | Geavanceerde NETCONF/RESTCONF |
| 27 | [Configure OSPF Routing](task_27/README.md) | Geavanceerde NETCONF/RESTCONF |
| 28 | [Retrieve Routing Table](task_28/README.md) | Geavanceerde NETCONF/RESTCONF |
| 29 | [Configure Interface MTU](task_29/README.md) | Geavanceerde NETCONF/RESTCONF |
| 30 | [Configure Access Control List](task_30/README.md) | Geavanceerde NETCONF/RESTCONF |
| 31 | [Configure Interface Speed and Duplex](task_31/README.md) | Geavanceerde NETCONF/RESTCONF |
| 32 | [Execute YANG Action](task_32/README.md) | Geavanceerde NETCONF/RESTCONF |
| 33 | [Retrieve YANG Capabilities](task_33/README.md) | Geavanceerde NETCONF/RESTCONF |
| 34 | [Use OpenConfig Models](task_34/README.md) | Geavanceerde NETCONF/RESTCONF |
| 35 | [Full Service Deployment](task_35/README.md) | Geavanceerde NETCONF/RESTCONF |


## 🐛 Algemene Troubleshooting

| Probleem | Oplossing |
|----------|-----------|
| NETCONF niet bereikbaar | Check `netconf-yang` config |
| Auth failed | Verifieer credentials |
| Timeout | Verhoog `TIMEOUT` waarde |
| XML validation | Test payload in YANG Suite |

## 📚 Referenties

- [LAB 8.2 Document](docs/LAB_8_2.pdf)
- [Cisco DevNet](https://developer.cisco.com/)
- [YANG Suite Docs](https://developer.cisco.com/docs/yangsuite/)
- [ncclient Documentation](https://ncclient.readthedocs.io/)

## 👤 Auteur

**Fedor Goossens**  
Studienr: 2SNEb  
Email: fedor.goossens@student.pxl.be  
Opleiding: Graduaat Systeem en Netwerkbeheer  
Hogeschool: PXL  
Datum: Mei 2026

---

⭐ **Veel succes met LAB 8.2!**
