# Simple scanner

This script scans the local network for devices using NMAP(install it if not installed), collects their IP and MAC addresses, and saves the information to a file while also displaying it in the terminal.
Detects devices on the local IPv4 network. Compatible with macOS and Linux. Asks password for admin for more accurate scanning.

### Install

```bash
git clone https://github.com/savasick/simpscanner.git
cd simpscanner
```


### run

```bash
python3 scan.py
```