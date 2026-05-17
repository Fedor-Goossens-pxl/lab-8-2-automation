#!/usr/bin/env python3
"""
Task 38: RESTCONF (Python) - IOS-XE Automatisering met YANG
Network as Code - Infrastructure as Code

Doel: Automatiseer een Cisco IOS-XE configuratie via RESTCONF
- Config wordt uit JSON-bestand gelezen (simuleert GitHub)
- PUT/PATCH requests naar RESTCONF API
- HTTP status codes controleren
- Logging van successen en fouten
"""

import requests
import json
import logging
import sys
from requests.auth import HTTPBasicAuth

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Device credentials
DEVICE_HOST = "192.168.19.139"
DEVICE_PORT = 443
DEVICE_USERNAME = "admin"
DEVICE_PASSWORD = "123"
CONFIG_FILE = "config-restconf.json"

# RESTCONF headers
RESTCONF_HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Base RESTCONF URL
BASE_URL = f"https://{DEVICE_HOST}:{DEVICE_PORT}/restconf"


def pretty_json(data):
    """Pretty-print JSON voor leesbaarheid"""
    try:
        return json.dumps(data, indent=2)
    except Exception as e:
        logger.error(f"Fout bij pretty-print JSON: {e}")
        return str(data)


def load_config_from_file(filename):
    """Lees YANG JSON-configuratie uit bestand (GitHub simulatie)"""
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        logger.info(f"Configuratie ingeladen uit: {filename}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuratiebestand '{filename}' niet gevonden!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        sys.exit(1)


def check_device_connectivity():
    """Test connectiviteit naar RESTCONF API"""
    try:
        logger.info(f"Controleer connectiviteit naar {DEVICE_HOST}:{DEVICE_PORT}")
        
        url = f"{BASE_URL}/yang-library-version"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(DEVICE_USERNAME, DEVICE_PASSWORD),
            headers=RESTCONF_HEADERS,
            verify=False,
            timeout=5
        )
        
        if response.status_code == 200:
            logger.info("Connectiviteit OK - RESTCONF API bereikbaar")
            return True
        else:
            logger.error(f"RESTCONF API geeft status {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij connectiviteit check: {e}")
        return False


def configure_hostname(hostname):
    """Configureer hostname via RESTCONF"""
    try:
        logger.info("\n--- CONFIGURE HOSTNAME ---")
        
        url = f"{BASE_URL}/data/Cisco-IOS-XE-native:native/hostname"
        
        payload = {
            "Cisco-IOS-XE-native:hostname": hostname
        }
        
        logger.info(f"PUT request naar: {url}")
        logger.info(f"Payload: {pretty_json(payload)}")
        
        response = requests.put(
            url,
            auth=HTTPBasicAuth(DEVICE_USERNAME, DEVICE_PASSWORD),
            headers=RESTCONF_HEADERS,
            json=payload,
            verify=False
        )
        
        # HTTP status codes controleren
        if response.status_code in [200, 201, 204]:
            logger.info(f"Hostname configuratie succesvol (HTTP {response.status_code})")
            return True
        else:
            logger.error(f"Hostname configuratie mislukt (HTTP {response.status_code})")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Exception bij hostname configuratie: {e}")
        return False


def configure_interface(interface_name, ip_address, subnet_mask):
    """Configureer interface via RESTCONF"""
    try:
        logger.info(f"\n--- CONFIGURE INTERFACE {interface_name} ---")
        
        # Cisco YANG model voor interface configuratie
        url = f"{BASE_URL}/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={interface_name}"
        
        payload = {
            "Cisco-IOS-XE-native:GigabitEthernet": [
                {
                    "name": interface_name,
                    "description": f"Configured by RESTCONF - Interface {interface_name}",
                    "enabled": True,
                    "ip": {
                        "address": {
                            "primary": {
                                "address": ip_address,
                                "mask": subnet_mask
                            }
                        }
                    }
                }
            ]
        }
        
        logger.info(f"PUT request naar: {url}")
        logger.info(f"Payload: {pretty_json(payload)}")
        
        response = requests.put(
            url,
            auth=HTTPBasicAuth(DEVICE_USERNAME, DEVICE_PASSWORD),
            headers=RESTCONF_HEADERS,
            json=payload,
            verify=False
        )
        
        if response.status_code in [200, 201, 204]:
            logger.info(f"Interface {interface_name} configuratie succesvol (HTTP {response.status_code})")
            return True
        else:
            logger.error(f"Interface {interface_name} configuratie mislukt (HTTP {response.status_code})")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Exception bij interface configuratie: {e}")
        return False


def configure_ospf(ospf_id, networks):
    """Configureer OSPF via RESTCONF"""
    try:
        logger.info("\n--- CONFIGURE OSPF ---")
        
        url = f"{BASE_URL}/data/Cisco-IOS-XE-native:native/router/ospf={ospf_id}"
        
        payload = {
            "Cisco-IOS-XE-native:ospf": [
                {
                    "id": ospf_id,
                    "network": networks
                }
            ]
        }
        
        logger.info(f"PUT request naar: {url}")
        logger.info(f"Payload: {pretty_json(payload)}")
        
        response = requests.put(
            url,
            auth=HTTPBasicAuth(DEVICE_USERNAME, DEVICE_PASSWORD),
            headers=RESTCONF_HEADERS,
            json=payload,
            verify=False
        )
        
        if response.status_code in [200, 201, 204]:
            logger.info(f"OSPF configuratie succesvol (HTTP {response.status_code})")
            return True
        else:
            logger.error(f"OSPF configuratie mislukt (HTTP {response.status_code})")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Exception bij OSPF configuratie: {e}")
        return False


def retrieve_running_config():
    """Haal running-config op via RESTCONF"""
    try:
        logger.info("\n--- RETRIEVE RUNNING CONFIG ---")
        
        url = f"{BASE_URL}/data/Cisco-IOS-XE-native:native"
        
        response = requests.get(
            url,
            auth=HTTPBasicAuth(DEVICE_USERNAME, DEVICE_PASSWORD),
            headers=RESTCONF_HEADERS,
            verify=False
        )
        
        if response.status_code == 200:
            config_data = response.json()
            logger.info("Running configuration opgehaald (HTTP 200)")
            print("\n" + "="*70)
            print(pretty_json(config_data))
            print("="*70)
            return True
        else:
            logger.error(f"Fout bij ophalen config (HTTP {response.status_code})")
            return False
            
    except Exception as e:
        logger.error(f"Exception bij ophalen config: {e}")
        return False


def main():
    """RESTCONF automatisering workflow"""
    
    print("\n" + "="*70)
    print("TASK 38: RESTCONF (Python) - Network as Code")
    print("IOS-XE Automatisering met YANG, RESTCONF en GitHub")
    print("="*70 + "\n")
    
    # Stap 1: Load config
    logger.info("STAP 1: Configuratie inladen (simuleert GitHub)")
    config = load_config_from_file(CONFIG_FILE)
    print(f"Config preview:\n{pretty_json(config)}\n")
    
    # Stap 2: Check connectiviteit
    logger.info("STAP 2: Controleer RESTCONF connectiviteit")
    if not check_device_connectivity():
        logger.error("Kan geen verbinding maken met RESTCONF API!")
        logger.info("TIPS voor troubleshooting:")
        logger.info(f"  1. Check IP-adres: {DEVICE_HOST}")
        logger.info(f"  2. Check HTTPS poort: {DEVICE_PORT}")
        logger.info(f"  3. Check credentials: {DEVICE_USERNAME}")
        logger.info(f"  4. Zorg dat RESTCONF enabled is op device:")
        logger.info("     (meestal automatisch enabled op moderne IOS-XE)")
        sys.exit(1)
    
    try:
        # Stap 3: Configure hostname
        logger.info("STAP 3: Configureer hostname")
        if not configure_hostname(config.get("hostname", "RESTCONF-Router-PE")):
            raise Exception("Hostname configuratie mislukt")
        
        # Stap 4: Configure interfaces
        logger.info("STAP 4: Configureer interfaces")
        for interface in config.get("interfaces", []):
            if not configure_interface(
                interface.get("name"),
                interface.get("ip"),
                interface.get("mask")
            ):
                raise Exception(f"Interface {interface.get('name')} configuratie mislukt")
        
        # Stap 5: Configure OSPF
        logger.info("STAP 5: Configureer OSPF")
        ospf_config = config.get("ospf", {})
        if ospf_config:
            if not configure_ospf(
                ospf_config.get("id", 1),
                ospf_config.get("networks", [])
            ):
                raise Exception("OSPF configuratie mislukt")
        
        # Stap 6: Retrieve config
        logger.info("STAP 6: Verificatie - Haal running config op")
        retrieve_running_config()
        
        logger.info("\n" + "="*70)
        logger.info("TASK 38 VOLTOOID - Network as Code succesvol!")
        logger.info("="*70 + "\n")
        
    except Exception as e:
        logger.error(f"\nFOUT in workflow: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
