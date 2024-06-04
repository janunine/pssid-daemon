# dependencies
import socket
import netifaces as ni

# function to get hostname and ip address
def get_host_name_ip():
    try:
        hostname = socket.gethostname()
        hostIP = socket.gethostbyname(hostname)
        print("hostname: ", hostname)
        print("IP addr: ", hostIP)
    except:
        print("Failed to obtain hostname and IP address")





get_host_name_ip()

