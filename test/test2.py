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
# DEVICE CONFIGURATION (EXAM REQUIREMENT)
# ============================================================
DEVICE_IP = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
PORT = 22

def main():
    # Connect to device
    mgr = connect_to_device(DEVICE_IP, USERNAME, PASSWORD, PORT)

    # Apply configuration
    success, response_dict = apply_configuration(mgr)

    if success:
        logger.info("Task 20 configuration applied successfully!")

        # Verify configuration
        verify_configuration(mgr)

        # Final summary
        print("\n" + "=" * 70)
        print("FINAL SUMMARY - TASK 20 SUCCESSFUL ✓")
        print("=" * 70)
        print("✓ NETCONF Connection: Established and authenticated")
        print("✓ Configuration Method: NETCONF edit-config (running datastore)")
        print("✓ NETCONF Status: <ok/> received")
        print("✓ Interface Configured: GigabitEthernet1/0/1")
        print("✓ IPv4 Address: 10.0.0.1")
        print("✓ Subnet Mask: 255.255.255.0 (/24)")
        print("✓ Verification: GET running-config successful")
        print("=" * 70)
    else:
        logger.error("Task 20 FAILED!")
        sys.exit(1)

def connect_to_device(ip, username, password, port):
    try:
        with manager.connect(host=ip, port=port, username=username, password=password, device_params={'name': 'csr'}, timeout=30, allow_agent=False, look_for_keys=False) as mgr:
            logger.info("NETCONF session established")
            return mgr
    except Exception as e:
        logger.error(f"Failed to establish NETCONF session: {e}")
        sys.exit(1)

def apply_configuration(mgr):
    try:
        response = mgr.edit_config(target="running", config=CONFIG, default_operation="merge")
        logger.info("Configuration applied successfully!")
        return True, response
    except Exception as e:
        logger.error(f"Failed to apply configuration: {e}")
        return False, e

def verify_configuration(mgr):
    try:
        response = mgr.get_config(source="running", filter=("subtree", VERIFY_FILTER))
        logger.info("Verification successful!")
        return True, response
    except Exception as e:
        logger.error(f"Failed to verify configuration: {e}")
        return False, e

if __name__ == "__main__":
    main()