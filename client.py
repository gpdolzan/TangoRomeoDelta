from socket_protocol import *

def main():
    # number of players
    player_count = 0
    # Baton starts as 0
    baton = 0
    # Card Dealer starts as 0
    card_dealer = 0
    host, port = get_host_and_port()
    # Target host and port
    tHost = host
    tPort = port
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
    print("tHost: " + tHost + " tPort: " + tPort)
    # While True
    while True:
        # If baton is 1, send message
        if baton == 1:
            # Get message
            msg = input("Voce possui o bastao, envie a mensagem: ")
            packet_msg = "#" + "_" + host + "_" + msg +"_" + str(1) + "_" + "@"
            # Send message
            s.sendto(packet_msg.encode('ascii'), (tHost, int(tPort)))
            # Receive message
            data, addr = s.recvfrom(1024)
            received_msg = data.decode('ascii')
            # Get host message and number in message splitting _
            msg_arr = received_msg.split("_")
            if msg_arr[0] == "#":
                if msg_arr[3] == str(len(tr)):
                    print("Deu a volta!")
            # print message
            print(msg_arr)
        else:
            # Receive message
            data, addr = s.recvfrom(1024)
            received_msg = data.decode('ascii')
            # Get host message and number in message splitting _
            msg_arr = received_msg.split("_")
            # If host is the Original sender
            if msg_arr[0] == "#":
                print(msg_arr)
                msg_arr[3] = str(int(msg_arr[3]) + 1)
                # Make message array intoa again
                msg_arr = "_".join(msg_arr)
                packet_msg = msg_arr
                # Send message
                s.sendto(packet_msg.encode('ascii'), (tHost, int(tPort)))

main()