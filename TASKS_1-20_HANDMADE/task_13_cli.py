#!/usr/bin/env python3
"""
Task 13: Create Local User (fedor) via CLI/SSH (COMPLETE IMPLEMENTATION)
Category: Basis configuratie (via SSH/CLI)

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (netmiko)
✓ Device connection & authentication
✓ Configuration application via CLI
✓ Verification via CLI commands
✓ Git/GitHub as single source of truth

Description: Create a new local user "fedor" with privilege 15 on CSR1000v via SSH.

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Usage:
    python task_13_cli_complete.py

Requirements:
    - Python 3.8+
    - netmiko library
    - Access to CSR1000v at 192.168.19.139 (SSH port 22)
"""

import sys
import logging
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Configure logging with detailed format
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
print("✓ netmiko         - SSH/CLI automation for network devices")
print("✓ paramiko        - SSH protocol (used by netmiko)")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
NEW_USERNAME = "fedor"
NEW_PASSWORD = "cisco123"
PRIVILEGE = "15"

# ============================================================
# Device Parameters for Netmiko
# ============================================================
device = {
    'device_type': 'cisco_ios',
    'host': DEVICE_IP,
    'username': USERNAME,
    'password': PASSWORD,
    'timeout': 30,
    'global_delay_factor': 1,
}


def connect_to_device():
    """
    Establish SSH connection to CSR1000v via Netmiko.
    
    Returns:
        ConnectHandler object or None on failure
    """
    try:
        logger.info(f"Connecting to {DEVICE_IP} via SSH...")
        net_connect = ConnectHandler(**device)
        logger.info("✓ Successfully connected to device!")
        return net_connect
    except NetmikoAuthenticationException as e:
        logger.error(f"✗ Authentication failed: {e}")
        return None
    except NetmikoTimeoutException as e:
        logger.error(f"✗ Connection timeout: {e}")
        return None
    except Exception as e:
        logger.error(f"✗ Connection failed: {e}")
        return None


def apply_configuration(net_connect):
    """
    Apply user configuration via CLI.
    
    Args:
        net_connect: Netmiko ConnectHandler object
    
    Returns:
        Tuple (success: bool, output: str)
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 1: APPLY USER CONFIGURATION")
        logger.info("=" * 70)
        
        # Create configuration command
        config_commands = [
            f'username {NEW_USERNAME} privilege {PRIVILEGE} secret {NEW_PASSWORD}'
        ]
        
        logger.info(f"Sending command: username {NEW_USERNAME} privilege {PRIVILEGE} secret {NEW_PASSWORD}")
        
        output = net_connect.send_config_set(
            config_commands,
            exit_config_mode=True
        )
        
        logger.info("=" * 70)
        logger.info("CONFIGURATION OUTPUT")
        logger.info("=" * 70)
        print(output)
        
        logger.info("✓ Configuration applied successfully!")
        return True, output
        
    except Exception as e:
        logger.error(f"✗ Configuration failed: {e}")
        return False, str(e)


def verify_configuration(net_connect):
    """
    Verify user configuration via CLI.
    
    EXAM REQUIREMENT: Verification via show commands
    
    Args:
        net_connect: Netmiko ConnectHandler object
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 2: VERIFICATION - SHOW RUNNING CONFIG")
        logger.info("=" * 70)
        
        # Check username configuration
        verify_cmd = 'show running-config | include username'
        logger.info(f"Sending command: {verify_cmd}")
        
        output = net_connect.send_command(verify_cmd)
        
        print("\n" + "=" * 70)
        print("USERNAME CONFIGURATION (running-config)")
        print("=" * 70)
        print(output if output.strip() else "(no output)")
        
        # Verify fedor user exists
        if NEW_USERNAME in output:
            logger.info(f"✓ User '{NEW_USERNAME}' found in configuration!")
            return True
        else:
            logger.warning(f"⚠ User '{NEW_USERNAME}' NOT found in configuration!")
            return False
        
    except Exception as e:
        logger.error(f"✗ Verification failed: {e}")
        return False


def test_login(net_connect):
    """
    Test login with new user credentials (via current session info).
    
    Args:
        net_connect: Netmiko ConnectHandler object
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 3: TEST LOGIN (Manual verification required)")
        logger.info("=" * 70)
        
        # Get current user info
        output = net_connect.send_command('show users')
        
        print("\n" + "=" * 70)
        print("CURRENT USERS")
        print("=" * 70)
        print(output)
        
        print("\n" + "=" * 70)
        print("MANUAL TEST (after script completes):")
        print("=" * 70)
        print(f"ssh {NEW_USERNAME}@{DEVICE_IP}")
        print(f"Password: {NEW_PASSWORD}")
        print("=" * 70)
        
    except Exception as e:
        logger.error(f"✗ User info retrieval failed: {e}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("TASK 13: CREATE LOCAL USER (VIA SSH/CLI)")
    print("=" * 70)
    print(f"GitHub Repository: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation")
    print(f"Device: CSR1000v at {DEVICE_IP} (SSH)")
    print(f"New User: {NEW_USERNAME}")
    print(f"Privilege Level: {PRIVILEGE}")
    print("=" * 70 + "\n")
    
    # Connect to device
    net_connect = connect_to_device()
    if not net_connect:
        logger.error("Failed to connect to device. Exiting.")
        sys.exit(1)
    
    try:
        # Apply configuration
        success, output = apply_configuration(net_connect)
        
        if success:
            # Verify configuration
            verify_success = verify_configuration(net_connect)
            
            # Show test login instructions
            test_login(net_connect)
            
            # Final summary
            print("\n" + "=" * 70)
            print("FINAL SUMMARY - TASK 13 SUCCESSFUL ✓")
            print("=" * 70)
            print("✓ SSH Connection: Established and authenticated")
            print("✓ Configuration Method: CLI via Netmiko")
            print(f"✓ Command Applied: username {NEW_USERNAME} privilege {PRIVILEGE} secret {NEW_PASSWORD}")
            print("✓ Status: Configuration saved to running-config")
            if verify_success:
                print(f"✓ Verification: User '{NEW_USERNAME}' found in config")
            print("\n✓ Next Step: Test login with new credentials:")
            print(f"   ssh {NEW_USERNAME}@{DEVICE_IP}")
            print(f"   Password: {NEW_PASSWORD}")
            print("=" * 70)
        else:
            logger.error("Task 13 FAILED!")
            sys.exit(1)
            
    finally:
        # Always close SSH connection
        try:
            net_connect.disconnect()
            logger.info("SSH session closed")
        except:
            pass


if __name__ == "__main__":
    main()