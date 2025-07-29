import paramiko

username = 'admin'
key_path = "key.pem"

device_ip = [
    "172.31.247.1",  
    "172.31.247.2",  
    "172.31.247.5",  
    "172.31.247.3",  
    "172.31.247.4"   
]

key = paramiko.RSAKey.from_private_key_file(key_path)

for ip in device_ip:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(ip, username=username, pkey=key, look_for_keys=False)

        stdin, stdout, stderr = client.exec_command("show ip int brief")
        print(f"Output from {ip}:\n{stdout.read().decode()}")
        
    except Exception as e:
        print(f"Error with {ip}: {e}")
    finally:
        client.close()
