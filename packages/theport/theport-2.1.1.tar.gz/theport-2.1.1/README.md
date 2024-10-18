# ThePort 2.1.1

ThePort is a Python library for scanning ports and identifying running services on a specified IP address. It allows users to find open ports and check their statuses.

- By using this tool you can scan ports very deep and list ports
  
## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Port Scanning](#basic-port-scanning)
  - [Scanning with User-Defined Ports](#scanning-with-user-defined-ports)
  - [Scanning All Ports](#scanning-all-ports)
  - [Asynchronous Scanning](#asynchronous-scanning)
- [Available Ports](#available-ports)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Installation

To install ThePort, you can use pip:

```bash
pip install theport
```

## Usage

### Basic Port Scanning

To scan ports on a specific IP address and print the status of each port:

```bash
from theport import scan_ports

# Example IP address to scan
ip_address = '199.36.158.100'

# Custom list of ports to scan
custom_ports = [22, 80, 443, 3306, 8080]

# Start scanning
open_ports, closed_ports = scan_ports(ip_address, custom_ports)

# Print results
for port, service in open_ports:
    print(f"Port {port} is open: {service}")

for port in closed_ports:
    print(f"Port {port} is closed")
```

### Scanning with User-Defined Ports

You can specify your own list of ports to scan as follows:

```bash
from theport import scan_ports

# Example IP address to scan
ip_address = '199.36.158.100'

# Custom list of ports to scan
custom_ports = [21, 25, 80, 443]

# Start scanning
open_ports, closed_ports = scan_ports(ip_address, custom_ports)

# Print results
for port, service in open_ports:
    print(f"Port {port} is open: {service}")

for port in closed_ports:
    print(f"Port {port} is closed")
```

### Scanning All Ports

To scan all ports in the full range (1-65535):

```bash
from theport import scan_ports

# Example IP address to scan
ip_address = '199.36.158.100'

# Start scanning all ports
open_ports, closed_ports = scan_ports(ip_address)

# Print results
for port, service in open_ports:
    print(f"Port {port} is open: {service}")

for port in closed_ports:
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

## Acknowledgments

Thank you for using ThePort! We appreciate your interest and support. If you find any issues or have suggestions, please let us know.
