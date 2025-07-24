from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader


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

env = Environment(loader=FileSystemLoader("templates"))

def render_template(template_name, variables):
    template = env.get_template(template_name)
    return template.render(variables).splitlines()

def config_vlan_S1():
    net_connect = ConnectHandler(**devices["S1"])
    config = render_template("vlan_config.j2", {"vlan_id": 101, "ports": "g0/1 - 2"})
    output = net_connect.send_config_set(config)
    print(f"S1 VLAN config output:\n{output}")
    net_connect.disconnect()

def config_ospf(device, loopback_ip, default_originate=False):
    net_connect = ConnectHandler(**devices[device])
    config = render_template("ospf_config.j2", {
        "network": "172.31.247.0 0.0.0.255",
        "loopback_ip": loopback_ip,
        "default_originate": default_originate
    })
    output = net_connect.send_config_set(config)
    print(f"{device} OSPF config output:\n{output}")
    net_connect.disconnect()

def config_acl(device):
    net_connect = ConnectHandler(**devices[device])
    config = render_template("acl_config.j2", {
        "allowed_networks": ["10.30.6.0 0.0.0.255", "192.168.1.0 0.0.0.255"],
        "interface": "g0/2"
    })
    output = net_connect.send_config_set(config)
    print(f"{device} ACL config output:\n{output}")
    net_connect.disconnect()

def config_pat():
    net_connect = ConnectHandler(**devices["R2"])
    config = render_template("pat_config.j2", {
        "inside_network": "172.31.247.0 0.0.0.255",
        "inside_interfaces": ["g0/1", "g0/2"],
        "outside_interface": "g0/3"
    })
    output = net_connect.send_config_set(config)
    print(f"PAT config output:\n{output}")
    net_connect.disconnect()

if __name__ == "__main__":
    config_vlan_S1()
    config_ospf("R1", "1.1.1.1")
    config_ospf("R2", "2.2.2.2", default_originate=True)
    config_acl("S1")
    config_acl("R1")
    config_acl("R2")
    config_pat()
