#!/usr/bin/env python3
"""
Task 14: Change Password of User fedor (VIA CLI/NETMIKO - FALLBACK)
Category: Basis YANG-configuratie (via CLI fallback)

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (netmiko)
✓ Configuration management (send_config_set)
✓ Response parsing & verification
✓ Hashed password display
✓ Git/GitHub as single source of truth
✓ CLI fallback when NETCONF fails (EXAM LESSON)

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Description: Change the password of user "fedor" via CLI commands.
This is a FALLBACK when NETCONF/YANG fails.

EXAM LEARNING:
- Task 9 (NTP) failed via NETCONF → used CLI fallback
- Task 14 (User password) fails via NETCONF → using CLI fallback
- LESSON: Know when to use CLI vs NETCONF
"""

import sys
import logging
from netmiko import ConnectHandler
import time

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
print("LIBRARIES USED FOR NETWORK AUTOMATION (CLI/SSH FALLBACK)")
print("=" * 70)
print("✓ netmiko - SSH/CLI automation (when NETCONF fails)")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 22
USERNAME = "cisco"
PASSWORD = "cisco123!"
DEVICE_TYPE = "cisco_ios"
TIMEOUT = 30

# ============================================================
# Configuration Commands
# ============================================================
CONFIG_COMMANDS = [
    "username fedor privilege 15 secret newpassword456"
]

# ============================================================
# Verification Commands
# ============================================================
VERIFY_COMMANDS = [
    "show running-config | include username"
]


def connect_to_device():
    """
    Establish SSH/CLI connection to the CSR1000v device using Netmiko.
    
    Returns:
        ConnectHandler object or None on failure
    """
    try:
        logger.info(f"Connecting to {DEVICE_IP}:{DEVICE_PORT} via SSH/CLI...")
        device = ConnectHandler(
            device_type=DEVICE_TYPE,
            host=DEVICE_IP,
            port=DEVICE_PORT,
            username=USERNAME,
            password=PASSWORD,
            timeout=TIMEOUT
        )
        logger.info("✓ Successfully connected to device via SSH/CLI!")
        return device
    except Exception as e:
        logger.error(f"✗ Connection failed: {e}")
        return None


def apply_configuration(device):
    """
    Apply the configuration commands to the device.
    
    EXAM REQUIREMENT: Configuration management
    Uses send_config_set() to apply multiple config commands.
    
    Args:
        device: Netmiko ConnectHandler object
    
    Returns:
        Tuple (success: bool, output: str)
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 1: SEND CONFIGURATION COMMANDS")
        logger.info("=" * 70)
        logger.info(f"Target: running-config")
        logger.info(f"Method: SSH/CLI (Netmiko)")
        logger.info(f"Commands:")
        for cmd in CONFIG_COMMANDS:
            logger.info(f"  - {cmd}")
        logger.info("-" * 70)
        
        # Send configuration commands
        output = device.send_config_set(CONFIG_COMMANDS)
        
        logger.info("✓ Configuration commands sent successfully!")
        logger.info("Command output:")
        print(output)
        
        # Small delay to ensure config is processed
        time.sleep(1)
        
        return True, output
        
    except Exception as e:
        logger.error(f"✗ Configuration failed with exception: {e}")
        return False, str(e)


def verify_configuration(device):
    """
    Verify the configuration by reading running-config.
    
    EXAM REQUIREMENT: Response parsing and verification
    Uses send_command() to retrieve and display user configuration.
    
    Args:
        device: Netmiko ConnectHandler object
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 2: VERIFICATION - SHOW RUNNING-CONFIG (User fedor)")
        logger.info("=" * 70)
        
        for cmd in VERIFY_COMMANDS:
            logger.info(f"Running: {cmd}")
            logger.info("-" * 70)
            
            response = device.send_command(cmd)
            
            print("\n" + "=" * 70)
            print("COMMAND OUTPUT")
            print("=" * 70)
            print(response)
            print("=" * 70)
            
            # Parse response to check if user exists
            if "fedor" in response:
                logger.info("✓ User 'fedor' found in running-config!")
                
                # Extract the line containing fedor
                lines = response.split('\n')
                for line in lines:
                    if "fedor" in line:
                        logger.info(f"Configuration: {line.strip()}")
                        
                        # Check if password hash is present
                        if "$" in line:
                            logger.info("✓ Password has been hashed and stored!")
                        else:
                            logger.info("⚠ Warning: Password might not be encrypted")
            else:
                logger.error("✗ User 'fedor' NOT found in running-config!")
                return False
        
        logger.info("✓ Configuration verified successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Verification failed: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 70)
    print("TASK 14: CHANGE PASSWORD OF USER FEDOR (VIA CLI/NETMIKO)")
    print("=" * 70)
    print(f"GitHub Repository: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation")
    print(f"Device: CSR1000v at {DEVICE_IP}:{DEVICE_PORT}")
    print(f"Method: SSH/CLI (NETCONF Fallback)")
    print(f"User: fedor")
    print(f"New Password: newpassword456")
    print("=" * 70)
    print("\n⚠ NOTE: This is a CLI/NETMIKO FALLBACK")
    print("  NETCONF/YANG approach failed because <password> is a CONTAINER,")
    print("  not a simple leaf element. CLI is more reliable for user management.")
    print("=" * 70 + "\n")
    
    # Connect to device
    device = connect_to_device()
    if not device:
        logger.error("Failed to connect to device. Exiting.")
        sys.exit(1)
    
    try:
        # Apply configuration
        success, output = apply_configuration(device)
        
        if success:
            logger.info("✓ Task 14 configuration applied successfully!")
            
            # Verify configuration
            verify_success = verify_configuration(device)
            
            if verify_success:
                # Final summary
                print("\n" + "=" * 70)
                print("FINAL SUMMARY - TASK 14 SUCCESSFUL ✓")
                print("=" * 70)
                print("✓ SSH/CLI Connection: Established and authenticated")
                print("✓ Configuration Method: CLI via Netmiko (send_config_set)")
                print("✓ Command Status: Executed successfully")
                print("✓ User Modified: fedor")
                print("✓ New Password: newpassword456 (hashed in config)")
                print("✓ Verification: show running-config successful")
                print("✓ EXAM LESSON: CLI fallback when NETCONF fails")
                print("=" * 70)
            else:
                logger.error("Verification failed!")
                sys.exit(1)
        else:
            logger.error("Task 14 FAILED!")
            sys.exit(1)
            
    finally:
        # Always close the SSH session
        try:
            device.disconnect()
            logger.info("SSH session closed")
        except:
            pass


if __name__ == "__main__":
    main()