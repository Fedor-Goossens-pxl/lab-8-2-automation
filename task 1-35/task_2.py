#!/usr/bin/env python3
"""
Task 2: Enable / Disable Interface
Category: Basis YANG-configuratie

Description: Schakel een interface administratief in of uit via YANG.

Author: Fedor Goossens
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Usage:
    python task_2.py

Requirements:
    - Python 3.8+
    - ncclient library
    - Access to CSR1000v at 192.168.19.139:830
"""

import sys
import logging
from ncclient import manager
from ncclient.operations import RaiseMode
import xml.dom.minidom as minidom

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "admin"
PASSWORD = "123"
TIMEOUT = 30

# ============================================================
# NETCONF XML Payload
# ============================================================
XML_PAYLOAD = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>1</name>
      </GigabitEthernet>
    </interface>
  </native>
</config>
"""

# ============================================================
# Verification Filter
# ============================================================
VERIFY_FILTER = """
<filter xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
"""


def connect_to_device():
    """
    Establish NETCONF connection to the CSR1000v device.
    
    Returns:
        manager object or None on failure
    """
    try:
        logger.info(f"Connecting to {DEVICE_IP}:{DEVICE_PORT}...")
        mgr = manager.connect(
            host=DEVICE_IP,
            port=DEVICE_PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
            device_params={'name': 'iosxe'},
            timeout=TIMEOUT,
            allow_agent=False,
            look_for_keys=False
        )
        logger.info("Successfully connected to device!")
        return mgr
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def apply_configuration(mgr):
    """
    Apply the NETCONF configuration to the device.
    
    Args:
        mgr: ncclient manager object
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("Sending NETCONF edit-config request...")
        
        # Send edit-config directly to running datastore
        response = mgr.edit_config(
            target='running',
            config=XML_PAYLOAD,
            default_operation='merge'
        )
        logger.info("edit-config successful!")
        
        return True
        
    except Exception as e:
        logger.error(f"Configuration failed: {e}")
        return False


def verify_configuration(mgr):
    """
    Verify the configuration by reading running-config.
    
    Args:
        mgr: ncclient manager object
    """
    try:
        logger.info("Verifying configuration...")
        
        response = mgr.get_config(
            source='running',
            filter=VERIFY_FILTER
        )
        
        # Pretty print XML response
        print("\n" + "=" * 60)
        print("Running-config verification:")
        print("=" * 60)
        print(minidom.parseString(response.xml).toprettyxml(indent="  "))
        
    except Exception as e:
        logger.error(f"Verification failed: {e}")


def main():
    """Main execution function."""
    print("=" * 60)
    print(f"Task 2: Enable / Disable Interface")
    print("=" * 60)
    
    # Connect to device
    mgr = connect_to_device()
    if not mgr:
        logger.error("Failed to connect to device. Exiting.")
        sys.exit(1)
    
    try:
        # Apply configuration
        if apply_configuration(mgr):
            logger.info("Task 2 completed successfully!")
            
            # Verify configuration
            verify_configuration(mgr)
        else:
            logger.error("Task 2 failed!")
            sys.exit(1)
            
    finally:
        # Always close the NETCONF session
        mgr.close_session()
        logger.info("NETCONF session closed")


if __name__ == "__main__":
    main()
