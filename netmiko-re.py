import re
from netmiko import ConnectHandler

devices = {
    "R1": {
        "device_type": "cisco_ios",
        "host": "172.31.247.4",
        "username": "admin",
        "use_keys": True,
        "key_file": "key.pem",
    },
    "R2": {
        "device_type": "cisco_ios",
        "host": "172.31.247.5",
        "username": "admin",
        "use_keys": True,
        "key_file": "key.pem",
    }
}

def get_router_uptime(device):
    try:
        conn = ConnectHandler(**device)
        output = conn.send_command("show version")
        conn.disconnect()

        match = re.search(r"(\S+) uptime is (.+)", output)
        if match:
            hostname = match.group(1)
            uptime = match.group(2)
            return (hostname, uptime)
        else:
            return (device["host"], "Uptime not found")
    except Exception as e:
        return (device["host"], f"Error: {e}")

def get_active_interfaces(device):
    try:
        conn = ConnectHandler(**device)
        output = conn.send_command("show interfaces")
        conn.disconnect()
        pattern = re.compile(
            r"^(?P<intf>\S+) is up, line protocol is up",
            re.MULTILINE
        )

        return [match.group("intf") for match in pattern.finditer(output)]

    except Exception as e:
        print(f"Failed to get interfaces from {device['host']}: {e}")
        return []

if __name__ == "__main__":
    for name, dev in devices.items():
        print(f"\n===== Device: {name} =====")

        hostname, uptime = get_router_uptime(dev)
        print(f"Router hostname: {hostname}")
        print(f"Router uptime  : {uptime}\n")

        active_intfs = get_active_interfaces(dev)
        if not active_intfs:
            print("No active interfaces found.")
        else:
            print(f"Active interfaces :")
            for intf in active_intfs:
                print(f"  - {intf}")
