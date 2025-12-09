import socket
import threading
import ssl
import re
import time  # Importing time module for delay
from tabulate import tabulate  # Importing tabulate for neat table formatting

# Developer name banner
def print_banner():
    banner = """
 MMMMMMM   RRRRRR    FFFFFFF   AAAAA    RRRRRR    III    DDDDD
 MM    MM  RR   RR   FF        AA   AA   RR   RR   II     DD   DD
 MM    MM  RRRRRR    FFFFF     AAAAAAA   RRRRRR    II     DD   DD
 MM    MM  RR  RR    FF        AA   AA   RR  RR    II     DD   DD
 MMMMMMM   RR   RR   FF        AA   AA   RR   RR   III    DDDDD
    """
    print(banner)

# Predefined list of common ports to scan
COMMON_PORTS = [21, 22, 23, 25, 80, 443, 3306, 3389, 8080]

# Function to identify services and versions
def get_service_banner(target, port):
    try:
        # Create socket and connect to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5 second timeout
        sock.connect((target, port))

        # For HTTPS ports, use SSLContext (updated method)
        if port == 443:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=target)

        # Send request to get banner for HTTP/HTTPS
        if port == 80 or port == 443:
            sock.send(b'HEAD / HTTP/1.1\r\nHost: ' + target.encode() + b'\r\n\r\n')
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore')

        if banner:
            version = extract_version(banner)
            return banner.strip(), version
        sock.close()
    except socket.timeout:
        return "Timed out", None  # Timeout error
    except Exception as e:
        return "Error", None

# Function to extract service version from banner
def extract_version(banner):
    # Known versions of services in the banners
    versions = {
        'Apache': r'Apache\/([0-9]+\.[0-9]+\.[0-9]+)',
        'nginx': r'nginx\/([0-9]+\.[0-9]+\.[0-9]+)',
        'OpenSSH': r'OpenSSH_([0-9]+\.[0-9]+\.[0-9]+)',
        'vsftpd': r'vsftpd ([0-9]+\.[0-9]+\.[0-9]+)',
        'ProFTPD': r'ProFTPD (\d+\.\d+\.\d+)',
        'MySQL': r'MySQL (\d+\.\d+\.\d+)',
    }
    
    # Look for version in the banner
    for service, pattern in versions.items():
        match = re.search(pattern, banner)
        if match:
            return match.group(1)
    return None

# Function to identify the service
def identify_service(port):
    if port == 21:
        return "FTP"
    elif port == 22:
        return "SSH"
    elif port == 23:
        return "Telnet"
    elif port == 25:
        return "SMTP"
    elif port == 80:
        return "HTTP"
    elif port == 443:
        return "HTTPS"
    elif port == 3306:
        return "MySQL"
    elif port == 3389:
        return "RDP"
    elif port == 8080:
        return "HTTP Alt"
    else:
        return "Unknown Service"

# Function to identify the operating system
def identify_os(port):
    if port == 22:
        return "Likely Linux or Unix-based"
    elif port == 3389:
        return "Likely Windows"
    elif port == 80 or port == 443:
        return "Likely Web Server (Apache, Nginx, or IIS)"
    elif port == 21:
        return "Likely FTP Server (Linux/Unix or Windows)"
    else:
        return "Unknown OS"

# Function to scan individual port
def scan_port(target, port, open_ports, results):
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5 second timeout

        # Attempt to connect to the target on the specified port
        result = sock.connect_ex((target, port))

        if result == 0:
            service = identify_service(port)
            os_info = identify_os(port)
            banner, version = get_service_banner(target, port)

            # Only add to results if the port is open and the banner is valid
            if banner != "Error" and banner != "Timed out":
                results.append([port, service, os_info, banner, version if version else "Unknown"])
                open_ports.append(port)  # Add open port to the list
        sock.close()
    except socket.timeout:
        pass  # Ignore timeout errors for ports that don’t respond
    except socket.error as e:
        pass  # Skip other errors for closed ports

# Function to scan predefined set of common ports and show only open ports
def scan_ports(target):
    print(f"Scanning common ports on {target}...\n")
    
    open_ports = []  # List to store open ports
    results = []  # List to store details of open ports
    thread_list = []  # List to hold all threads

    # Create and start threads for scanning ports
    for port in COMMON_PORTS:
        t = threading.Thread(target=scan_port, args=(target, port, open_ports, results))
        thread_list.append(t)
        t.start()

    # Wait for the remaining threads to finish
    for t in thread_list:
        t.join()

    # Split the results into two tables: Service Version and Open Ports
    if results:
        headers1 = ["Port", "Service", "Operating System", "Banner", "Service Version"]
        headers2 = ["Open Ports"]
        
        # Creating two separate tables: One for Service Version, one for Open Ports
        service_version_table = [row[:4] + [row[4]] for row in results]  # Display only Service Version
        open_ports_table = [[row[0]] for row in results]  # Only show Open Ports
        
        print("\nService Version Table:")
        print(tabulate(service_version_table, headers=headers1, tablefmt="fancy_grid"))
        
        print("\nOpen Ports Table:")
        print(tabulate(open_ports_table, headers=headers2, tablefmt="fancy_grid"))
    else:
        print("\nNo open ports found.")
    print("\nPort scan finished!")

if __name__ == "__main__":
    # Print banner before the scan
    print_banner()

    # Input for target IP address
    target_ip = input("Enter target IP address: ")

    # Add a 5-second delay before starting the scan
    print("Waiting for 5 seconds before starting the scan...")
    time.sleep(5)  # Wait for 5 seconds

    # Run port scan on common ports
    scan_ports(target_ip)
