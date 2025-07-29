from netmiko import ConnectHandler
devices = {
    "S1": {
        "device_type": "cisco_ios",
        "host": "172.31.247.3",
        "username": "admin",
        "use_keys": True,
        "key_file": "key.pem",
    },
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

def config_Description(device):
    net_connect = ConnectHandler(**devices[device])
    output = net_connect.send_command("show cdp neighbors", use_textfsm=True)
    for i in range(len(output)):
        print(output[i])
        routerName = output[i]['neighbor_name'].split('.')
        platform = output[i]['platform']
        interface = output[i]['neighbor_interface']
        final = f"Connect to {platform[0]}{interface} of {routerName[0]}"
        commands = (
            f"interface {output[i]['local_interface']}",
            f"description {final}"
        )
        net_connect.send_config_set(commands)
    net_connect.disconnect()

def config_Description_Man(device, interface, where):
    net_connect = ConnectHandler(**devices[device])
    commands = [
        f"interface {interface}",
        f"description Connect to {where}"
    ]
    net_connect.send_config_set(commands)
    net_connect.disconnect()

if __name__ == "__main__":
    config_Description("R1")
    config_Description_Man("R1", "g0/1", "PC")
    config_Description("R2")
    config_Description_Man("R2", "g0/3", "WAN")
    config_Description("S1")
    config_Description_Man("S1", "g0/2", "PC")