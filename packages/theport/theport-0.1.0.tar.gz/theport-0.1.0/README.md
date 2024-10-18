# ThePort

ThePort is a Python library for scanning ports and identifying running services on a specified IP address. It allows users to find open ports and check for known vulnerabilities.

## Installation

To install ThePort, you can use pip:

```bash
pip install theport
```

## Usage

### Basic Port Scanning

To scan ports on a specific IP address, use the following example:

```python
import theport

# Example IP address to scan
ip_address = '192.168.1.1'
ports_to_scan = range(1, 1025)  # You can specify a custom range of ports

for port in ports_to_scan:
    service = theport.identify_service(port)
    is_open = theport.scan(ip_address, port)

    if is_open:
        print(f"Port {port} is open: {service}")
    else:
        print(f"Port {port} is closed")
```

### Scanning with User-Defined Ports

Users can also specify their own list of ports to scan:

```python
import theport

# Example IP address to scan
ip_address = '192.168.1.1'

# Custom list of ports to scan
custom_ports = [22, 80, 443, 3306, 8080]

for port in custom_ports:
    service = theport.identify_service(port)
    is_open = theport.scan(ip_address, port)

    if is_open:
        print(f"Port {port} is open: {service}")
    else:
        print(f"Port {port} is closed")
```

### Known Vulnerabilities Check

ThePort can also check for known vulnerabilities on specified ports. Below is an example of how to use this functionality:

```python
import theport

# Example IP address to scan
ip_address = '192.168.1.1'

# Custom list of ports to scan
custom_ports = [22, 80, 443]

for port in custom_ports:
    service = theport.identify_service(port)
    is_open = theport.scan(ip_address, port)
    
    if is_open:
        vulnerabilities = theport.check_vulnerability(port)
        print(f"Port {port} is open: {service}. Vulnerabilities: {vulnerabilities}")
    else:
        print(f"Port {port} is closed")
```

## Available Ports

ThePort supports a variety of commonly used ports, including but not limited to:

- **HTTP**: 80
- **HTTPS**: 443
- **FTP**: 21
- **SMTP**: 25, 587
- **MySQL**: 3306
- **SSH**: 22
- **Telnet**: 23
- **RDP**: 3389
- **PostgreSQL**: 5432
- **Redis**: 6379
- **MongoDB**: 27017

Feel free to extend the list as per your needs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you would like to contribute to ThePort, please open an issue or submit a pull request. Any help is greatly appreciated!
