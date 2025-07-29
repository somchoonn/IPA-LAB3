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
    },
}

def config_vlan_S1():
    net_connect = ConnectHandler(**devices["S1"])
    commands = [
        "vlan 101",
        "interface range g0/1 - 2",
        "switchport mode access",
        "switchport access vlan 101"
    ]
    output = net_connect.send_config_set(commands)
    print(f"S1 VLAN config output:\n{output}")
    net_connect.disconnect()

def config_ospf_R1():
    net_connect = ConnectHandler(**devices["R1"])
    commands = [
        "router ospf 1 vrf control-data",
        "network 172.31.247.0 0.0.0.255 area 0",
        "int loopback 0",
        "ip address 1.1.1.1 255.255.255.255"
    ]
    output = net_connect.send_config_set(commands)
    print(f"R1 OSPF config output:\n{output}")
    net_connect.disconnect()

def config_ospf_R2():
    net_connect = ConnectHandler(**devices["R2"])
    commands = [
        "router ospf 1 vrf control-data",
        "network 172.31.247.0 0.0.0.255 area 0",
        "default-information originate",
        "int loopback 0",
        "ip address 2.2.2.2 255.255.255.255"
    ]
    output = net_connect.send_config_set(commands)
    print(f"R2 OSPF config output:\n{output}")
    net_connect.disconnect()

def config_acl(device): #R1 R2 S1
    net_connect = ConnectHandler(**devices[device])
    commands = [
    "ip access-list extended ACL-TEST2",
    "permit tcp 10.30.6.0 0.0.0.255 any eq 22",
    "permit tcp 10.30.6.0 0.0.0.255 any eq 23",
    "permit tcp 192.168.1.0 0.0.0.255 any eq 22",
    "permit tcp 192.168.1.0 0.0.0.255 any eq 23",
    "deny tcp any any eq 22",
    "deny tcp any any eq 23",
    "permit ip any any",
    "interface g0/2",
    "ip access-group ACL-TEST2 in",
    ]
    output = net_connect.send_config_set(commands)
    print(f"ACL config output:\n{output}")
    net_connect.disconnect()

def config_pat():
    net_connect = ConnectHandler(**devices["R2"])

    commands = [
        "access-list 2 permit 172.31.247.0 0.0.0.255",
        "ip nat inside source list 2 interface g0/3 vrf control-data overload",
        "interface g0/1",
        "ip nat inside",
        "interface g0/2",   
        "ip nat inside",
        "interface g0/3",
        "ip nat outside"
    ]

    output = net_connect.send_config_set(commands)
    print(f"PAT config output:\n{output}")

    net_connect.disconnect()

if __name__ == "__main__":
    config_vlan_S1()
    config_ospf_R1()
    config_ospf_R2()
    config_acl("S1")
    config_acl("R1")
    config_acl("R2")
    config_pat()
