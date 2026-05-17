#!/usr/bin/env python3
"""
Task 36: NETCONF (Python) - IOS-XE Automatisering met YANG
Network as Code - Infrastructure as Code

Doel: Automatiseer een Cisco IOS-XE configuratie via NETCONF
- Config wordt uit XML-bestand gelezen (simuleert GitHub)
- Edit-config naar candidate datastore
- Commit naar running
- Foutafhandeling en status feedback
"""

import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from ncclient import manager
from ncclient.operations import RaiseMode
import logging

# ============================================================================
# LOGGING SETUP - Statusinformatie zichtbaar maken
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DEVICE CREDENTIALS - Pas aan naar jouw IOS-XE device
# ============================================================================
DEVICE_HOST = "192.168.19.139"  # CSR1000v IP
DEVICE_PORT = 830
DEVICE_USERNAME = "admin"
DEVICE_PASSWORD = "123"
DEVICE_HOSTKEY_VERIFY = False

# YANG XML CONFIG FILE
CONFIG_FILE = "config-iosxe.xml"

# ============================================================================
# FUNCTIE 1: Pretty-print XML Response
# ============================================================================
def prettify_xml(xml_string):
    """
    Parse en pretty-print XML voor leesbaarheid
    Requirement: XML/JSON-pretty-print voor NETCONF responses
    """
    try:
        dom = minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")
    except Exception as e:
        logger.error(f"Fout bij pretty-print XML: {e}")
        return xml_string

# ============================================================================
# FUNCTIE 2: Inladen configuratie uit XML-bestand (GitHub simulatie)
# ============================================================================
def load_config_from_file(filename):
    """
    Lees YANG XML-configuratie uit bestand
    In productie: wordt dit uit GitHub opgehaald
    """
    try:
        with open(filename, 'r') as f:
            config_xml = f.read()
        logger.info(f"✓ Configuratie ingeladen uit: {filename}")
        return config_xml
    except FileNotFoundError:
        logger.error(f"✗ FOUT: Configuratiebestand '{filename}' niet gevonden!")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ FOUT bij inladen config: {e}")
        sys.exit(1)

# ============================================================================
# FUNCTIE 3: NETCONF Connectie en Authenticatie
# ============================================================================
def connect_netconf_device(host, port, username, password):
    """
    Maak NETCONF SSH-connectie met IOS-XE device
    """
    try:
        logger.info(f"Verbinden met {host}:{port}...")
        
        m = manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=DEVICE_HOSTKEY_VERIFY,
            allow_agent=False,
            look_for_keys=False,
            ssh_config=None
        )
        
        logger.info("✓ NETCONF-verbinding gelukt!")
        return m
        
    except Exception as e:
        logger.error(f"✗ NETCONF-verbinding mislukt: {e}")
        sys.exit(1)

# ============================================================================
# FUNCTIE 4: Edit-Config naar Candidate Datastore
# ============================================================================
def edit_candidate_datastore(manager_obj, config_xml):
    """
    Requirement: NETCONF statusinformatie
    - <ok/> response betekent succes
    - Foutmeldingen met error-tag/error-type
    """
    try:
        logger.info("\n--- EDIT-CONFIG naar CANDIDATE DATASTORE ---")
        
        # Verstuur edit-config RPC
        rpc_reply = manager_obj.edit_config(
            target='candidate',
            config=config_xml,
            default_operation='merge',  # merge ipv replace
            error_option='stop-on-error'
        )
        
        # Check NETCONF RPC Reply
        if rpc_reply.ok:
            logger.info("✓ Edit-config succes! RPC reply: <ok/>")
            return True
        else:
            logger.error(f"✗ Edit-config mislukt!")
            logger.error(f"RPC Reply:\n{prettify_xml(rpc_reply.xml)}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Exception bij edit-config: {e}")
        return False

# ============================================================================
# FUNCTIE 5: Commit Configuratie naar Running Datastore
# ============================================================================
def commit_config(manager_obj):
    """
    Commit candidate config naar running datastore
    Statusinformatie: <ok/> response controleren
    """
    try:
        logger.info("\n--- COMMIT naar RUNNING DATASTORE ---")
        
        commit_reply = manager_obj.commit()
        
        if commit_reply.ok:
            logger.info("✓ Commit succes! RPC reply: <ok/>")
            logger.info("Configuratie is nu actief op het device!")
            return True
        else:
            logger.error(f"✗ Commit mislukt!")
            logger.error(f"RPC Reply:\n{prettify_xml(commit_reply.xml)}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Exception bij commit: {e}")
        logger.info("Probeer discard-changes...")
        try:
            manager_obj.discard_changes()
            logger.info("Candidate config verworpen")
        except:
            pass
        return False

# ============================================================================
# FUNCTIE 6: Retrieve Running Configuration
# ============================================================================
def get_running_config(manager_obj):
    """
    Haal running-config op en toon resultaat
    """
    try:
        logger.info("\n--- RETRIEVE RUNNING CONFIG ---")
        
        running = manager_obj.get_config(source='running')
        config_data = running.data_xml
        
        logger.info("Running configuration opgehaald:")
        print("\n" + "="*70)
        print(prettify_xml(config_data))
        print("="*70)
        
        return config_data
        
    except Exception as e:
        logger.error(f"✗ Fout bij ophalen running config: {e}")

# ============================================================================
# FUNCTIE 7: Validatie - Check Device Capabilities
# ============================================================================
def check_device_capabilities(manager_obj):
    """
    Controleer welke NETCONF capabilities het device ondersteunt
    """
    logger.info("\n--- DEVICE NETCONF CAPABILITIES ---")
    capabilities = manager_obj.server_capabilities
    
    logger.info(f"Device supports {len(capabilities)} NETCONF capabilities:")
    for cap in capabilities:
        if 'http' in cap:
            logger.info(f"  • {cap[:80]}...")
    
    # Check kritische capabilities
    supports_candidate = any('candidate' in str(cap) for cap in capabilities)
    supports_commit = any('confirmed-commit' in str(cap) or 'commit' in str(cap) 
                         for cap in capabilities)
    
    if supports_candidate and supports_commit:
        logger.info("✓ Device ondersteunt candidate datastore en commit!")
        return True
    else:
        logger.warning("⚠ Device ondersteunt mogelijk niet alle vereiste capabilities!")
        return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """
    Volledige NETCONF automatisering workflow
    Task 36: NETCONF (Python) met GitHub als configuratiebron
    """
    
    print("\n" + "="*70)
    print("TASK 36: NETCONF (Python) - Network as Code")
    print("IOS-XE Automatisering met YANG, NETCONF en GitHub")
    print("="*70 + "\n")
    
    # Stap 1: Inladen configuratie
    logger.info("STAP 1: Configuratie inladen (simuleert GitHub)")
    config_xml = load_config_from_file(CONFIG_FILE)
    print(f"Config preview:\n{prettify_xml(config_xml)}\n")
    
    # Stap 2: NETCONF verbinding
    logger.info("STAP 2: Verbinding maken met IOS-XE device")
    try:
        m = connect_netconf_device(
            DEVICE_HOST,
            DEVICE_PORT,
            DEVICE_USERNAME,
            DEVICE_PASSWORD
        )
    except:
        logger.error("Kan geen verbinding maken met device!")
        logger.info("TIPS voor troubleshooting:")
        logger.info(f"  1. Controleer IP-adres: {DEVICE_HOST}")
        logger.info(f"  2. Controleer NETCONF poort: {DEVICE_PORT}")
        logger.info(f"  3. Controleer credentials: {DEVICE_USERNAME}")
        logger.info(f"  4. Zorg dat NETCONF enabled is op device:")
        logger.info("     netconf ssh")
        sys.exit(1)
    
    try:
        # Stap 3: Check capabilities
        logger.info("STAP 3: Controleer device capabilities")
        check_device_capabilities(m)
        
        # Stap 4: Edit-config naar candidate
        logger.info("STAP 4: Verstuur config naar candidate datastore")
        if not edit_candidate_datastore(m, config_xml):
            raise Exception("Edit-config naar candidate mislukt!")
        
        # Stap 5: Commit naar running
        logger.info("STAP 5: Commit naar running datastore")
        if not commit_config(m):
            raise Exception("Commit mislukt!")
        
        # Stap 6: Haal running config op ter verificatie
        logger.info("STAP 6: Verificatie - Haal running config op")
        get_running_config(m)
        
        logger.info("\n" + "="*70)
        logger.info("✓ TASK 36 VOLTOOID - Network as Code succesvol!")
        logger.info("="*70 + "\n")
        
    except Exception as e:
        logger.error(f"\n✗ FOUT in workflow: {e}")
        sys.exit(1)
    finally:
        # Sluit connectie
        try:
            m.close_session()
            logger.info("NETCONF-sessie gesloten")
        except:
            pass

if __name__ == "__main__":
    main()
