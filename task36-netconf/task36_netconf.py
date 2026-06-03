from ncclient import manager
import requests

router = {
    "host": "192.168.19.139",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!"
}

# GitHub raw config URL
github_url = "https://raw.githubusercontent.com/MilanCampsPXL/Cisco-Network-Automation-Project/refs/heads/main/Configs/Task_36/full_config.xml"

try:

    print("Configuratie ophalen van GitHub")

    response = requests.get(github_url)

    if response.status_code != 200:
        raise Exception("GitHub config niet gevonden")

    config = response.text

    print("Verbinden via NETCONF")

    with manager.connect(
        host=router["host"],
        port=830,
        username=router["username"],
        password=router["password"],
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False
    ) as m:

        print("Configuratie toepassen")

        try:

            netconf_reply = m.edit_config(
                target="running",
                config=config
            )

            print(netconf_reply)

            print("Deployment succesvol")

        except Exception as config_error:

            print("Configuratie fout")

            print(config_error)

            try:
                m.discard_changes()
                print("Wijzigingen discarded")
            except:
                print("Discard niet ondersteund")

except Exception as e:

    print(f"Failed {e}")
