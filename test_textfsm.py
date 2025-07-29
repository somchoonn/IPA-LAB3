import pytest
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

def connect_device(device):
    net_connect = ConnectHandler(**devices[device])
    output = net_connect.send_command("show interface description", use_textfsm=True)
    net_connect.disconnect()
    return output


        
def test_R1():
    output = connect_device("R1")
    for port in output:
        if port['port'] == "Gi0/0":
            assert port['description'] == "Connect to G0/1 of S0"
        elif port['port'] == "Gi0/2":
            assert port['description'] == "Connect to G0/1 of R2"
        elif port['port'] == "Gi0/1":
            assert port['description'] == "Connect to PC"

def test_R2():
    output = connect_device("R2")
    for port in output:
        if port['port'] == "Gi0/0":
            assert port['description'] == "Connect to G0/2 of S0"
        elif port['port'] == "Gi0/1":
            assert port['description'] == "Connect to G0/2 of R1"
        elif port['port'] == "Gi0/2":
            assert port['description'] == "Connect to G0/1 of S1"
        elif port['port'] == "Gi0/3":
            assert port['description'] == "Connect to WAN"
def test_S1():
    output = connect_device("S1")
    for port in output:
        if port['port'] == "Gi0/0":
            assert port['description'] == "Connect to G0/3 of S0"
        elif port['port'] == "Gi0/1":
            assert port['description'] == "Connect to G0/2 of R2"
        elif port['port'] == "Gi0/2":
            assert port['description'] == "Connect to PC"
