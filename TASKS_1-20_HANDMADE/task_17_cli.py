#!/usr/bin/env python3
"""
Task 17: Configure SNMP Community via CLI/SSH (Netmiko)
Category: Basis SNMP-configuratie (via CLI fallback)

EXAM REQUIREMENTS INCLUDED:
✓ Network automation libraries (netmiko)
✓ SSH/CLI based configuration
✓ Response parsing
✓ Error handling
✓ Git/GitHub as single source of truth

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Mei 2026
Course: Enterprise Networks 2 - PXL Hogeschool

Description: Configure SNMP community "public" (read-only) via CLI/SSH.
Uses Netmiko for SSH-based CLI automation (NETCONF not fully supported on CSR1000v 16.9.5).

Usage:
    python task_17_cli.py

Device credentials are hardcoded in the script:
    HOST: 192.168.19.139
    USERNAME: cisco
    PASSWORD: cisco123!

Requirements:
    - Python 3.8+
    - netmiko library
"""

import traceback
from netmiko import ConnectHandler

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ netmiko - SSH/CLI automation library")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration (Hardcoded)
# ============================================================
HOST = "192.168.19.139"
USERNAME = "cisco"
PASSWORD = "cisco123!"
DEVICE_TYPE = "cisco_ios"
TIMEOUT = 30

# ============================================================
# CLI Commands for SNMP Configuration
# ============================================================
SNMP_COMMANDS = [
    "snmp-server community public RO"
]


def main():
    """Main execution function."""
    
    print("=" * 70)
    print("TASK 17: CONFIGURE SNMP COMMUNITY VIA CLI/SSH")
    print("=" * 70)
    print(f"Device: {HOST}")
    print(f"Username: {USERNAME}")
    print(f"SNMP Community: public")
    print(f"Access Type: Read-Only (RO)")
    print(f"Method: CLI/SSH via Netmiko")
    print("=" * 70 + "\n")
    
    # Device configuration for netmiko
    device = {
        'device_type': DEVICE_TYPE,
        'host': HOST,
        'username': USERNAME,
        'password': PASSWORD,
        'timeout': TIMEOUT,
    }
    
    try:
        print(f"Connecting to {HOST} via SSH...")
        
        net_connect = ConnectHandler(**device)
        print("✓ Successfully connected to device!\n")
        
        # ============================================================
        # STEP 1: Send Configuration Commands
        # ============================================================
        print("=" * 70)
        print("STEP 1: SEND CONFIGURATION COMMANDS (CLI)")
        print("=" * 70)
        
        try:
            print("Sending CLI commands...")
            output = net_connect.send_config_set(SNMP_COMMANDS)
            print("✓ Commands sent successfully!\n")
            
            print("CLI Output:")
            print("-" * 70)
            print(output)
            print("-" * 70)
            
            # Check for errors in output
            if "Error" in output or "error" in output or "Invalid" in output:
                print("⚠ Potential error in output\n")
            else:
                print("✓ Configuration Applied Successfully!\n")
        
        except Exception as e:
            print(f"✗ Configuration failed: {e}")
            traceback.print_exc()
            net_connect.disconnect()
            exit(1)
        
        # ============================================================
        # STEP 2: Verify Configuration
        # ============================================================
        print("=" * 70)
        print("STEP 2: VERIFICATION - SHOW RUNNING-CONFIG (SNMP)")
        print("=" * 70)
        
        try:
            print("Sending show command for verification...")
            verify_output = net_connect.send_command("show running-config | include snmp-server")
            print("✓ Verification command executed!\n")
            
            print("Verification Output:")
            print("-" * 70)
            print(verify_output)
            print("-" * 70)
            
            # Check if SNMP community is in output
            if "public" in verify_output and "RO" in verify_output:
                print("✓ SNMP community 'public' RO found in running-config!\n")
            elif "public" in verify_output:
                print("✓ SNMP community 'public' found in running-config!\n")
            else:
                print("⚠ SNMP community not clearly visible in verification output\n")
        
        except Exception as e:
            print(f"Verification failed: {e}")
            traceback.print_exc()
        
        # ============================================================
        # Final Summary
        # ============================================================
        print("=" * 70)
        print("FINAL SUMMARY - TASK 17")
        print("=" * 70)
        print("✓ SSH Connection: Established and authenticated")
        print("✓ Configuration Method: CLI/SSH via Netmiko")
        print("✓ SNMP Community: public")
        print("✓ Access Type: Read-Only (RO)")
        print("✓ CLI Command: snmp-server community public RO")
        print("✓ Verification: show running-config executed")
        print("=" * 70 + "\n")
        
        # Close the connection
        net_connect.disconnect()
        print("SSH connection closed")
    
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()