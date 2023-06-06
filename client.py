from socket_protocol import *
from game_logic import *

player_cards = []

def read_command(command):
    if command[0] == "receive":
        # Read all cards and append as cards object in player_cards
        for i in range(1, len(command)):
            player_cards.append(cards[int(command[i]) - 1])

def main():
    tHost, tPort, s, tr, baton, card_dealer = initiate_tokenring()
    host_list = get_host_list(tr)

    if card_dealer == 1:
        # tamanho do tokenring
        num_players = len(tr)
        # embaralha o array
        deck = generate_deck()
        # distribui as cartas
        player_hands = deal_cards(num_players, deck)
        # Define GD
        gd_pos = random.randint(0, num_players - 1)
        while gd_pos <= num_players - 1:
            # First hand will be sent to GD
            gd_hand = player_hands[0]
            # Percorre gd_hand
            msg = host_list[gd_pos]
            msg += ":receive"
            for card in gd_hand:
                # Append number
                msg += ":" + str(card[1])
            # Remove first hand from player_hands
            player_hands.pop(0)
            # Send message
            s.sendto(create_message(msg, get_hostname(), 0).encode('ascii'), (tHost, int(tPort)))

            # Listen to message
            data, addr = s.recvfrom(1024)
            received_msg = data.decode('ascii')
            if(received_msg[1] == get_hostname()):
                print("Mensagem deu a volta!")
            gd_pos += 1
        else: # Se nao for card dealer
            # Receive message
            data, addr = s.recvfrom(1024)
            msg = data.decode('ascii')
            print(msg)
            exec, command, msg_arr = read_message(msg)
            if(exec == True):
                print("Lendo o comando!")
                read_command(command)
            new_msg = create_message(msg_arr[2], msg_arr[1], str(int(msg_arr[3] + 1)))
            # envia mensagem
            s.sendto(new_msg.encode('ascii'), (tHost, int(tPort)))
        
    print(player_cards)
    # While True
    #while True:
        # If baton is 1, send message
        #if baton == 1:
            # Get message
            #msg = input("Voce possui o bastao, envie a mensagem: ")
            #packet_msg = "#" + "_" + host + "_" + msg +"_" + str(1) + "_" + "@"
            # Send message
            #s.sendto(packet_msg.encode('ascii'), (tHost, int(tPort)))
            # Receive message
            #data, addr = s.recvfrom(1024)
            #received_msg = data.decode('ascii')
            # Get host message and number in message splitting _
            #msg_arr = received_msg.split("_")
            #if msg_arr[0] == "#":
                #if msg_arr[3] == str(len(tr)):
                    #print("Deu a volta!")
            # print message
            #print(msg_arr)
        #else:
            # Receive message
            #data, addr = s.recvfrom(1024)
            #received_msg = data.decode('ascii')
            # Get host message and number in message splitting _
            #msg_arr = received_msg.split("_")
            # If host is the Original sender
            #if msg_arr[0] == "#":
                #print(msg_arr)
                #msg_arr[3] = str(int(msg_arr[3]) + 1)
                # Make message array intoa again
                #msg_arr = "_".join(msg_arr)
                #packet_msg = msg_arr
                # Send message
                #s.sendto(packet_msg.encode('ascii'), (tHost, int(tPort)))

main()