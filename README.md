
# F-port_Scanner

**F-port_Sanner** is a powerful tool for scanning open and closed ports on a target domain or IP address. It provides detailed service information, operating system hints, and banner data, all displayed in a neat table format.

Supports **Linux**, **Windows**, and **MacOS**.

---

## Features

* Scan common ports for a target domain or IP.
* Detect open ports only, ignoring closed ones.
* Identify service type (HTTP, FTP, SSH, SMTP, etc.).
* Retrieve service banner information and service version if available.
* Identify likely operating system based on open ports.
* Multi-threaded scanning for faster results.
* User-friendly output displayed in tables using **tabulate**.
* 5-second delay before scanning for safe and controlled execution.
* Custom ASCII banner display on startup.

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/mrfarid780/F-port_Scanner.git
```

2. **Navigate into the folder**:

```bash
cd F-port_Scanner
```

3. **Install required dependencies** (if not already installed):

```bash
pip install tabulate
```

4. **Run the scanner**:

```bash
python3 F-port_Scanner.py
```

> **Note**: You need **Python 3** installed on your system.



## Usage

1. Start the program by running:

```bash
python3 F-port_Scanner.py
```

2. Enter the target **IP address or domain name** when prompted.

3. The scanner will wait **5 seconds** before starting the scan.

4. Once scanning is complete, the results will be displayed in two tables:

   * **Service Version Table** – Shows open ports, service type, operating system hints, banner, and service version.
   * **Open Ports Table** – Shows only the list of open ports.



## Example Output

```
 MMMMMMM   RRRRRR    FFFFFFF   AAAAA    RRRRRR    III    DDDDD
 MM    MM  RR   RR   FF        AA   AA   RR   RR   II     DD   DD
 MM    MM  RRRRRR    FFFFF     AAAAAAA   RRRRRR    II     DD   DD
 MM    MM  RR  RR    FF        AA   AA   RR  RR    II     DD   DD
 MMMMMMM   RR   RR   FF        AA   AA   RR   RR   III    DDDDD

Enter target IP address: 192.168.1.1
Waiting for 5 seconds before starting the scan...
Scanning common ports on 192.168.1.1...

Service Version Table:
+-------+---------+-------------------------------+--------------------------+-----------------+
| Port  | Service | Operating System               | Banner                   | Service Version |
+-------+---------+-------------------------------+--------------------------+-----------------+
| 80    | HTTP    | Likely Web Server (Apache...) | HTTP/1.1 200 OK          | Apache/2.4.41   |
| 443   | HTTPS   | Likely Web Server (Apache...) | HTTP/1.1 200 OK          | nginx/1.18      |
+-------+---------+-------------------------------+--------------------------+-----------------+

Open Ports Table:
+------------+
| Open Ports |
+------------+
| 80         |
| 443        |
+------------+


## Supported Platforms

* Linux
* Windows
* MacOS



## Requirements

* Python 3.x
* `tabulate` module (install using `pip install tabulate`)



## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.



## Author

**MRFARID**
GitHub: [https://github.com/mrfarid780](https://github.com/mrfarid780)

