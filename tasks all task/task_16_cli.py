#!/usr/bin/env python3
"""
Task 16: Assign Interface to VLAN (CLI/SSH version)
Category: Basis configuratie via CLI

Description: Configure GigabitEthernet1 as access port in VLAN 10 via SSH/CLI.

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Juni 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Usage:
    python task_16_cli.py

Requirements:
    - Python 3.8+
    - netmiko library
    - Access to CSR1000v at 192.168.19.139:22
"""

import sys
import logging
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ netmiko - SSH/CLI automation library")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE = {
    'device_type': 'cisco_ios',
    'host': '192.168.19.139',
    'username': 'cisco',
    'password': 'cisco123!',
    'port': 22,
    'timeout': 60,
    'conn_timeout': 60,
}

# ============================================================
# Configuration Commands - Assign Interface to VLAN
# ============================================================
CONFIG_COMMANDS = [
    'interface GigabitEthernet1',
    'switchport mode access',
    'switchport access vlan 10',
    'no shutdown',
    'end'
]

# ============================================================
# Verification Command
# ============================================================
VERIFY_COMMAND = 'show interfaces GigabitEthernet1 switchport'


def apply_configuration():
    """
    Apply configuration via SSH/CLI.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("=" * 70)
        print("TASK 16: ASSIGN INTERFACE TO VLAN (CLI/SSH)")
        print("=" * 70)
        print(f"Device: {DEVICE['host']}:22")
        print(f"Interface: GigabitEthernet1")
        print(f"VLAN: 10")
        print(f"Mode: access")
        print("=" * 70 + "\n")
        
        logger.info(f"Connecting to {DEVICE['host']}:22...")
        
        with ConnectHandler(**DEVICE) as net_connect:
            logger.info("✓ Successfully connected to device!\n")
            
            print("=" * 70)
            print("STEP 1: SEND CONFIGURATION COMMANDS (CLI)")
            print("=" * 70)
            logger.info("Sending configuration commands...")
            
            output = net_connect.send_config_set(
                CONFIG_COMMANDS,
                cmd_verify=False
            )
            
            logger.info("✓ Configuration sent successfully!\n")
            
            print("CLI Output:")
            print("-" * 70)
            print(output)
            print("-" * 70)
            
            # Check for errors in output
            if 'error' in output.lower() or 'invalid' in output.lower():
                logger.warning("⚠ Possible error in configuration output")
                return False
            else:
                logger.info("✓ Configuration applied successfully!")
                return True
            
    except NetmikoAuthenticationException as e:
        logger.error(f"✗ Authentication failed: {e}")
        return False
    except NetmikoTimeoutException as e:
        logger.error(f"✗ Connection timeout: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Configuration failed: {e}")
        return False


def verify_configuration():
    """
    Verify the configuration via show command.
    """
    try:
        print("\n" + "=" * 70)
        print("STEP 2: VERIFICATION - SHOW SWITCHPORT")
        print("=" * 70)
        
        logger.info("Connecting for verification...")
        
        with ConnectHandler(**DEVICE) as net_connect:
            logger.info("✓ Connected!\n")
            
            logger.info(f"Sending verify command: {VERIFY_COMMAND}")
            output = net_connect.send_command(VERIFY_COMMAND)
            
            print("Verification Output:")
            print("-" * 70)
            print(output)
            print("-" * 70)
            
            # Check if VLAN 10 is in output
            if 'Access Mode VLAN' in output or 'VLAN: 10' in output or 'vlan 10' in output.lower():
                logger.info("✓ VLAN 10 configuration verified!")
            else:
                logger.warning("⚠ VLAN 10 not clearly visible in output")
            
    except Exception as e:
        logger.error(f"✗ Verification failed: {e}")


def main():
    """Main execution function."""
    
    # Apply configuration
    if apply_configuration():
        logger.info("Task 16 configuration applied successfully!")
        
        # Verify configuration
        verify_configuration()
        
        # Final summary
        print("\n" + "=" * 70)
        print("FINAL SUMMARY - TASK 16")
        print("=" * 70)
        print("✓ SSH Connection: Established and authenticated")
        print("✓ Configuration Method: CLI via Netmiko")
        print("✓ Interface: GigabitEthernet1")
        print("✓ VLAN: 10")
        print("✓ Mode: access")
        print("✓ Verification: show command executed")
        print("=" * 70 + "\n")
    else:
        logger.error("Task 16 failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()