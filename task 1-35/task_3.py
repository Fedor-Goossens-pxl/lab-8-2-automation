#!/usr/bin/env python3
"""
Task [N]: [TASK_NAME]
Category: [CATEGORY]

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (ncclient/requests, xml, json)
✓ Pretty-print XML/JSON responses
✓ Response parsing & deserialization
✓ NETCONF status feedback (<ok/> or error-type/error-tag)
✓ HTTP status codes (RESTCONF)
✓ Git/GitHub as single source of truth

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool
"""

import sys
import logging
from ncclient import manager
import xml.dom.minidom as minidom
from xml.etree import ElementTree as ET

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
print("✓ ncclient       - NETCONF client for device automation")
print("✓ xml.dom.minidom - XML pretty-printing and parsing")
print("✓ xml.etree      - XML response handling")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE_IP = "192.168.19.139"
DEVICE_PORT = 830
USERNAME = "admin"
PASSWORD = "123"
TIMEOUT = 30


def connect_to_device():
    """Establish NETCONF connection."""
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
    
    Returns:
        dict with parsed status and details
    """
    try:
        root = ET.fromstring(response_xml)
        
        # Check for <ok/> element
        if root.find('.//{urn:ietf:params:xml:ns:netconf:base:1.0}ok') is not None:
            return {
                'status': 'SUCCESS',
                'message': '<ok/> received - Operation successful',
                'raw_response': response_xml
            }
        
        # Check for errors
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
    """
    try:
        dom = minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")
    except Exception as e:
        logger.error(f"Error formatting XML: {e}")
        return xml_string


def main():
    """Main execution function."""
    print("=" * 70)
    print("TASK [N]: [TASK_NAME]")
    print("=" * 70)
    print(f"GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation")
    print(f"Device: CSR1000v at {DEVICE_IP}:{DEVICE_PORT}")
    print("=" * 70 + "\n")
    
    # Connect to device
    mgr = connect_to_device()
    if not mgr:
        logger.error("Failed to connect to device. Exiting.")
        sys.exit(1)
    
    try:
        # TODO: Add task-specific logic here
        logger.info("Task logic to be implemented")
        
    finally:
        try:
            mgr.close_session()
            logger.info("NETCONF session closed")
        except:
            pass


if __name__ == "__main__":
    main()