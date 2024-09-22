import subprocess
import platform
import os

def check_nmap_installed():
    try:
        subprocess.check_call(['nmap', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    
def check_brew_installed():
    try:
        subprocess.check_call(['brew', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    
def install_brew():
    try:
        subprocess.check_call(['/bin/bash', '-c', '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'])
        print("Homebrew installed successfully")
    except subprocess.CalledProcessError:
        print("Failed to install Homebrew")

def install_nmap():
    os_name = platform.system()
    
    if os_name == 'Darwin': 
        if not check_brew_installed():
            install_brew()
        try:
            subprocess.check_call(['brew', 'install', 'nmap'])
            print("nmap installed successfully on macOS")
        except subprocess.CalledProcessError:
            print("Failed to install nmap on macOS")
    
    elif os_name == 'Linux':
        package_manager = None
        
        if subprocess.call(['which', 'apt'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            package_manager = 'apt'
        elif subprocess.call(['which', 'yum'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            package_manager = 'yum'
        elif subprocess.call(['which', 'dnf'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            package_manager = 'dnf'
        elif subprocess.call(['which', 'pacman'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            package_manager = 'pacman'
        elif subprocess.call(['which', 'apk'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            package_manager = 'apk'
        
        else:
            print("No supported package manager found.")
            return
        
        try:
            if package_manager == 'apt':
                subprocess.check_call(['sudo', 'apt-get', 'update'])
                subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'nmap'])
            elif package_manager == 'yum':
                subprocess.check_call(['sudo', 'yum', 'install', '-y', 'nmap'])
            elif package_manager == 'dnf':
                subprocess.check_call(['sudo', 'dnf', 'install', '-y', 'nmap'])
            elif package_manager == 'pacman':
                subprocess.check_call(['sudo', 'pacman', '-Syu', '--noconfirm', 'nmap'])
            elif package_manager == 'apk':
                subprocess.check_call(['apk', 'update'])
                subprocess.check_call(['apk', 'add', 'nmap'])
                
            print(f"nmap installed successfully using {package_manager}")
        
        except subprocess.CalledProcessError:
            print(f"Failed to install nmap using {package_manager}")
    
    else:
        print(f"Unsupported operating system: {os_name}")

def check_nmap():
    if not check_nmap_installed():
        try:
            install_nmap()
            print("nmap installed successfully")
        except Exception as e:
            print(f"Failed to install nmap: {str(e)}")
            return False
    else:
        return True
    return False

if __name__ == "__main__":
    if check_nmap():
        print("nmap is ready")
