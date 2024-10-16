import socket

def check_ports(host, ports):
    results = {}
    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=2) as sock:
                results[port] = "Open"
        except socket.error as e:
            if e.errno == 111:  # Connection refused
                results[port] = "Connection refused"
            else:
                results[port] = f"Error: {e}"
    return results
