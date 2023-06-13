import random
import socket
import os

# GLOBAL VARIABLES
ja_comecou = 0
last_player = ""
round_counter = 0
bastao = False
carteador = False
fim = False
num_players = 0
pass_count = 0
finished_count = 0
finished_hand = False
finished_order = []
deck = []
hand = []
last_played = []
tokenring = {}
myInfo = ()
targetInfo = ()
s = None

# CONFIG FILE RELATED FUNCTIONS

# Check if a file exists
def file_exists(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except FileNotFoundError:
        print("File does not exist, aborting")
        exit(1)

# Read config file
def create_tokenring(filename):
    file_exists(filename)
    f = open(filename, "r")
    # Read all lines and create dict with key and value
    tokenring = {}
    for line in f:
        line = line.strip()
        if line != "":
            host, port, rank = line.split(" ")
            tokenring[host] = host, port, rank
    f.close()
    return tokenring

# Given a name return the from tokenring
def get_HPR(name):
    return tokenring[name]

# Given a name return the next in tokenring
def get_next_HPR(name):
    # Get the index of the name in the tokenring
    index = list(tokenring.keys()).index(name)
    # Get the next index
    index = (index + 1) % len(tokenring)
    # Get the next name
    next_name = list(tokenring.keys())[index]
    return tokenring[next_name]

def get_previous_HPR(name):
    # Get the index of the name in the tokenring
    index = list(tokenring.keys()).index(name)
    # Get the previous index
    index = (index - 1) % len(tokenring)
    # Get the previous name
    previous_name = list(tokenring.keys())[index]
    return tokenring[previous_name]

def get_hostnames():
    return list(tokenring.keys())

def get_greatdalmuti():
    return list(tokenring.keys())[0]

def get_next_host(hostname):
    index = list(tokenring.keys()).index(hostname)
    index = (index + 1) % len(tokenring)
    return list(tokenring.keys())[index]

def get_port_list():
    port_list = []
    for key in tokenring:
        port_list.append(tokenring[key][1])
    return port_list

def get_rank_list():
    rank_list = []
    for key in tokenring:
        rank_list.append(tokenring[key][2])
    return rank_list

# TOKENRING RELATED FUNCTIONS

# MENSAGENS
# MI / ORIGEM / JOGADA / CONFIRMATION / MF
# COMANDOS POSSIVEIS
# "IJ" == inicio de jogo --> SINALIZA INICIO DO JOGO
# EXEMPLO IJ
# MI / ORIGEM / IJ / CONFIRMATION / MF
# "EC" == enviar cartas --> RECEBE CARTAS PARA INICIO DO JOGO
# EXEMPLO EC
# MI / ORIGEM / EC:DESTINO:1,2,3,4,5,6,7,8,9,10,11,12,13 / CONFIRMATION / MF
# "DC" == descartar cartas --> CARTAS DESCARTADAS
# EXEMPLO DC
# MI / ORIGEM / DC:1,2,3,4,5,6,7,8,9,10,11,12,13 / CONFIRMATION / MF
# "PJ" == passar jogada --> PASSA A VEZ
# EXEMPLO PJ
# MI / ORIGEM / PJ:DESTINO / CONFIRMATION / MF
# "APC" == atualizar pass count --> ATUALIZA O PASS COUNT
# EXEMPLO APC
# MI / ORIGEM / APC:VALOR / CONFIRMATION / MF
# "NR" == new round --> INICIA NOVO ROUND
# EXEMPLO NR
# MI / ORIGEM / NR / CONFIRMATION / MF
# "AFC" == atualizar finished count --> ATUALIZA O FINISHED COUNT
# EXEMPLO AFC
# MI / ORIGEM / AFC:VALOR / CONFIRMATION / MF
# "FIM" == fim de jogo --> SINALIZA FIM DO JOGO
# EXEMPLO FIM
# MI / ORIGEM / FIM / CONFIRMATION / MF

# Create a UDP socket DATAGRAM
def get_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get local machine name
def get_hostname():
    return socket.gethostname()

# Function that creates a message
def create_message(origin, target, command, cards, confirmation):
    if command == "IJ":
        message = "#/" + origin + "/IJ/" + str(confirmation) + "/@"
    elif command == "EC":
        str_cards = ""
        for card in cards:
            str_cards += str(card) + ","
        str_cards = str_cards[:-1]
        message = "#/" + origin + "/EC:" + target + ":" + str_cards + "/" + str(confirmation) + "/@"
    elif command == "DC":
        str_cards = ""
        for card in cards:
            str_cards += str(card) + ","
        str_cards = str_cards[:-1]
        message = "#/" + origin + "/DC:" + str_cards + "/" + str(confirmation) + "/@"
    elif command == "PJ":
        message = "#/" + origin + "/PJ:" + target + "/" + str(confirmation) + "/@"
    elif command == "APC":
        message = "#/" + origin + "/APC:" + str(cards) + "/" + str(confirmation) + "/@"
    elif command == "NR":
        message = "#/" + origin + "/NR/" + str(confirmation) + "/@"
    elif command == "AFC":
        message = "#/" + origin + "/AFC:" + str(cards) + "/" + str(confirmation) + "/@"
    elif command == "FIM":
        message = "#/" + origin + "/FIM/" + str(confirmation) + "/@"
    return message

# Function that reads a message
def break_message(message):
    message = message.split("/")
    return message

# Function that checks confirmation
def check_confirmation(expected_confirmation, message):
    message = break_message(message)
    if int(message[3]) == int(expected_confirmation):
        return True
    else:
        return False

def break_command(command):
    # Break the command using split in both ":" and ","
    command = command.split(":")
    
    if command[0] == "IJ":
        return command # IJ
    elif command[0] == "PJ":
        return [command[0], command[1]] # PJ, DESTINO
    elif command[0] == "EC":
        return [command[0], command[1], command[2]] # EC, DESTINO, 1,2,3,4,5,6,7,8,9,10,11,12,13
    elif command[0] == "DC":
        return [command[0], command[1]] # DC, 1,2,3,4,5,6,7,8,9,10,11,12,13
    elif command[0] == "APC":
        return [command[0], command[1]] # APC, VALOR
    elif command[0] == "NR":
        return [command[0]] # NR
    elif command[0] == "AFC":
        return [command[0], command[1]] # AFC, VALOR
    elif command[0] == "FIM":
        return [command[0]] # FIM

def translate_message(message):
    # Break the message
    message = break_message(message)

    # Get origin
    origin = message[1]
    # Get the command
    command = message[2]
    # Get the confirmation
    confirmation = int(message[3])

    # Break the command
    command = break_command(command)
    
    # If the command is IJ
    if command[0] == "IJ":
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, "", "IJ", [], confirmation)
        # return command and message as list
        return [command, message]
    # If the command is EC
    elif command[0] == "EC":       
        # Get the cards
        cards = command[2].split(",")
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, command[1], "EC", cards, confirmation)
        # return command and message as list
        return [command, message]
    # If the command is DC
    elif command[0] == "DC":
        global last_player
        last_player = origin
        # Get the cards
        cards = command[1].split(",")
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, "", "DC", cards, confirmation)
        # return command, cards and message as list
        return [command, message]
    # If the command is PJ
    elif command[0] == "PJ":
        # Get the target
        target = command[1]
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, target, "PJ", [], confirmation)
        # return command, target and message as list
        return [command, message]
    # If the command is APC
    elif command[0] == "APC":
        global pass_count
        # Get the value
        value = command[1]
        pass_count = int(value)
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, "", "APC", value, confirmation)
        # return command, value and message as list
        return [command, message]
    # If the command is NR
    elif command[0] == "NR":
        global round_counter
        global last_played
        round_counter = round_counter + 1
        pass_count = 0
        last_played = []
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, "", "NR", [], confirmation)
        # return command and message as list
        return [command, message]
    # If the command is AFC
    elif command[0] == "AFC":
        global finished_count
        global finished_order
        # Get the value
        value = command[1]
        finished_count = int(value)
        # Append origin to finished order
        # Check if origin is already in finished order
        if origin not in finished_order:
            finished_order.append(origin)
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, "", "AFC", value, confirmation)
        # return command, value and message as list
        return [command, message]
    # If the command is FIM
    elif command[0] == "FIM":
        # Adjust confirmation and create message
        confirmation = confirmation + 1
        message = create_message(origin, "", "FIM", [], confirmation)
        # return command and message as list
        return [command, message]

# Execute command
def execute_command(command):
    # If the command is IJ
    if command[0] == "IJ":
        # Return the command
        return command[0]
    # If the command is FIM
    elif command[0] == "FIM":
        # Return the command
        return command[0]
    # If the command is EC
    elif command[0] == "EC":
        # Get the target
        target = command[1]
        # Get the cards
        cards_str = command[2]
        # EXECUTION
        if get_hostname() == target:
            # split cards
            cards_str = cards_str.split(",")
            cards = []
            # Convert cards to int
            for card in cards_str:
                cards.append(int(card))
            # Set cards as hand
            global hand
            hand = cards
            return
    # If the command is DC
    elif command[0] == "DC":
        # Get the cards
        cards_str = command[1]
        cards_str = cards_str.split(",")
        cards = []
        # Convert cards to int
        for card in cards_str:
            cards.append(int(card))
        # EXECUTION
        global last_played
        last_played.clear()
        last_played = cards
        return
    # If the command is PJ
    elif command[0] == "PJ":
        # Get the target
        target = command[1]
        # EXECUTION
        if get_hostname() == target:
            global bastao
            # Set bastao as true
            bastao = True
            return command[0]

def send_message(message):
    s.sendto(message.encode('ascii'), (targetInfo[0], int(targetInfo[1])))

def receive_message():
    data, addr = s.recvfrom(1024)
    data = data.decode('ascii')
    return data

def send_hands():
    global hands
    # Get all hostnames
    hostnames = get_hostnames()
    for hostname in hostnames:
        if hostname != get_hostname():
            # Create message
            message = create_message(get_hostname(), hostname, "EC", hands.pop(0), 0)
            # Send message
            send_message(message)
            received = receive_message()
            received = translate_message(received)
            execute_command(received[0])
            # Check if confirmation is correct
            if check_confirmation(num_players, received[1]) is False:
                print("Confirmation is incorrect")
                exit(1)

def listen_messages():
    global ja_comecou
    # Listen to messages
    while True:

        if len(finished_order) == num_players - 1:
            # Find last hostname and append to finished_order
            for hostname in get_hostnames():
                if hostname not in finished_order:
                    finished_order.append(hostname)

        if ja_comecou == 1:
            os.system('clear')
            if finished_hand is False:
                print_game_state()
                print("Esperando player jogar")
            else:
                print_game_state()
                print("Voce ja terminou o jogo, aguarde os outros jogadores")
        # Receive message
        received = receive_message()
        # Translate message
        received = translate_message(received)
        # Execute command
        action = execute_command(received[0])
        # Send confirmation
        send_message(received[1])
        if action == "IJ":
            #os.system('clear')
            ja_comecou = 1
            break
        elif action == "PJ":
            #os.system('clear')
            break
        elif action == "FIM":
            global fim
            fim = True
            #os.system('clear')
            break

# Create, send and receive IJ message
def send_IJ():
    # Create message
    message = create_message(get_hostname(), "", "IJ", "", 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation IJ is incorrect")
        exit(1)

# Create, send and receive EC message
def send_EC(target):
    # Create message
    message = create_message(get_hostname(), target, "EC", hand, 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation EC is incorrect")
        exit(1)

# Create, send and receive DC message
def send_DC(jogada):
    global last_played
    # Create message
    message = create_message(get_hostname(), "", "DC", jogada, 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation DC is incorrect")
        exit(1)
    last_played.clear()
    last_played = jogada
    

# Create, send and receive PJ message
def send_PJ(target):
    global bastao
    bastao = False
    # Create message
    message = create_message(get_hostname(), target, "PJ", "", 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation PJ is incorrect")
        exit(1)

# Create, send and receive APC message
def send_APC(num):
    global pass_count
    if num == 0:
        pass_count = 0
    else:
        pass_count += 1
    # Create message
    message = create_message(get_hostname(), "", "APC", pass_count, 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation APC is incorrect")
        exit(1)

# Create, send and receive NR message
def send_NR():
    # Create message
    message = create_message(get_hostname(), "", "NR", "", 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation NR is incorrect")
        exit(1)

# Create, send and receive AFC message
def send_AFC(num):
    global finished_count
    if num == 1:
        finished_count += 1
    # Create message
    message = create_message(get_hostname(), "", "AFC", finished_count, 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation AFC is incorrect")
        exit(1)

# Create, send and receive FIM message
def send_FIM():
    # Create message
    message = create_message(get_hostname(), "", "FIM", "", 0)
    # Send message
    send_message(message)
    # Receive message
    received = receive_message()
    # Translate message
    received = translate_message(received)
    # Execute command
    execute_command(received[0])
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation FIM is incorrect")
        exit(1)

# GAMEPLAY RELATED FUNCTIONS

def get_num_players():
    num_players = len(tokenring)
    return num_players

def generate_deck():
    for i in range(1, 5):
        for j in range(1, (i + 1)):
            deck.append(i)
    deck.append(13)
    deck.append(13)
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)

def get_hands(num_players, deck):
    # Create num_players arrays
    hands = [[] for _ in range(num_players)]
    # Pop deck until it is empty cycling through the hands
    while deck:
        for hand in hands:
            # Try pop from deck, if deck is empty break
            try:
                hand.append(deck.pop())
            except IndexError:
                break
    # Sort the cards in each player's hand
    for hand in hands:
        hand.sort(key=lambda x: x, reverse=False)
    return hands

# Check if I have bastao and carteador
def check_bastao(myInfo):
    if myInfo[2] == "GreaterDalmuti":
        return True
    return False

# Print Game State
def print_game_state():
    #CLEAR SCREEN
    #os.system('clear')
    print("Current round:", round_counter)
    print("My name:", get_hostname())
    print("My hand:", hand)
    print("Passes (", pass_count, "/", num_players, ")")
    # Print finished_count similar to pass_count
    print("Finished players (", finished_count, "/", num_players, "):", finished_order)
    print("Last player:", last_player)
    print("Last played:", last_played)

def check_cards():
    # Check if with current hand I can play
    global hand
    global last_played

    if len(last_played) == 0:
        return True

    # Get jester count
    jester_count = hand.count(13)

    # Get last card played
    last_card = last_played[0]

    if(last_card == 1):
        return False

    # Count cards lower than last card using range
    for i in range(1, last_card):
        count = hand.count(i)
        # add jester count to count
        if count > 0:
            count += jester_count
            # if count is greater than last_played return true
            if count >= len(last_played):
                return True
        
    return False

def check_jogada(jogada):
    global hand
    hand_copy = hand.copy()

    if(len(last_played) > 0):
        if len(jogada) != len(last_played):
            return False
    
    # Check if ultima_jogada is empty
    if len(last_played) > 0:
        if jogada[0] >= last_played[0]:
            return False

    # Check if the cards are in the player's hand
    for card in jogada:
        if card not in hand_copy:
            return False
        else:
            if len(last_played) > 0:
                if card != 13:
                    if card >= last_played[0]:
                        return False
                    else:
                        hand_copy.remove(card)
            else:
                # Remove card from player_cards_copy
                hand_copy.remove(card)

    # Count the number of jesters in cards
    jester_count = jogada.count(13)
        
    # Check if all cards except jesters are the same
    if len(jogada) - jester_count > 1:
        for card in jogada:
            if card != 13:
                if jogada.count(card) != len(jogada) - jester_count:
                    return False

    return True

# MAIN FUNCTION
# ----- Prepare tokenring, myInfo and targetInfo -----
tokenring = create_tokenring("config.file")
num_players = get_num_players()
myInfo = get_HPR(get_hostname())
targetInfo = get_next_HPR(get_hostname())

# ----- Socket functions -----
s = get_socket()
# bind socket to myInfo
s.bind((myInfo[0], int(myInfo[1])))

# ----- Preparing Game -----
# Check if I have bastao and carteador
if check_bastao(myInfo) is True:
    bastao = True
    carteador = True

# ----- GAME START WAITING FOR INPUT -----
# Wait for input
if(bastao is True):
    input("Press Enter quando todos estiverem conectados")
    #os.system('clear')
else:
    print("Esperando GD iniciar o jogo")

# Generate deck and shuffle it
if carteador is True:
    deck = generate_deck()
    shuffle_deck(deck)
    # Deal cards
    hands = get_hands(num_players, deck)
    # Give GD first hand
    hand = hands.pop(0)
    # Send hands to players
    send_hands()
    # Send "IJ"
    message = create_message(get_hostname(), "", "IJ", [], 0)
    send_message(message)
    received = receive_message()
    received = translate_message(received)
    ja_comecou = 1
    # Check if confirmation is correct
    if check_confirmation(num_players, received[1]) is False:
        print("Confirmation is incorrect")
        exit(1)
else:
    listen_messages()

# ----- GAME LOOP -----
def pass_func(last_player, num_players, pass_count, targetInfo, get_greatdalmuti, send_PJ, send_APC, send_NR):
    send_APC(1) # Aumenta o contador de passes
    if pass_count == num_players:
        persistent_player = last_player
        send_NR() # Sinaliza novo round
        if persistent_player == "":
            # Envia bastao para Dalmuti
            if finished_hand is False:
                input("Ninguem jogou nada, retornando para o Great Dalmuti")
            send_PJ(get_greatdalmuti())
        else:
            # Envia bastao para last_player
            # Check if persistent_player is the on finished_order
            if persistent_player in finished_order:
                # Envia bastao para next_player
                send_PJ(get_next_host(persistent_player))
            else:
                send_PJ(persistent_player)
    else:
                # Envia bastao para next_player
        send_PJ(targetInfo[0])

def cycle_breaker():
    if len(finished_order) == (num_players - 1) or len(finished_order) == num_players:
        # Find last hostname and append to finished_order
        for hostname in get_hostnames():
            if hostname not in finished_order:
                finished_order.append(hostname)
        return True
    return False

while True:

    if fim is True:
        break

    if bastao is True:
        os.system('clear')
        print_game_state()

        if finished_hand is True:
            print("Voce ja terminou o jogo, aguarde os outros jogadores")
            # use pass_func
            if cycle_breaker() is True:
                send_FIM()
                break
            pass_func(last_player, num_players, pass_count, targetInfo, get_greatdalmuti, send_PJ, send_APC, send_NR)
        elif check_cards() is False: # NAO PODE JOGAR
            if cycle_breaker() is True:
                send_FIM()
                break
            input("Voce nao tem jogadas possiveis, pressione enter para passar")
            pass_func(last_player, num_players, pass_count, targetInfo, get_greatdalmuti, send_PJ, send_APC, send_NR)
        elif check_cards() is True: # PODE JOGAR
            if cycle_breaker() is True:
                send_FIM()
                break
            value = input("Press Enter para passar a vez ou digite o valor da quantidade de cartas que deseja jogar: ")
            if len(value) > 0:
                value = int(value)
                if value > 0 and value <= len(hand):
                    # Get cards from player
                    jogada = []
                    for i in range(value):
                        jogada.append(int(input("Digite o valor da carta: ")))
                    # sort cards
                    jogada.sort()
                    # Check if cards are valid
                    if check_jogada(jogada) is True:
                        input("Jogada valida, pressione enter para jogar")
                        # Remove cards from hand
                        for card in jogada:
                            hand.remove(card)

                        if len(hand) == 0:
                            if finished_hand is False:
                                finished_hand = True
                                finished_order.append(myInfo[0])
                                send_AFC(1)

                        send_APC(0) # RESETA CONTADOR DE PASSES
                        send_DC(jogada) # Envia jogada
                        send_PJ(targetInfo[0]) # Envia bastao para next_player
                    else:
                        input("Jogada invalida, pressione enter para tentar novamente")
                else:
                    print("Valor invalido")
            else: # PODIA JOGAR MAS DECIDIU PULAR
                send_APC(1) # Aumenta o contador de passes
                if pass_count == num_players:
                    persistent_player = last_player
                    send_NR() # Sinaliza novo round
                    if persistent_player == "":
                        # Envia bastao para Dalmuti
                        input("Ninguem jogou nada, pressione enter para retornar para o Great Dalmuti")
                        send_PJ(get_greatdalmuti())
                    else:
                        # Envia bastao para last_player
                        send_PJ(persistent_player)
                else:
                    # Envia bastao para next_player
                    send_PJ(targetInfo[0])
    else:
        listen_messages()

# ----- GAME END -----
os.system('clear')
print("Fim de jogo")
print("Ordem de termino:", finished_order)
print("Seu ranking era", myInfo[2])
print("Voce ficou em", finished_order.index(myInfo[0]) + 1, "lugar")

if bastao is True:
    f = open("config.file", "w")
    port_list = get_port_list()
    rank_list = get_rank_list()

    # Using finished_order, port_list and rank_list
    for i in range(len(finished_order)):
        if i != 0:
            f.write("\n")
        f.write(finished_order[i] + " " + port_list[i] + " " + rank_list[i])
    f.close()