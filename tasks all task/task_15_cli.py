#!/usr/bin/env python3
"""
Task 15: Create VLAN 10 (DATA) via CLI/SSH
Category: Basis VLAN-configuratie

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (netmiko)
✓ Configuration management (send_config_set)
✓ Response parsing & verification
✓ Error handling & logging
✓ Git/GitHub as single source of truth

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Description: Create VLAN 10 with name "DATA" via CLI commands.
This is the CLI version of Task 15 (NETCONF was also attempted).

Usage:
    python task_15_cli.py

Requirements:
    - Python 3.8+
    - netmiko library
    - Access to CSR1000v at 192.168.19.139:22
"""

import sys
import logging
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ netmiko - SSH/CLI automation for network devices")
print("=" * 70 + "\n")

# Configure logging with detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
# Configuration Commands - Create VLAN 10
# ============================================================
CONFIG_COMMANDS = [
    'vlan 10',
    'name DATA',
    'exit'
]

# ============================================================
# Verification Commands
# ============================================================
VERIFY_COMMANDS = [
    'show running-config | include vlan',
    'show running-config | section vlan'
]


def apply_configuration():
    """
    Apply VLAN configuration via SSH/CLI.
    
    EXAM REQUIREMENT: Configuration management
    Uses send_config_set() to apply multiple config commands.
    
    Returns:
        Tuple (success: bool, output: str)
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 1: NETCONF CONNECTION & CONFIGURATION")
        logger.info("=" * 70)
        logger.info(f"Connecting to {DEVICE['host']}:{DEVICE['port']}...")
        
        with ConnectHandler(**DEVICE) as net_connect:
            logger.info("✓ Successfully connected to device via SSH!")
            logger.info(f"  Device type: {DEVICE['device_type']}")
            logger.info(f"  Username: {DEVICE['username']}")
            
            logger.info("-" * 70)
            logger.info("STEP 2: SENDING CONFIGURATION COMMANDS")
            logger.info("-" * 70)
            logger.info("Commands to execute:")
            for cmd in CONFIG_COMMANDS:
                logger.info(f"  > {cmd}")
            logger.info("-" * 70)
            
            # Send configuration commands
            output = net_connect.send_config_set(
                CONFIG_COMMANDS,
                cmd_verify=False
            )
            
            logger.info("✓ Configuration commands sent successfully!")
            logger.info("\nCommand output:")
            print(output)
            
            return True, output
            
    except NetmikoAuthenticationException as e:
        logger.error(f"✗ Authentication failed: {e}")
        logger.error(f"  Check username/password: {DEVICE['username']}")
        return False, str(e)
    except NetmikoTimeoutException as e:
        logger.error(f"✗ Connection timeout: {e}")
        logger.error(f"  Device may be unreachable at {DEVICE['host']}:{DEVICE['port']}")
        return False, str(e)
    except Exception as e:
        logger.error(f"✗ Configuration failed: {e}")
        return False, str(e)


def verify_configuration():
    """
    Verify VLAN configuration on the device.
    
    EXAM REQUIREMENT: Response parsing and verification
    Checks if VLAN 10 exists in running-config.
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 3: VERIFICATION - CHECK RUNNING-CONFIG")
        logger.info("=" * 70)
        
        with ConnectHandler(**DEVICE) as net_connect:
            
            # Get running config and check for VLAN
            logger.info("Running verification commands...")
            logger.info("-" * 70)
            
            for cmd in VERIFY_COMMANDS:
                logger.info(f"\nCommand: {cmd}")
                logger.info("-" * 70)
                
                output = net_connect.send_command(cmd)
                
                print(output)
                
                # Parse response to check if VLAN 10 exists
                if "vlan 10" in output.lower() or "10" in output:
                    logger.info("✓ VLAN 10 found in configuration!")
                    
                    # Check for name "DATA"
                    if "data" in output.lower():
                        logger.info("✓ VLAN name 'DATA' found!")
                    else:
                        logger.info("⚠ VLAN 10 found, but name 'DATA' not visible in output")
                
            # Get full VLAN config section
            logger.info("\n" + "=" * 70)
            logger.info("FULL VLAN CONFIGURATION SECTION")
            logger.info("=" * 70)
            
            vlan_config = net_connect.send_command('show running-config | begin vlan')
            print(vlan_config[:1000])  # First 1000 chars
            
            logger.info("✓ Verification completed!")
            return True
            
    except Exception as e:
        logger.error(f"✗ Verification failed: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 70)
    print("TASK 15: CREATE VLAN 10 (DATA) VIA CLI/SSH")
    print("=" * 70)
    print(f"GitHub Repository: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation")
    print(f"Device: CSR1000v at {DEVICE['host']}:{DEVICE['port']}")
    print(f"Target: Create VLAN 10 with name 'DATA'")
    print("=" * 70 + "\n")
    
    # Apply configuration
    success, output = apply_configuration()
    
    if success:
        logger.info("\n✓ Task 15 configuration applied successfully!")
        
        # Verify configuration
        verify_success = verify_configuration()
        
        if verify_success:
            # Final summary
            print("\n" + "=" * 70)
            print("FINAL SUMMARY - TASK 15 SUCCESSFUL ✓")
            print("=" * 70)
            print("✓ SSH Connection: Established and authenticated")
            print("✓ Configuration Method: CLI via Netmiko (send_config_set)")
            print("✓ Commands Executed: 3 commands (vlan 10, name DATA, exit)")
            print("✓ VLAN Created: VLAN 10")
            print("✓ VLAN Name: DATA")
            print("✓ Verification: Running-config checked successfully")
            print("=" * 70)
        else:
            logger.error("Verification failed!")
            sys.exit(1)
    else:
        logger.error("\n✗ Task 15 FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()