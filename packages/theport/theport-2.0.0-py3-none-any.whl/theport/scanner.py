# scanner.py
import socket
import threading
import requests
from .services import identify_service

FULL_PORT_RANGE = range(1, 65536)

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def send_http_request(ip, port):
    url = f"http://{ip}:{port}"
    try:
        response = requests.get(url, timeout=2)
        return response.status_code, response.text[:100]
    except requests.exceptions.RequestException:
        return None, "No response"

def scan_ports(ip, port_list=None):
    if port_list is None:
        port_list = FULL_PORT_RANGE
    
    open_ports = []
    
    def scan_thread(ip, port):
        if scan_port(ip, port):
            service_info = identify_service(port)
            open_ports.append((port, service_info))

    threads = []
    for port in port_list:
        t = threading.Thread(target=scan_thread, args=(ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return open_ports

def check_port_status(ip, user_ports=None):
    open_ports = scan_ports(ip, user_ports)
    all_ports = {port: 'closed' for port in (user_ports if user_ports else FULL_PORT_RANGE)}
    
    for port, service in open_ports:
        all_ports[port] = f'open {service}'

    return all_ports
