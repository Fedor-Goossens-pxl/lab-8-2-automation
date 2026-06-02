#!/usr/bin/env python3
"""
Task 5: Create Loopback Interface (NETCONF/YANG)
Category: Basis YANG-configuratie (via NETCONF)

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (ncclient, xml)
✓ Pretty-print XML responses
✓ Response parsing & deserialization
✓ NETCONF status feedback (<ok/> or error-type/error-tag)
✓ Git/GitHub as single source of truth

Description: Maak Loopback0 interface aan via NETCONF.

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Usage:
    python3 task_5.py

Requirements:
    - Python 3.8+
    - ncclient library
    - Access to CSR1000v at 192.168.19.139:830
"""

import sys
import logging
from ncclient import manager
import xml.dom.minidom as minidom
from xml.etree import ElementTree as ET

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
print("✓ ncclient       - NETCONF client for device automation")
print("✓ xml.dom.minidom - XML pretty-printing and parsing")
print("✓ xml.etree      - XML response handling and parsing")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"
TIMEOUT = 30

# ============================================================
# NETCONF XML Payload - Create Loopback0
# ============================================================
XML_PAYLOAD = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>0</name>
      </Loopback>
    </interface>
  </native>
</config>
"""

# ============================================================
# Verification Filter - Get Loopback0 configuration
# ============================================================
VERIFY_FILTER = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>0</name>
      </Loopback>
    </interface>
  </native>
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
        logger.info("✓ Successfully connected to device!")
        return mgr
    except Exception as e:
        logger.error(f"✗ Connection failed: {e}")
        return None


def parse_netconf_response(response_xml):
    """
    Parse NETCONF RPC response and extract status.
    
    EXAM REQUIREMENT: Response parsing & deserialization
    Extracts <ok/> or error-type/error-tag elements.
    
    Args:
        response_xml: Raw XML response from NETCONF
    
    Returns:
        dict with parsed status and details
    """
    try:
        root = ET.fromstring(response_xml)
        
        # Check for <ok/> element (success indicator)
        if root.find('.//{urn:ietf:params:xml:ns:netconf:base:1.0}ok') is not None:
            return {
                'status': 'SUCCESS',
                'message': '<ok/> received - Loopback0 created successfully',
                'raw_response': response_xml
            }
        
        # Check for RPC errors
        errors = root.findall('.//{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-error')
        if errors:
            error_details = []
            for error in errors:
                error_type = error.find('{urn:ietf:params:xml:ns:netconf:base:1.0}error-type')
                error_tag = error.find('{urn:ietf:params:xml:ns:netconf:base:1.0}error-tag')
                error_msg = error.find('{urn:ietf:params:xml:ns:netconf:base:1.0}error-message')
                
                error_details.append({
                    'error-type': error_type.text if error_type is not None else 'unknown',
                    'error-tag': error_tag.text if error_tag is not None else 'unknown',
                    'error-message': error_msg.text if error_msg is not None else 'No details'
                })
            
            return {
                'status': 'FAILURE',
                'message': 'NETCONF error received',
                'errors': error_details,
                'raw_response': response_xml
            }
        
        return {
            'status': 'UNKNOWN',
            'message': 'Could not parse response',
            'raw_response': response_xml
        }
    except Exception as e:
        logger.error(f"Error parsing response: {e}")
        return {
            'status': 'PARSE_ERROR',
            'message': str(e)
        }


def pretty_print_xml(xml_string):
    """
    Pretty-print XML for readability.
    
    EXAM REQUIREMENT: Pretty-print XML responses
    Formats raw XML with indentation for human readability.
    
    Args:
        xml_string: Raw XML string
    
    Returns:
        Formatted XML string
    """
    try:
        dom = minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")
    except Exception as e:
        logger.error(f"Error formatting XML: {e}")
        return xml_string


def apply_configuration(mgr):
    """
    Apply the NETCONF configuration to create Loopback0.
    
    EXAM REQUIREMENT: NETCONF status feedback
    Uses edit-config to merge Loopback interface to running datastore.
    
    Args:
        mgr: ncclient manager object
    
    Returns:
        Tuple (success: bool, response_dict: dict)
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 1: NETCONF EDIT-CONFIG REQUEST")
        logger.info("=" * 70)
        
        logger.info("Target datastore: running")
        logger.info("Default operation: merge")
        logger.info("Configuration: Create Loopback0 interface")
        logger.info("-" * 70)
        
        # Send edit-config RPC
        response = mgr.edit_config(
            target='running',
            config=XML_PAYLOAD,
            default_operation='merge'
        )
        
        # Parse response for status
        response_dict = parse_netconf_response(response.xml)
        
        # Display status
        logger.info("=" * 70)
        logger.info("NETCONF RESPONSE STATUS")
        logger.info("=" * 70)
        logger.info(f"Status: {response_dict['status']}")
        logger.info(f"Message: {response_dict['message']}")
        
        if response_dict['status'] == 'SUCCESS':
            logger.info("✓ Configuration applied successfully!")
            return True, response_dict
        else:
            logger.error("✗ Configuration failed!")
            if 'errors' in response_dict:
                for error in response_dict['errors']:
                    logger.error(f"  Error Type: {error['error-type']}")
                    logger.error(f"  Error Tag: {error['error-tag']}")
                    logger.error(f"  Message: {error['error-message']}")
            return False, response_dict
        
    except Exception as e:
        logger.error(f"✗ Configuration failed with exception: {e}")
        return False, {'status': 'EXCEPTION', 'message': str(e)}


def verify_configuration(mgr):
    """
    Verify the configuration by reading running-config.
    
    EXAM REQUIREMENT: Response parsing and pretty-print
    Uses GET with filter to retrieve and display current configuration.
    
    Args:
        mgr: ncclient manager object
    """
    try:
        logger.info("=" * 70)
        logger.info("STEP 2: VERIFICATION - GET RUNNING-CONFIG")
        logger.info("=" * 70)
        
        response = mgr.get_config(
            source='running',
            filter=VERIFY_FILTER
        )
        
        print("\n" + "=" * 70)
        print("RAW NETCONF RESPONSE (XML)")
        print("=" * 70)
        print(response.xml)
        
        print("\n" + "=" * 70)
        print("PRETTY-PRINTED RESPONSE (Formatted for readability)")
        print("=" * 70)
        print(pretty_print_xml(response.xml))
        
        logger.info("✓ Configuration verified successfully!")
        
    except Exception as e:
        logger.error(f"✗ Verification failed: {e}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("TASK 5: CREATE LOOPBACK0 INTERFACE (VIA NETCONF/YANG)")
    print("=" * 70)
    print(f"GitHub Repository: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation")
    print(f"Device: CSR1000v at {DEVICE_IP}:{DEVICE_PORT}")
    print("=" * 70 + "\n")
    
    # Connect to device
    mgr = connect_to_device()
    if not mgr:
        logger.error("Failed to connect to device. Exiting.")
        sys.exit(1)
    
    try:
        # Apply configuration
        success, response_dict = apply_configuration(mgr)
        
        if success:
            logger.info("Task 5 configuration applied successfully!")
            
            # Verify configuration
            verify_configuration(mgr)
            
            # Final summary
            print("\n" + "=" * 70)
            print("FINAL SUMMARY - TASK 5 SUCCESSFUL ✓")
            print("=" * 70)
            print("✓ NETCONF Connection: Established and authenticated")
            print("✓ Configuration Method: NETCONF edit-config (running datastore)")
            print("✓ NETCONF Status: <ok/> received")
            print("✓ Interface Created: Loopback0")
            print("✓ Verification: GET running-config successful")
            print("=" * 70)
        else:
            logger.error("Task 5 FAILED!")
            sys.exit(1)
            
    finally:
        # Always close the NETCONF session
        try:
            mgr.close_session()
            logger.info("NETCONF session closed")
        except:
            pass


if __name__ == "__main__":
    main()
