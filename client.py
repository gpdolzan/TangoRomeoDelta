from socket_protocol import *
from game_logic import *
from game_logic import player_cards

def main():
    tHost, tPort, tRank, host, port, rank, s, tr, baton, card_dealer = initiate_tokenring()
    host_list = get_host_list(tr)
    send_cards(tHost, tPort, host, s, tr, card_dealer, host_list)
    print(player_cards)

    # GAMELOOP HERE
    if baton == 1:
        pass

main()