# $$ set up customized log file
# local0.*    /var/log/pssid-daemon.log
# if $programname == 'pssid-daemon' then /var/log/pssid-daemon.log
# & stop

# systemctl restart rsyslog

# $$ output
# root@198:/var/log# cat pssid-daemon.log
# Jun  5 05:42:56 198 pssid-daemon.py[10069]: Hostname: 198.111.226.179, IP address: 198.111.226.179

# dependencies
import socket
import netifaces as ni
import syslog

# functions
def get_hostname_ip():
    try:
        hostname = socket.gethostname()
        hostIP = socket.gethostbyname(hostname)
        return hostname, hostIP
        print("hostname: ", hostname)
        print("IP addr: ", hostIP)
    except:
        print("Failed to obtain hostname and IP address")

def get_ethernet_ip(interface_name='eth0'):
    try:
        # Retrieve all addresses for the specified interface
        addr_info_list = ni.ifaddresses(interface_name)
        
        # Check for IPv4 addresses, which are under the AF_INET key
        if ni.AF_INET in addr_info_list:
            # Extract the first IPv4 address
            ipv4_info = addr_info_list[ni.AF_INET][0]
            ip = ipv4_info.get('addr')
            if ip:
                print(f"Interface: {interface_name}, IP: {ip}")
            else:
                print(f"No IP address assigned to {interface_name}.")
        else:
            print(f"No IPv4 address assigned to {interface_name}.")

    except ValueError:
        print(f"Interface {interface_name} not found.")
    except KeyError:
        print(f"Interface {interface_name} does not have an IPv4 address assigned.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def list_interfaces_with_ips():
    # Retrieve all addresses for each network interface
    interfaces = ni.interfaces()

    for interface in interfaces:
        # Get addresses by family
        addr_info_list = ni.ifaddresses(interface)
        
        # Check for IPv4 addresses, which are under the AF_INET key
        if ni.AF_INET in addr_info_list:
            # Extract IPv4 addresses
            for addr_info in addr_info_list[ni.AF_INET]:
                ip = addr_info.get('addr')
                if ip:
                    print(f"Interface: {interface}, IP: {ip}")
        else:
            print(f"Interface: {interface}, No IP assigned")


# Open the syslog connection
syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL0)

hostname, hostIP = get_hostname_ip()
print("===========")
get_ethernet_ip('eth0')
print("===========")
list_interfaces_with_ips()

# Log the information
# syslog.syslog(f"Hostname: {hostname}, IP address: {ip_address}, Interface: {interface_name}")
syslog.syslog(f"Hostname: {hostname}, IP address: {hostIP}")
#
# Close the syslog connection
syslog.closelog()

