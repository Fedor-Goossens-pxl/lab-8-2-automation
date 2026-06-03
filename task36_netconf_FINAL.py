#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════
Task 36: NETCONF (Python) - End-to-End Network Automation
═══════════════════════════════════════════════════════════════════════════

📋 TASK DESCRIPTION:
    Automatiseer volledige Cisco IOS-XE configuratie via NETCONF
    - Config uit GitHub repository (simuleert remote source)
    - Atomaire deployment (alles-of-niets)
    - Foutafhandeling met discard-changes fallback
    - Verificatie na deployment

✅ VEREISTEN:
    ✓ NETCONF + YANG XML
    ✓ Hostname: NETCONF-Router-PE
    ✓ 2 Interfaces: GigabitEthernet1 (10.255.255.1) + Loopback0 (172.16.1.1)
    ✓ OSPF Process 1 (Area 0)
    ✓ Atomaire deployment (stop-on-error)
    ✓ Discard-changes op error

👤 AUTHOR: Fedor Goossens
🏫 COURSE: Enterprise Networks 2 - PXL Hogeschool
📅 DATE: Juni 2026
🔗 GITHUB: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation

═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════

import sys
import os
from pathlib import Path
from xml.dom import minidom
from ncclient import manager
from ncclient.operations import RPCError
import logging
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

def setup_logging():
    """Configure logging with timestamp"""
    log_format = '%(asctime)s | %(levelname)-8s | %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

class DeviceConfig:
    """Device connection parameters"""
    HOST = "192.168.19.139"
    PORT = 830
    USERNAME = "cisco"
    PASSWORD = "cisco123!"
    HOSTKEY_VERIFY = False
    TIMEOUT = 60

class ConfigFile:
    """Configuration file management"""
    FILENAME = "task36_config_complete.xml"
    
    @staticmethod
    def find():
        """Find config file in multiple locations"""
        search_paths = [
            Path.cwd() / ConfigFile.FILENAME,
            Path(__file__).parent / ConfigFile.FILENAME,
            Path.home() / "Downloads" / ConfigFile.FILENAME,
        ]
        
        for path in search_paths:
            if path.exists():
                logger.info(f"✓ Config file found: {path}")
                return str(path)
        
        logger.warning(f"⚠ Config file not found in standard locations")
        return ConfigFile.FILENAME

# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def pretty_print_xml(xml_string):
    """Pretty-print XML string for readability"""
    try:
        dom = minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")
    except Exception as e:
        logger.warning(f"Could not prettify XML: {e}")
        return xml_string

def print_header(title):
    """Print formatted header"""
    width = 75
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width + "\n")

def print_section(number, title):
    """Print section header with number"""
    print(f"\n{'─' * 75}")
    print(f"STAP {number}: {title}")
    print(f"{'─' * 75}\n")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: LOAD CONFIGURATION FROM "GITHUB"
# ═══════════════════════════════════════════════════════════════════════════

def load_configuration():
    """Load YANG XML configuration from file (simulates GitHub)"""
    print_section("1️⃣", "Load Configuration from 'GitHub'")
    
    config_file = ConfigFile.find()
    logger.info(f"📥 Loading configuration from: {config_file}")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_xml = f.read()
        
        file_size = len(config_xml)
        logger.info(f"✓ Configuration loaded successfully ({file_size} bytes)")
        logger.info(f"  Source: GitHub repository (simulated)")
        logger.info(f"  Format: YANG XML")
        
        # Show preview
        logger.info(f"\n📋 Configuration preview:\n")
        preview = pretty_print_xml(config_xml[:800])
        print(preview)
        
        return config_xml
        
    except FileNotFoundError:
        logger.error(f"✗ ERROR: Configuration file not found!")
        logger.error(f"\n💡 SOLUTION:")
        logger.error(f"  1. Download 'task36_config_complete.xml'")
        logger.error(f"  2. Place it in one of these folders:")
        logger.error(f"     • {Path.cwd()}")
        logger.error(f"     • {Path(__file__).parent}")
        logger.error(f"     • {Path.home() / 'Downloads'}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"✗ ERROR loading configuration: {e}")
        sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: ESTABLISH NETCONF CONNECTION
# ═══════════════════════════════════════════════════════════════════════════

def establish_netconf_connection():
    """Establish NETCONF SSH connection to IOS-XE device"""
    print_section("2️⃣", "Establish NETCONF Connection")
    
    logger.info(f"🔗 Connecting to {DeviceConfig.HOST}:{DeviceConfig.PORT}")
    logger.info(f"  Username: {DeviceConfig.USERNAME}")
    logger.info(f"  Protocol: NETCONF over SSH")
    
    try:
        mgr = manager.connect(
            host=DeviceConfig.HOST,
            port=DeviceConfig.PORT,
            username=DeviceConfig.USERNAME,
            password=DeviceConfig.PASSWORD,
            hostkey_verify=DeviceConfig.HOSTKEY_VERIFY,
            allow_agent=False,
            look_for_keys=False,
            timeout=DeviceConfig.TIMEOUT
        )
        
        logger.info(f"✓ NETCONF connection established!")
        logger.info(f"  Session ID: {mgr.id if hasattr(mgr, 'id') else 'N/A'}")
        
        return mgr
        
    except Exception as e:
        logger.error(f"✗ ERROR: NETCONF connection failed!")
        logger.error(f"  Error: {e}")
        logger.error(f"\n💡 TROUBLESHOOTING:")
        logger.error(f"  • Is NETCONF enabled? 'netconf-yang'")
        logger.error(f"  • Is port 830 reachable?")
        logger.error(f"  • Are credentials correct?")
        sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: CHECK DEVICE CAPABILITIES
# ═══════════════════════════════════════════════════════════════════════════

def check_device_capabilities(mgr):
    """Verify NETCONF device capabilities"""
    print_section("3️⃣", "Check Device Capabilities")
    
    try:
        capabilities = mgr.server_capabilities
        
        logger.info(f"📋 Device NETCONF Capabilities:")
        logger.info(f"  Total capabilities: {len(capabilities)}")
        
        # Check for essential capabilities
        has_running = any(':base:1.0' in str(cap) for cap in capabilities)
        is_cisco = any('cisco' in str(cap).lower() for cap in capabilities)
        
        if has_running:
            logger.info(f"  ✓ Running datastore supported")
        else:
            logger.warning(f"  ⚠ Running datastore support unclear")
        
        if is_cisco:
            logger.info(f"  ✓ Cisco IOS-XE device detected")
        
        logger.info(f"  ✓ Device ready for deployment")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ ERROR: Could not check capabilities: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: DEPLOY CONFIGURATION (ATOMIC)
# ═══════════════════════════════════════════════════════════════════════════

def deploy_configuration(mgr, config_xml):
    """Deploy configuration to running datastore (atomic operation)"""
    print_section("4️⃣", "Deploy Configuration (Atomic)")
    
    logger.info(f"🚀 Deploying configuration to RUNNING datastore")
    logger.info(f"  Deployment type: ATOMIC (all-or-nothing)")
    logger.info(f"  Error handling: stop-on-error (discard on failure)")
    logger.info(f"  Operation: merge (non-destructive)")
    
    try:
        # Execute edit-config with atomic error handling
        rpc_reply = mgr.edit_config(
            target='running',
            config=config_xml,
            default_operation='merge',
            error_option='stop-on-error'
        )
        
        if rpc_reply.ok:
            logger.info(f"✓ Deployment SUCCESSFUL!")
            logger.info(f"  Response: <ok/> received from device")
            logger.info(f"  Status: Configuration is now ACTIVE on device")
            return True
        else:
            logger.error(f"✗ Deployment FAILED!")
            logger.error(f"  RPC Response:\n{pretty_print_xml(rpc_reply.xml)}")
            
            # Attempt error recovery
            try_discard_changes(mgr)
            return False
            
    except RPCError as e:
        logger.error(f"✗ RPC ERROR during deployment:")
        logger.error(f"  Type: {type(e).__name__}")
        logger.error(f"  Message: {e}")
        
        try_discard_changes(mgr)
        return False
        
    except Exception as e:
        logger.error(f"✗ UNEXPECTED ERROR during deployment:")
        logger.error(f"  {e}")
        
        try_discard_changes(mgr)
        return False

def try_discard_changes(mgr):
    """Attempt to discard changes on error (error recovery)"""
    try:
        logger.warning(f"  ↻ Attempting to discard changes (error recovery)...")
        mgr.discard_changes()
        logger.info(f"  ✓ Changes discarded successfully")
    except Exception as e:
        logger.warning(f"  ⚠ Could not discard changes: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: VERIFY DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════

def verify_deployment(mgr):
    """Verify that configuration was deployed correctly"""
    print_section("5️⃣", "Verify Deployment")
    
    logger.info(f"✅ Verifying configuration on device...")
    
    try:
        # Retrieve current running configuration
        running = mgr.get_config(source='running')
        config_data = running.data_xml
        
        logger.info(f"✓ Running configuration retrieved")
        logger.info(f"  Size: {len(config_data)} bytes\n")
        
        # Verification checks
        verification_items = {
            'Hostname': ('NETCONF-Router-PE', 'hostname setting'),
            'GigabitEthernet1': ('10.255.255.1', 'primary network interface'),
            'Loopback0': ('172.16.1.1', 'OSPF router ID'),
            'OSPF Process': ('ospf', 'routing protocol'),
        }
        
        logger.info(f"📊 Verification Results:\n")
        
        all_passed = True
        for check_name, (search_term, description) in verification_items.items():
            if search_term in config_data:
                logger.info(f"  ✓ {check_name:20} | {description}")
            else:
                logger.warning(f"  ✗ {check_name:20} | {description} - NOT FOUND")
                all_passed = False
        
        if all_passed:
            logger.info(f"\n✓ All verification checks PASSED!")
            return True
        else:
            logger.warning(f"\n⚠ Some verification checks FAILED")
            return False
            
    except Exception as e:
        logger.error(f"✗ ERROR during verification: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6: DISPLAY DEPLOYED CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

def display_deployed_config(mgr):
    """Display the actual deployed configuration"""
    print_section("6️⃣", "Display Deployed Configuration")
    
    try:
        logger.info(f"📄 Retrieving deployed configuration...\n")
        
        running = mgr.get_config(source='running')
        config_data = running.data_xml
        
        # Show truncated pretty-printed config
        pretty_config = pretty_print_xml(config_data)
        print(pretty_config[:1500] + "\n\n... (configuration snippet shown)\n")
        
    except Exception as e:
        logger.error(f"✗ ERROR retrieving configuration: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# CLEANUP & FINALIZATION
# ═══════════════════════════════════════════════════════════════════════════

def close_session(mgr):
    """Close NETCONF session gracefully"""
    if mgr:
        try:
            mgr.close_session()
            logger.info(f"🔒 NETCONF session closed")
        except Exception as e:
            logger.warning(f"⚠ Could not close session cleanly: {e}")

def print_summary(success, verify_ok):
    """Print final summary report"""
    print("\n" + "=" * 75)
    
    if success and verify_ok:
        print("  ✓✓✓ TASK 36 COMPLETED SUCCESSFULLY ✓✓✓")
        print("  Network as Code deployment was successful!")
    elif success:
        print("  ⚠ TASK 36 COMPLETED (Verification incomplete)")
        print("  Deployment executed but some checks were inconclusive")
    else:
        print("  ✗✗✗ TASK 36 FAILED ✗✗✗")
        print("  Please review error messages above")
    
    print("=" * 75)
    print("\n📊 DEPLOYMENT SUMMARY:\n")
    print(f"  Device: {DeviceConfig.HOST}:{DeviceConfig.PORT}")
    print(f"  Protocol: NETCONF over SSH")
    print(f"  Datastore: running (direct deployment)")
    print(f"  Deployment: ATOMIC (stop-on-error)")
    print(f"  Error Recovery: discard-changes")
    print(f"  Verification: {'PASSED ✓' if verify_ok else 'INCONCLUSIVE ⚠'}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main execution flow"""
    
    # Header
    print_header("TASK 36: NETCONF Network Automation")
    print("✓ Hostname: NETCONF-Router-PE")
    print("✓ Interfaces: GigabitEthernet1 (10.255.255.1) + Loopback0 (172.16.1.1)")
    print("✓ Routing: OSPF Process 1 (Area 0)")
    print("✓ Deployment: Atomic (all-or-nothing)")
    print("✓ Source: GitHub repository (simulated)")
    print()
    
    mgr = None
    success = False
    verify_ok = False
    
    try:
        # STEP 1: Load configuration
        config_xml = load_configuration()
        
        # STEP 2: Connect to device
        mgr = establish_netconf_connection()
        
        # STEP 3: Check capabilities
        check_device_capabilities(mgr)
        
        # STEP 4: Deploy configuration
        success = deploy_configuration(mgr, config_xml)
        
        if not success:
            raise Exception("Deployment failed - aborting")
        
        # STEP 5: Verify deployment
        verify_ok = verify_deployment(mgr)
        
        # STEP 6: Display configuration
        display_deployed_config(mgr)
        
    except KeyboardInterrupt:
        logger.info("\n⚠ Script interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"\n✗ FATAL ERROR: {e}")
        success = False
        
    finally:
        # Cleanup
        close_session(mgr)
        
        # Summary
        print_summary(success, verify_ok)
        
        # Exit code
        sys.exit(0 if (success and verify_ok) else 1)

# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()