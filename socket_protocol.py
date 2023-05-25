import socket
import random

# Create a UDP socket DATAGRAM
def get_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get local machine name and get random port number
def get_host_and_port():
    host = socket.gethostname()
    # Get random port number from 1024 to 65535
    port = random.randint(1024, 65535)
    # Return host and port as dict key and value
    return host, port

# Check if a file exists
def file_exists(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except FileNotFoundError:
        return False
    
# Create a file if it does not exist
def create_file(filename):
    if file_exists(filename) == False:
        f = open(filename, "w")
        f.close()

# Add host and port to tokenring
def add_host_and_port(host, port, dict):
    # dict can't have more than 8 hosts
    if len(dict) == 8:
        print("Tokenring is full")
        return
    dict[host] = port
    return dict

# Read config.delta
def read_config_file(filename):
    create_file(filename)
    f = open(filename, "r")
    # Read all lines and create dict with key and value
    file_dict = {}
    for line in f:
        line = line.strip()
        if line != "":
            key, value = line.split(" ")
            file_dict[key] = value
    f.close()
    return file_dict

# Write to config.delta
def write_config_file(filename, file_dict):
    create_file(filename)
    f = open(filename, "w")
    # Check if f has no content
    if f.tell() == 0:
        # Write key and value to f
        for key, value in file_dict.items():
            f.write(key + " " + str(value) + "\n")
        f.close()

# Message protocol: MI / Origin / Message / Confirmation / ME
# MI: Message Init
# Origin: Hostname
# Message: Message
# Confirmation: 0 or 1
# ME: Message End
# Example: "[#][hostname][Message][0 to number of hosts in tokenring][@]"

def main():
    # Baton starts as 0
    baton = 0
    # Get host and port
    tokenring = read_config_file("config.delta")
    # tokenring can't have more than 8 hosts
    host, port = get_host_and_port()
    add_host_and_port(host, port, tokenring)
    # Write host and port to config.delta
    write_config_file("config.delta", tokenring)
    # If host is the first host in tokenring he has the baton
    if host == list(tokenring.keys())[0]:
        baton = 1
    # Create socket
    s = get_socket()
    # Bind address to socket
    s.bind((host, port))
    # While True
    while True:
        # If baton is 1, send message
        if baton == 1:
            # Get message
            msg = input("Voce possui o bastao, envie a mensagem: ")
            packet_msg = "#" + "_" + host + "_" + msg +"_" + str(1) + "_" + "@"
            # Send message
            s.sendto(packet_msg.encode('ascii'), (host, port))
            # Receive message
            data, addr = s.recvfrom(1024)
            received_msg = data.decode('ascii')
            # Get host message and number in message splitting _
            msg_arr = received_msg.split("_")
            if(msg_arr[3] == str(len(tokenring))):
                print("Deu a volta!")
            # print message
            print(msg_arr)

main()