import socket

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, port))
        return True
    except:
        return False
    finally:
        s.close()

ip = "10.11.0.2"
ports = [1433, 1434, 445, 135, 80, 443]

print(f"Scanning ports on {ip} from container...")
for port in ports:
    status = "OPEN" if check_port(ip, port) else "CLOSED/BLOCKED"
    print(f"Port {port}: {status}")
