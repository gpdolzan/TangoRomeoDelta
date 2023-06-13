import random
from socket_protocol import *
import os

player_cards = []
ultima_jogada = []

cards = {
    "Jester (alone)": 13,
    "Peasants": 12,
    "Stonecutter": 11,
    "Shepherdess": 10,
    "Cook": 9,
    "Mason": 8,
    "Seamstress": 7,
    "Knight": 6,
    "Abbess": 5,
    "Baroness": 4,
    "Earl Marshal": 3,
    "Archbishop": 2,
    "The Great Dalmuti": 1
}

players = {
    "Greater Dalmuti": [],
    "Lesser Dalmuti": [],
    "Lesser Peon": [],
    "Greater Peon": [],
}
    

def get_card_index(cards, value):
    for i, card in enumerate(cards):
        if card[1] == value:
            return i
    return -1  # Return -1 if the card with the specified value is not found

def generate_deck():
    deck = []
    for card, count in cards.items():
        if card == "Jester (alone)":
            # Add two Jester cards
            deck.extend([(card, count)] * 2)
        else:
            # Add cards based on their count
            deck.extend([(card, count)] * count)
    shuffle_deck(deck)
    return deck


def shuffle_deck(deck):
    random.shuffle(deck)

def deal_cards(num_players, deck):
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
        hand.sort(key=lambda x: x[1], reverse=False)
    return hands

def check_max_cards():
    # Given an array of numbers, count the max number of duplicate numbers
    # Return the max number of duplicate numbers
    max_cards = 0
    for card in player_cards:
        # Count the number of times card appears in player_cards
        if card != 13:
            count = player_cards.count(int(card))
            if count > max_cards:
                max_cards = count
        else:
            max_cards += player_cards.count(13)
    return max_cards

def check_cards(cards, jester_count, ultima_jogada, player_cards):
    # Make a copy of player_cards
    player_cards_copy = player_cards.copy()

    # Check if the cards are in the player's hand
    for card in cards:
        if card not in player_cards_copy:
            return False
        else:
            if len(ultima_jogada) > 0:
                if card >= ultima_jogada[0]:
                    return False
            else:
                # Remove card from player_cards_copy
                player_cards_copy.remove(card)
        
    # Check if all cards except jesters are the same
    if len(cards) - jester_count > 1:
        for card in cards:
            if card != 13:
                if cards.count(card) != len(cards) - jester_count:
                    return False
                
    # Check if ultima_jogada is empty
    if len(ultima_jogada) > 0:
        if cards[0] >= ultima_jogada[0]:
            return False

    return True

def play_cards(screen_erased):
    if screen_erased == 1:
        print("Nao foi possivel fazer a jogada escolhida, tente novamente")
            # Check the max number of cards player can play
    max_cards = check_max_cards()
    print("Você pode descartar no máximo:", max_cards, "cartas")
    # Show deck
    print(player_cards)
    # Show number of cards in deck
    print(len(player_cards))
    # Show ultima_jogada
    if len(ultima_jogada) > 0:
        print(ultima_jogada)
    else:
        print("Nenhuma jogada anterior")

    n_cards = int(input("Digite quantas cartas iguais deseja descartar (0 para passar a vez): "))
    if n_cards == 0:
        return []
    if n_cards > max_cards:
        print("Você não possui essa quantidade de cartas iguais")
        #os.system('clear')
        screen_erased = 1
    else:
                # Read cards from player
        cards = []
                # Count jester
        jester_count = 0
        for i in range(n_cards):
            card = int(input("Digite a carta: "))
            if card == 13:
                jester_count += 1
            cards.append(card)
                    # Sort cards
            cards.sort()
                # Check if cards are valid
        if check_cards(cards, jester_count, ultima_jogada, player_cards):
            #os.system('clear')
            screen_erased = 0
                    # Clear ultima_jogada
            ultima_jogada.clear()
                    # Remove cards from player_cards and append to ultima_jogada
            for card in cards:
                player_cards.remove(card)
                ultima_jogada.append(card)
            return ultima_jogada
        else:
                    # Clear console screen
            #os.system('clear')
            screen_erased = 1

# Function that receives 2 arrays and compare if it is possible to play the cards
def compare_cards(cards, last_played):
    if len(last_played) == 0:
        return True
    if len(cards) != len(last_played):
        return False
    
    num = last_played[0]

    # count the number of times num appears in cards
    count = cards.count(num)
    # count the number of times 13 appears in cards
    count += cards.count(13)

    if count >= len(last_played):
        return True
    return False