from socket_protocol import *
from game_logic import *
from game_logic import ultima_jogada, player_cards

def main():
    pass_count = 0
    auto_pass = False
    round_count = 0
    screen_erased = 0
    tHost, tPort, tRank, host, port, rank, s, tr, baton, card_dealer = initiate_tokenring()
    host_list = get_host_list(tr)
    send_cards(tHost, tPort, host, s, tr, card_dealer, host_list)
    #os.system('clear')

    # GAMELOOP HERE
    while True:
        if baton == 1:
            if len(ultima_jogada) > check_max_cards() or compare_cards(player_cards, ultima_jogada) == False or auto_pass == True:
                pass_count += 1
                auto_pass = True
                passagem_bastao(tHost, tPort, host, s, tr, baton)

            print("-----  ROUND " + str(round_count) + "  -----")
            print(str(pass_count))
            played = play_cards(screen_erased)

            if len(played) > 0:
                baton = descartar(tHost, tPort, host, s, tr, baton, played)
                pass_count = 0
            elif len(played) == 0:
                pass_count += 1
                auto_pass = True
                passagem_bastao(tHost, tPort, host, s, tr, baton)
        else:
            print(player_cards)
            # Listen to message
            exec, command, msg_arr = receive_message(s)
            if(exec == True):
                cmd = read_command(command)
                # envia mensagem
                new_msg = create_message(msg_arr[2], msg_arr[1], int(msg_arr[3]) + 1)
                s.sendto(new_msg.encode('ascii'), (tHost, int(tPort)))
                if(cmd == "break"):
                    break
                if(cmd == "discarded"):
                    print("Ultima jogada realizada:", ultima_jogada)
                if(cmd == "pass"):
                    baton = 1
            else:
                new_msg = create_message(msg_arr[2], msg_arr[1], int(msg_arr[3]) + 1)
                # envia mensagem
                s.sendto(new_msg.encode('ascii'), (tHost, int(tPort)))

main()