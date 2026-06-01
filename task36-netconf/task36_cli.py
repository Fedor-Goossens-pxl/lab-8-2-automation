#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 36: NETCONF (Python) CLI Version - IMPROVED
Network as Code via SSH/CLI Automation (Netmiko)

Doel: Automatiseer IOS-XE config via SSH when NETCONF fails
Verbeteringen:
  - Per-commando handling (niet send_config_set)
  - Betere prompt detection
  - Langzamere config versturen
  - Uitgebreide error handling
  - Verificatie na config
"""

import sys
import time
import logging
import os
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Fix voor Windows Unicode issues
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# ============================================================================
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task36_cli.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# DEVICE CREDENTIALS
# ============================================================================
DEVICE = {
    'device_type': 'cisco_ios',
    'host': '192.168.19.139',
    'username': 'admin',
    'password': '123',
    'port': 22,
    'timeout': 30,
    'global_delay_factor': 2.0,  # Langzamer versturen
    'session_log': 'netmiko_session.log',  # Debug log
}

# ============================================================================
# CONFIGURATIE COMMANDO'S
# ============================================================================
CONFIG_COMMANDS = [
    ('config t', 'config mode'),
    ('hostname NETCONF-Router-PE', 'hostname'),
    ('interface GigabitEthernet1', 'interface GigabitEthernet1'),
    ('ip address 10.255.255.1 255.255.255.0', 'IP GigabitEthernet1'),
    ('description Configured by CLI Automation', 'description GigabitEthernet1'),
    ('no shutdown', 'enable GigabitEthernet1'),
    ('exit', 'exit GigabitEthernet1'),
    
    ('interface GigabitEthernet2', 'interface GigabitEthernet2'),
    ('ip address 192.168.1.1 255.255.255.0', 'IP GigabitEthernet2'),
    ('description Secondary Interface CLI', 'description GigabitEthernet2'),
    ('no shutdown', 'enable GigabitEthernet2'),
    ('exit', 'exit GigabitEthernet2'),
    
    ('interface Loopback0', 'interface Loopback0'),
    ('ip address 172.16.1.1 255.255.255.255', 'IP Loopback0'),
    ('description Loopback Interface', 'description Loopback0'),
    ('exit', 'exit Loopback0'),
    
    ('router ospf 1', 'router ospf'),
    ('router-id 172.16.1.1', 'OSPF router-id'),
    ('network 10.255.255.0 0.0.0.255 area 0', 'OSPF network 1'),
    ('network 192.168.1.0 0.0.0.255 area 0', 'OSPF network 2'),
    ('network 172.16.1.0 0.0.0.255 area 0', 'OSPF network 3'),
    ('exit', 'exit ospf'),
    
    ('end', 'exit config mode'),
    ('write memory', 'save configuration'),
]

# ============================================================================
# FUNCTIE 1: Verbinding maken
# ============================================================================
def connect_device():
    """Maak SSH-verbinding met IOS-XE device"""
    try:
        logger.info(f"Verbinding met {DEVICE['host']}:{DEVICE['port']}...")
        
        net_connect = ConnectHandler(**DEVICE)
        
        logger.info("[OK] SSH-verbinding gelukt!")
        
        # Toon device info
        prompt = net_connect.find_prompt()
        logger.info(f"Device prompt: {prompt}")
        
        return net_connect
        
    except NetmikoAuthenticationException as e:
        logger.error(f"[FAIL] Authenticatie mislukt: {e}")
        logger.error("Check username/password credentials")
        sys.exit(1)
    except NetmikoTimeoutException as e:
        logger.error(f"[FAIL] Timeout bij verbinding: {e}")
        logger.error("Device reageert niet - check IP-adres en connectivity")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[FAIL] Verbinding mislukt: {e}")
        sys.exit(1)

# ============================================================================
# FUNCTIE 2: Configuratie versturen (per commando)
# ============================================================================
def apply_configuration(net_connect):
    """Verstuur config commando's één voor één met error handling"""
    try:
        logger.info("\n" + "="*70)
        logger.info("CONFIGURATIE VERSTUREN")
        logger.info("="*70)
        
        success_count = 0
        fail_count = 0
        failed_commands = []
        
        for command, description in CONFIG_COMMANDS:
            try:
                logger.info(f"  > {description}: '{command}'")
                
                # Verstuur commando en wacht op response
                output = net_connect.send_command(
                    command,
                    expect_string=r'[>#]',  # Prompt match
                    read_timeout=10
                )
                
                # Check voor error messages
                if 'error' in output.lower() or 'invalid' in output.lower():
                    logger.warning(f"    [WARN] Mogelijke fout in response: {output[:100]}")
                    fail_count += 1
                    failed_commands.append((command, output))
                else:
                    logger.info(f"    [OK]")
                    success_count += 1
                
                # Kleine vertraging tussen commando's
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"    [FAIL] FOUT: {str(e)[:100]}")
                fail_count += 1
                failed_commands.append((command, str(e)))
                # Probeer door te gaan met volgende commando
                continue
        
        logger.info("="*70)
        logger.info(f"Configuratie verstuur: {success_count} succesvol, {fail_count} fouten")
        logger.info("="*70)
        
        if failed_commands:
            logger.warning("\nMislukte commando's:")
            for cmd, error in failed_commands:
                logger.warning(f"  * {cmd}: {error[:100]}")
            return False
        
        logger.info("[OK] Alle commando's succesvol!")
        return True
        
    except Exception as e:
        logger.error(f"[FAIL] Kritieke fout bij configuratie: {e}")
        return False

# ============================================================================
# FUNCTIE 3: Configuratie verifiëren
# ============================================================================
def verify_configuration(net_connect):
    """Controleer of config daadwerkelijk is geapplied"""
    try:
        logger.info("\n" + "="*70)
        logger.info("VERIFICATIE - RUNNING CONFIGURATION")
        logger.info("="*70 + "\n")
        
        verification_commands = [
            ('show run | grep hostname', 'Hostname'),
            ('show ip interface brief', 'Interfaces'),
            ('show ip ospf', 'OSPF status'),
            ('show running-config | section ospf', 'OSPF networks'),
        ]
        
        all_ok = True
        
        for cmd, desc in verification_commands:
            try:
                logger.info(f"> {desc}:")
                output = net_connect.send_command(cmd, read_timeout=10)
                
                if output.strip():
                    # Toon output
                    for line in output.split('\n'):
                        if line.strip():
                            logger.info(f"  {line}")
                else:
                    logger.warning(f"  [WARN] Geen output voor {desc}")
                    all_ok = False
                
                logger.info("")
                
            except Exception as e:
                logger.error(f"  [FAIL] Fout bij {desc}: {e}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        logger.error(f"[FAIL] Verificatie mislukt: {e}")
        return False

# ============================================================================
# FUNCTIE 4: Pre-flight checks
# ============================================================================
def preflight_checks(net_connect):
    """Controleer device status voor configuratie"""
    try:
        logger.info("\n" + "="*70)
        logger.info("PRE-FLIGHT CHECKS")
        logger.info("="*70)
        
        # Check device OS
        logger.info("> Checking device OS...")
        output = net_connect.send_command('show version | grep "Software Version"', read_timeout=10)
        logger.info(f"  {output.strip()}")
        
        # Check running config
        logger.info("> Checking current config size...")
        output = net_connect.send_command('show running-config | count', read_timeout=10)
        logger.info(f"  {output.strip()}")
        
        logger.info("[OK] Pre-flight checks OK\n")
        return True
        
    except Exception as e:
        logger.warning(f"[WARN] Pre-flight check mislukt (non-critical): {e}\n")
        return True  # Non-fatal

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """Volledige CLI automatisering workflow"""
    
    print("\n" + "="*70)
    print("TASK 36: NETCONF (Python) CLI Version - IMPROVED")
    print("Network as Code via SSH/CLI Automation")
    print("="*70 + "\n")
    
    net_connect = None
    
    try:
        # Stap 1: Verbinding
        logger.info("STAP 1: SSH-verbinding maken")
        net_connect = connect_device()
        
        # Stap 2: Pre-flight checks
        logger.info("STAP 2: Pre-flight checks")
        preflight_checks(net_connect)
        
        # Stap 3: Configuratie versturen
        logger.info("STAP 3: Configuratie versturen (per commando)")
        config_ok = apply_configuration(net_connect)
        
        if not config_ok:
            logger.error("[FAIL] Configuratie versturen mislukt!")
            return False
        
        # Kleine wachttijd voor device om config te verwerken
        logger.info("\nWachten op device verwerking...")
        time.sleep(2)
        
        # Stap 4: Verificatie
        logger.info("STAP 4: Verificatie")
        verify_ok = verify_configuration(net_connect)
        
        # Resultaat
        logger.info("\n" + "="*70)
        if config_ok and verify_ok:
            logger.info("[OK] TASK 36 CLI VOLTOOID - Network as Code succesvol!")
            logger.info("="*70 + "\n")
            return True
        else:
            logger.error("[FAIL] TASK 36 CLI GEDEELTELIJK MISLUKT")
            logger.error("="*70 + "\n")
            return False
        
    except Exception as e:
        logger.error(f"\n[FAIL] KRITIEKE FOUT: {e}")
        logger.error("="*70 + "\n")
        return False
    
    finally:
        # Cleanup
        if net_connect:
            try:
                net_connect.disconnect()
                logger.info("SSH-sessie gesloten")
            except:
                pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
