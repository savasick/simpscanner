#!/usr/bin/env python
import subprocess
import re
import check_nmap
import socket
import time

def scan_for_ip(subnet):
    if subnet is None:
        subnet = get_subnet(get_internal_ip())
    command = f'nmap -sn -PS80 {subnet}'
    result = subprocess.check_output(command, shell=True)
    result = result.decode('utf-8')
    ip_addresses = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', result)

    return ip_addresses

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    return private_ip

def get_subnet(ip):
    subnet = ip.split('.')
    subnet[-1] = '0'
    return '.'.join(subnet) + '/24'

def scan_syn(subnet=None):
    if subnet is None:
        subnet = get_subnet(get_internal_ip())
    
    command = f'sudo nmap -sn -PS80 {subnet}'
    result = subprocess.check_output(command, shell=True).decode('utf-8')

    ip_addresses = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', result)
    mac_info = re.findall(r'MAC Address: ([\w:]+) \((.*?)\)', result)

    own_ip = get_internal_ip()

    mac_dict = {ip: (mac, vendor) for ip, (mac, vendor) in zip(ip_addresses, mac_info)}

    results = [
        (ip, *mac_dict[ip]) if ip in mac_dict else (ip, None, None)
        for ip in ip_addresses
        if ip != own_ip
    ]

    return results

def write_scan(result, known_devices):
    for ip, mac, name in result:
        if (ip, mac) not in known_devices:
            known_devices.add((ip, mac))
            with open('devices.txt', 'a') as f:
                if mac:
                    f.write(f"IP: {ip}, MAC: {mac} ({name})\n")
                else:
                    f.write(f"IP: {ip}, MAC: Not found\n")

def print_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except IOError:
        print(f"Error: Failed to read file '{file_path}'.")


def print_syn(result):
    for ip, mac, name in result:
        if mac:
            print(f"IP: {ip}, MAC: {mac} ({name})")
        else:
            print(f"IP: {ip}, MAC: Not found")

def load_known_devices(file_path):
    known_devices = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.search(r'IP: (\d+\.\d+\.\d+\.\d+), MAC: ([\w:]+)', line)
                if match:
                    ip, mac = match.groups()
                    known_devices.add((ip, mac))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except IOError:
        print(f"Error: Failed to read file '{file_path}'.")
    
    return known_devices

def compare_devices(scan_result, known_devices):
    scan_ips = {ip for ip, mac, name in scan_result}

    only_in_scan_syn = scan_ips - {ip for ip, mac in known_devices}

    only_in_file = {ip for ip, mac in known_devices} - scan_ips
    
    return only_in_scan_syn, only_in_file

def is_device_online(ip):
    packet = IP(dst=ip)/ICMP()
    response = sr1(packet, timeout=1, verbose=0)
    return response is not None

def main():
    known_devices_file = "devices.txt"
    known_devices = load_known_devices(known_devices_file)
    internal_ip = get_internal_ip()
    try:
        print(check_nmap.check_nmap())
        while True:
            print("To stop press CTRL+C")
            print("Your IP:", internal_ip)
            result = scan_syn()
            subprocess.run("clear")
            write_scan(result, known_devices)
            print_file_contents(known_devices_file)

    except KeyboardInterrupt:
        print("\nScript stopped by user.")

if __name__ == "__main__":
    main()
