#!/usr/bin/env python3
"""
Task 9: Configure NTP Server (CLI/SSH version)
Category: Basis YANG-configuratie

Description: Configureer een NTP-server via SSH/CLI.

Author: Fedor Goossens
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Usage:
    python task_9_cli.py

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
# Configuration Commands
# ============================================================
CONFIG_COMMANDS = [
    'ntp server 193.190.230.65',
    'end'
]


def apply_configuration():
    """
    Apply configuration via SSH/CLI.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Connecting to {DEVICE['host']}:22...")
        
        with ConnectHandler(**DEVICE) as net_connect:
            logger.info("Successfully connected to device!")
            
            logger.info("Sending configuration commands...")
            output = net_connect.send_config_set(
                CONFIG_COMMANDS,
                cmd_verify=False
            )
            
            logger.info("Configuration sent successfully!")
            logger.info("\nConfiguration output:")
            print(output)
            
            return True
            
    except NetmikoAuthenticationException as e:
        logger.error(f"Authentication failed: {e}")
        return False
    except NetmikoTimeoutException as e:
        logger.error(f"Connection timeout: {e}")
        return False
    except Exception as e:
        logger.error(f"Configuration failed: {e}")
        return False


def verify_configuration():
    """
    Verify the configuration by reading running-config.
    """
    try:
        logger.info("Verifying configuration...")
        
        with ConnectHandler(**DEVICE) as net_connect:
            output = net_connect.send_command('show running-config | include ntp')
            
            print("\n" + "=" * 60)
            print("Running-config verification:")
            print("=" * 60)
            print(output)
            
    except Exception as e:
        logger.error(f"Verification failed: {e}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Task 9: Configure NTP Server")
    print("=" * 60)
    
    # Apply configuration
    if apply_configuration():
        logger.info("Task 9 completed successfully!")
        
        # Verify configuration
        verify_configuration()
    else:
        logger.error("Task 9 failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
