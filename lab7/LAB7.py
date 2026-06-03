## Device			device_type
#CSR1000v (jij)		cisco_xe ✅
#Classic IOS router 	cisco_ios
#Nexus switch		cisco_nxos
#ASA firewall		cisco_asa
#IOS XR				cisco_xr


##########################################
# Send show commands to a single device  #
##########################################

from netmiko import ConnectHandler

router = {
    "device_type": "cisco_xe",
    "host": "192.168.19.139",
    "username": "cisco",
    "password": "cisco123!",
    "port": 22
}

net_connect = ConnectHandler(**router)

commands = [
    "show ip interface brief",
    "show version"
]

for cmd in commands:
    print(f"\n=== {cmd.upper()} ===")
    output = net_connect.send_command(cmd)
    print(output)
	
	
##################################################
# Send configuration commands to a single device #
##################################################

from netmiko import ConnectHandler

router = {
    "device_type": "cisco_xe",
    "host": "192.168.19.139",
    "username": "cisco",
    "password": "cisco123!",
    "port": 22
}

net_connect = ConnectHandler(**router)

commands = [
    "show ip interface brief",
    "show version"
]

for cmd in commands:
    print(f"\n=== {cmd.upper()} ===")
    output = net_connect.send_command(cmd)
    print(output)
	
	
##########################################
# Run show commands and save the output  #
##########################################

from netmiko import ConnectHandler

router = {
    "device_type": "cisco_xe",
    "host": "192.168.19.139",
    "username": "cisco",
    "password": "cisco123!",
    "port": 22
}

net_connect = ConnectHandler(**router)

commands = [
    "show ip interface brief",
    "show version"
]

with open("router_output.txt", "w") as f:
    for cmd in commands:
        f.write(f"\n=== {cmd} ===\n")
        output = net_connect.send_command(cmd)
        f.write(output + "\n")

net_connect.disconnect()

print("✅ Output saved to router_output.txt")


######################################################
## Send device configuration using an external file  #
######################################################

from netmiko import ConnectHandler

router = {
    "device_type": "cisco_xe",
    "host": "192.168.19.139",
    "username": "cisco",
    "password": "cisco123!",
    "port": 22
}

net_connect = ConnectHandler(**router)

# Lees config file
with open("config.txt") as f:
    config_commands = f.read().splitlines()

# Stuur config
output = net_connect.send_config_set(config_commands)
print(output)

# Save config
net_connect.save_config()

net_connect.disconnect()


##########################################
##   Configure a subset of interfaces    #
##########################################

from netmiko import ConnectHandler

router = {
    "device_type": "cisco_xe",
    "host": "192.168.19.139",
    "username": "cisco",
    "password": "cisco123!",
    "port": 22
}

net_connect = ConnectHandler(**router)

interfaces = [
    "GigabitEthernet1",
    "GigabitEthernet2"
]

for intf in interfaces:
    commands = [
        f"interface {intf}",
        "description CONFIGURED_BY_SCRIPT",
        "no shutdown"
    ]
    print(net_connect.send_config_set(commands))

net_connect.disconnect()


##########################################
#   Connect using a Python Dictionary    #
##########################################

from netmiko import ConnectHandler

router = {
    "device_type": "cisco_xe",
    "host": "192.168.19.139",
    "username": "cisco",
    "password": "cisco123!",
    "port": 22
}

net_connect = ConnectHandler(**router)

output = net_connect.send_command("show ip interface brief")
print(output)

net_connect.disconnect()


##########################################
#    Meerdere devices (next step)        #
##########################################

devices = [
    {
        "device_type": "cisco_xe",
        "host": "192.168.19.139",
        "username": "cisco",
        "password": "cisco123!",
        "port": 22
    },
    {
        "device_type": "cisco_xe",
        "host": "192.168.19.139",
        "username": "cisco",
        "password": "cisco123!",
    }
]

for device in devices:
    net_connect = ConnectHandler(**device)
    print(f"\nConnected to {device['host']}")
    print(net_connect.send_command("show version"))
    net_connect.disconnect()


##########################################
#  Meerdere devices, meerdere commands   #
##########################################

from netmiko import ConnectHandler

devices = [
    {
        "device_type": "cisco_xe",
        "host": "192.168.19.139",
        "username": "cisco",
        "password": "cisco123!",
    },
    {
        "device_type": "cisco_xe",
        "host": "192.168.19.139",
        "username": "cisco",
        "password": "cisco123!",
    }
]

commands = [
    "show ip interface brief",
    "show version",
    "show running-config | section interface"
]

for device in devices:
    net_connect = ConnectHandler(**device)

    print(f"\n========== {device['host']} ==========")

    for cmd in commands:
        print(f"\n--- {cmd} ---")
        output = net_connect.send_command(cmd)
        print(output)

    net_connect.disconnect()
