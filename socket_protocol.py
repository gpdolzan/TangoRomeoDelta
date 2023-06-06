import socket
import random

# Create a UDP socket DATAGRAM
def get_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_hostname():
    return socket.gethostname()

# Get local machine name and get random port number
def get_host_and_port():
    host = get_hostname()
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
        exit()
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

# Prepare token ring
def prepare_tokenring(filename, host, port):
    # Read config.delta
    tokenring = read_config_file(filename)
    # tokenring can't have more than 8 hosts
    add_host_and_port(host, port, tokenring)
    # Write host and port to config.delta
    write_config_file(filename, tokenring)
    return tokenring

# Update tokenring for current host
def update_tokenring(filename):
    # Read config.delta
    tokenring = read_config_file(filename)
    return tokenring

# Check if host is the first in tokenring
def is_first_in_tr(host, tokenring):
    # Check if host is the first in tokenring
    if host == list(tokenring.keys())[0]:
        return True
    return False

def create_message(message, host, confirmation):
    # Create message
    message = "#" + "_" + host + "_" + message + "_" + str(confirmation) + "_" + "@"
    return message

def read_message(message):
    # Split message by _
    message_arr = message.split("_")
    print(message_arr)
    # Get message and split with :
    command = message_arr[2].split(":")
    # If host is the same as target host
    if(command[0] == get_hostname()):
        return True, command, message_arr
    return False, command, message_arr

def send_update_to_hosts(filename, socket, cHost, cPort):
    # Read config.delta
    tokenring = read_config_file(filename)
    # for each host in tokenring
    for host, port in tokenring.items():
        # except current host and port
        if host != cHost and port != cPort:
            # Send update to host
            socket.sendto(create_message("updatetr", cHost, 0).encode(), (host, int(port)))

def get_next_host_and_port(host, tr):
    # Get index of host in tokenring
    index = list(tr.keys()).index(host)
    # Check if host is the last in tokenring
    if index == len(tr) - 1:
        # Return first host and port
        return list(tr.keys())[0], list(tr.values())[0]
    # Return next host and port
    return list(tr.keys())[index + 1], list(tr.values())[index + 1]

def initiate_tokenring():
    host, port = get_host_and_port()
    # Prepare tokenring
    tr = prepare_tokenring("config.delta", host, port)
    # Get socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind address to socket
    s.bind((host, port))
    # Wait for tokenring to be ready
    if is_first_in_tr(host, tr):
        baton = 1
        card_dealer = 1
        while True:
            start = input("Digite sim, quando todos estiverem conectados: ")
            if start == "sim":
                send_update_to_hosts("config.delta", s, host, port)
                tr = update_tokenring("config.delta")
                break
    else:
        while True:
            data, addr = s.recvfrom(1024)
            received_msg = data.decode('ascii')
            msg_arr = received_msg.split("_")
            if msg_arr[0] == "#":
                if msg_arr[2] == "updatetr":
                    tr = update_tokenring("config.delta")
                    break
    # Adjust tHost and tPort
    tHost, tPort = get_next_host_and_port(host, tr)
    return tHost, tPort, s, tr, baton, card_dealer

def get_host_list(tokenring):
    host_list = []
    for host in tokenring.keys():
        host_list.append(host)
    return host_list
    

# Message protocol: MI / Origin / Message / Confirmation / ME
# MI: Message Init
# Origin: Hostname
# Message: Message
# Confirmation: 1 ~ total number of players
# ME: Message End
# Example: "[#][hostname][Message][1 to number of hosts in tokenring][@]"
# Taxation: "[#][hostname][receive:12:10:1]"