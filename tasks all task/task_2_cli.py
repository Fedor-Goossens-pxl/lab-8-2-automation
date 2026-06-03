#!/usr/bin/env python3
"""
Task 2: Enable / Disable Interface (CLI/Netmiko)
Schakel een interface administratief in of uit via CLI commands.

Author: Fedor Goossens
GitHub: https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
Date: Juni 2026
Course: Enterprise Networks 2 - PXL Hogeschool
"""

from netmiko import ConnectHandler

# ============================================================
# LIBRARIES USED (EXAM REQUIREMENT)
# ============================================================
print("\n" + "=" * 70)
print("LIBRARIES USED FOR NETWORK AUTOMATION")
print("=" * 70)
print("✓ netmiko - SSH/CLI network device automation")
print("=" * 70 + "\n")

# ============================================================
# Device Configuration
# ============================================================
DEVICE = {
    'device_type': 'cisco_ios',
    'host': '192.168.19.139',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'cisco123!',
}

# ============================================================
# CLI Commands
# ============================================================
CONFIG_COMMANDS = [
    'interface loopback 0',
    'ip address 10.99.0.1 255.255.255.255',
    'no shutdown',
    'exit',
]

DISABLE_COMMANDS = [
    'interface loopback 0',
    'shutdown',
    'exit',
]

ENABLE_COMMANDS = [
    'interface loopback 0',
    'no shutdown',
    'exit',
]


def main():
    print("=" * 70)
    print("TASK 2: ENABLE / DISABLE INTERFACE (CLI)")
    print("=" * 70)
    print(f"Device: {DEVICE['host']}")
    print(f"Interface: Loopback0")
    print("=" * 70 + "\n")

    try:
        # ============================================================
        # STEP 1: Connect to device
        # ============================================================
        print("[1] Connecting via SSH/CLI...")
        conn = ConnectHandler(**DEVICE)
        print("✓ Connected!\n")

        # ============================================================
        # STEP 2: Create Loopback0 with IP
        # ============================================================
        print("[2] CREATE Loopback0 with IP 10.99.0.1/32...")
        output = conn.send_config_set(CONFIG_COMMANDS)
        print("✓ Loopback0 created\n")

        # ============================================================
        # STEP 3: DISABLE Interface (shutdown)
        # ============================================================
        print("[3] DISABLE Interface (shutdown)...")
        output = conn.send_config_set(DISABLE_COMMANDS)
        print("✓ Loopback0 DISABLED (administratief uit)\n")

        # Verify disabled state
        print("[3b] Verifying disabled state...")
        verify = conn.send_command('show interface loopback 0')
        if 'disabled' in verify.lower() or 'administratively down' in verify.lower():
            print("✓ Confirmed: Interface is DOWN\n")
        else:
            print("⚠ Check output below:\n")
            print(verify)
            print()

        # ============================================================
        # STEP 4: ENABLE Interface (no shutdown)
        # ============================================================
        print("[4] ENABLE Interface (no shutdown)...")
        output = conn.send_config_set(ENABLE_COMMANDS)
        print("✓ Loopback0 ENABLED (administratief aan)\n")

        # Verify enabled state
        print("[4b] Verifying enabled state...")
        verify = conn.send_command('show interface loopback 0')
        if 'up' in verify.lower():
            print("✓ Confirmed: Interface is UP\n")
        else:
            print("⚠ Check output below:\n")
            print(verify)
            print()

        # ============================================================
        # FINAL SUMMARY
        # ============================================================
        print("=" * 70)
        print("TASK 2 SUCCESSFUL ✓")
        print("=" * 70)
        print("✓ Loopback0 created with IP 10.99.0.1/32")
        print("✓ Interface DISABLED (shutdown)")
        print("✓ Interface ENABLED (no shutdown)")
        print("=" * 70 + "\n")

        conn.disconnect()

    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()