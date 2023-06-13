import socket
import random
from game_logic import *
from game_logic import player_cards
from game_logic import ultima_jogada, player_cards

# Create a UDP socket DATAGRAM
def get_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_hostname():
    return socket.gethostname()

# Get local machine name and get random port number
def get_host():
    host = get_hostname()
    # Return host and port as dict key and value
    return host

# Check if a file exists
def file_exists(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except FileNotFoundError:
        print("File does not exist, aborting")
        exit(1)

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
    file_exists(filename)
    f = open(filename, "r")
    # Read all lines and create dict with key and value
    file_dict = {}
    for line in f:
        line = line.strip()
        if line != "":
            host, port, rank = line.split(" ")
            file_dict[host] = (port, rank)
    f.close()
    return file_dict

# Prepare token ring
def get_tokenring(filename):
    # Read config.delta
    tokenring = read_config_file(filename)
    return tokenring

def create_message(message, host, confirmation):
    # Create message
    message = "#" + "_" + host + "_" + message + "_" + str(confirmation) + "_" + "@"
    return message

def read_message(message):
    # Split message by _
    message_arr = message.split("_")
    # Get message and split with :
    command = message_arr[2].split(":")

    # If host is the same as target host
    if(command[0] == get_hostname()):
        # HERE
        #if(command[1] == "pass"):
            #set_pass_count(get_pass_count() + 1)
        return True, command, message_arr
    elif(command[0] == "endreceive"):
        return True, command, message_arr
    elif(command[0] == "discarded"):
        return True, command, message_arr
    return False, command, message_arr

def get_port_and_rank(host, tr):
    # Get index of host in tokenring
    index = list(tr.keys()).index(host)
    # Using index get port and rank
    return list(tr.values())[index]

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
    baton = 0
    card_dealer = 0
    host = get_host()
    # Prepare tokenring
    tr = get_tokenring("config.file")
    # Prepare tokenring connections
    port, rank = get_port_and_rank(host, tr)
    tHost, tInfo = get_next_host_and_port(host, tr)
    tPort = tInfo[0]
    tRank = tInfo[1]

    # if rank == gd
    if rank == "gd":
        baton = 1
        card_dealer = 1

    # Get socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind address to socket
    s.bind((host, int(tr[host][0])))
    
    # Adjust tHost and tPort
    return tHost, tPort, tRank, host, port, rank, s, tr, baton, card_dealer

def get_host_list(tokenring):
    host_list = []
    # Get host from tokenring
    for host in tokenring:
        host_list.append(host)
    return host_list
    
def read_command(command):
    if command[0] == "endreceive":
        return "break"
    elif command[0] == "discarded":
        # Clear ultima_jogada
        ultima_jogada.clear()
        # Fill discarded_cards with cards from command
        num = len(command)
        # Do a loop that gets number from command and append card to discarded_cards from cards
        for i in range(1, num):
            # Append card to ultima_jogada
            ultima_jogada.append(int(command[i]))
        return "discarded"
    elif command[1] == "receive":
        # Fill player_cards with cards from command
        num = len(command)
        # Do a loop that gets number from command and append card to player_cards from cards
        for i in range(2, num):
            # Append card to player_cards
            player_cards.append(int(command[i]))
        return "receive"
    elif command[1] == "pass":
        # I have the baton now
        return "pass"
    
def send_cards(tHost, tPort, host, s, tr, card_dealer, host_list):
    if card_dealer == 1:
        resp = "nao"
        while resp != "sim":
            resp = input("Digite sim para iniciar:")
        # tamanho do tokenring
        num_players = len(tr)
        # embaralha o array
        deck = generate_deck()
        # distribui as cartas
        player_hands = deal_cards(num_players, deck)

        # Percorre host_list
        for h in host_list:
            msg = h
            msg += ":receive"
            # pop first player_hand
            hand = player_hands.pop(0)
            for card in hand:
                # Append number
                msg += ":" + str(card[1])
            # Send message
            s.sendto(create_message(msg, host, 1).encode('ascii'), (tHost, int(tPort)))

            # Listen to message
            data, addr = s.recvfrom(1024)
            received_msg = data.decode('ascii')
            exec, command, msg_arr = read_message(received_msg)
            if(int(msg_arr[3]) != len(tr)):
                print("Anel esta configurado errado!")
                exit(1)
            if(exec == True):
                cmd = read_command(command)

        msg = "endreceive"
        packed = create_message(msg, host, 1).encode('ascii')
        s.sendto(packed, (tHost, int(tPort)))
        # Listen to message
        data, addr = s.recvfrom(1024)
        received_msg = data.decode('ascii')
        exec, command, msg_arr = read_message(received_msg)

        if(int(msg_arr[3]) != len(tr)):
            print("Anel esta configurado errado!")
            exit(1)
            
        if(exec == True):
            cmd = read_command(command)
    else: # Se nao for card dealer
        while True:
            # Receive message
            data, addr = s.recvfrom(1024)
            msg = data.decode('ascii')
            exec, command, msg_arr = read_message(msg)
            if(exec == True):
                cmd = read_command(command)
                # envia mensagem
                new_msg = create_message(msg_arr[2], msg_arr[1], int(msg_arr[3]) + 1)
                s.sendto(new_msg.encode('ascii'), (tHost, int(tPort)))
                if(cmd == "break"):
                    break
            else:
                new_msg = create_message(msg_arr[2], msg_arr[1], int(msg_arr[3]) + 1)
                # envia mensagem
                s.sendto(new_msg.encode('ascii'), (tHost, int(tPort)))

def receive_message(s):
    data, addr = s.recvfrom(1024)
    received_msg = data.decode('ascii')
    exec, command, msg_arr = read_message(received_msg)
    return exec,command,msg_arr

def baton_process_msg(tr, exec, command, msg_arr, baton):
    if(int(msg_arr[3]) != len(tr)):
        print("Anel esta configurado errado!")
        exit(1)
    else:
        if command[1] == "pass":
            baton = 0
    if(exec == True):
        cmd = read_command(command)
    return baton

def prepare_discard(host, played):
    msg = "discarded"
    for card in played:
        msg += ":" + str(card)
                # Send message
    msg = create_message(msg, host, 1)
    return msg

def prepare_pass(tHost, host):
    msg = str(tHost) + ":pass"
                # Send message
    msg = create_message(msg, host, 1)
    return msg

def passagem_bastao(tHost, tPort, host, s, tr, baton):
    msg = prepare_pass(tHost, host)
    s.sendto(msg.encode('ascii'), (tHost, int(tPort)))
    exec, command, msg_arr = receive_message(s)
    baton = baton_process_msg(tr, exec, command, msg_arr, baton)

def descartar(tHost, tPort, host, s, tr, baton, played):
    msg = prepare_discard(host, played)
    s.sendto(msg.encode('ascii'), (tHost, int(tPort)))
    exec, command, msg_arr = receive_message(s)
    baton = baton_process_msg(tr, exec, command, msg_arr, baton)
    msg = prepare_pass(tHost, host)
    s.sendto(msg.encode('ascii'), (tHost, int(tPort)))
    exec, command, msg_arr = receive_message(s)
    baton = baton_process_msg(tr, exec, command, msg_arr, baton)
    return baton

# Message protocol: MI / Origin / Message / Confirmation / ME
# MI: Message Init
# Origin: Hostname
# Message: Message
# Confirmation: 1 ~ total number of players
# ME: Message End
# Example: "[#][hostname][Message][1 to number of hosts in tokenring][@]"
# Taxation: "[#][hostname][receive:12:10:1]"