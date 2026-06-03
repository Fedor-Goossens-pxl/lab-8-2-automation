#!/usr/bin/env python3
"""
Task 17: Enable SNMP Community (CLI/SSH version)
Category: Basis YANG-configuratie

Description: Configure SNMP read-only community via SSH/CLI.

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Juni 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Usage:
    python task_17_cli.py

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
# SNMP Community Configuration Commands
# ============================================================
CONFIG_COMMANDS = [
    'snmp-server community public RO',
    'end'
]

# ============================================================
# Verification Command
# ============================================================
VERIFY_COMMAND = 'show snmp community'


def apply_configuration():
    """
    Apply SNMP configuration via SSH/CLI.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("=" * 70)
        print("TASK 17: ENABLE SNMP COMMUNITY (CLI/SSH)")
        print("=" * 70)
        print(f"Device: {DEVICE['host']}:22")
        print(f"Community: public")
        print(f"Access: Read-Only (RO)")
        print("=" * 70 + "\n")
        
        logger.info(f"Connecting to {DEVICE['host']}:22...")
        
        with ConnectHandler(**DEVICE) as net_connect:
            logger.info("✓ Successfully connected to device!\n")
            
            print("=" * 70)
            print("STEP 1: SEND CONFIGURATION COMMANDS (CLI)")
            print("=" * 70)
            logger.info("Sending SNMP configuration commands...")
            
            output = net_connect.send_config_set(
                CONFIG_COMMANDS,
                cmd_verify=False
            )
            
            logger.info("✓ Configuration sent successfully!\n")
            
            print("CLI Output:")
            print("-" * 70)
            print(output)
            print("-" * 70)
            
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
    Verify SNMP configuration via show command.
    """
    try:
        print("\n" + "=" * 70)
        print("STEP 2: VERIFICATION - SHOW SNMP COMMUNITY")
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
            
            if 'public' in output.lower() or 'RO' in output:
                logger.info("✓ SNMP community 'public' (RO) verified!")
            else:
                logger.warning("⚠ SNMP community not clearly visible in output")
            
    except Exception as e:
        logger.error(f"✗ Verification failed: {e}")


def main():
    """Main execution function."""
    
    # Apply configuration
    if apply_configuration():
        logger.info("Task 17 configuration applied successfully!")
        
        # Verify configuration
        verify_configuration()
        
        # Final summary
        print("\n" + "=" * 70)
        print("FINAL SUMMARY - TASK 17")
        print("=" * 70)
        print("✓ SSH Connection: Established and authenticated")
        print("✓ Configuration Method: CLI via Netmiko")
        print("✓ SNMP Community: public")
        print("✓ Access Level: Read-Only (RO)")
        print("✓ Verification: show snmp community executed")
        print("=" * 70 + "\n")
    else:
        logger.error("Task 17 failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()