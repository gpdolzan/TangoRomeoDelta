import random

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


def exchange_cards(players):
    # Greater Peon and Lesser Peon exchange their highest cards with the Greater Dalmuti and Lesser Dalmuti respectively
    players["Greater Dalmuti"].append(players["Greater Peon"].pop(0))
    players["Greater Dalmuti"].append(players["Greater Peon"].pop(0))
    players["Lesser Dalmuti"].append(players["Lesser Peon"].pop(0))

    # Greater Peon and Lesser Peon exchange the cards they want with the Lesser Dalmuti and Greater Dalmuti respectively
    print("Greater Dalmuti, which cards do you want to exchange? Enter the card values.")
    card1 = int(input())
    card2 = int(input())
    players["Greater Peon"].append(players["Greater Dalmuti"].pop(get_card_index(players["Greater Dalmuti"], card1)))
    players["Greater Peon"].append(players["Greater Dalmuti"].pop(get_card_index(players["Greater Dalmuti"], card2)))

    print("Lesser Dalmuti, which cards do you want to exchange? Enter the card values.")
    card3 = int(input())
    players["Lesser Peon"].append(players["Lesser Dalmuti"].pop(get_card_index(players["Lesser Dalmuti"], card3)))

# function to check if the game has a possible revolution
def check_revolution(players):
    jester_count = 0
    for player, hand in players.items():
        if hand.count(("Jester (alone)", 13)) == 2:
            jester_count += 1
            print(f"{player} has two Jesters and can start a Revolution! A Revolution means that no one has to exchange cards before the game starts.")
            return player

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
            hand.append(deck.pop())
    # Sort the cards in each player's hand
    for hand in hands:
        hand.sort(key=lambda x: x[1], reverse=False)
    return hands

# function to distribute cards for players evenly, starting with the Greater Dalmuti and giving one card to each player clockwise

#player_names = list(players.keys())  # Get a list of player names
#num_players = len(players)  # Get the number of players
#card_index = 0  # Initialize the card index

#for card in deck:
    # Select the player based on the card index
    #player = player_names[card_index % num_players]
    #players[player].append(card)  # Assign the card to the player
    #card_index += 1  # Increment the card index

# Print the cards assigned to each player

#def print_cards(players):
    #for player, cards in players.items():
        #print(f"Number of cards: {len(cards)}")
        #print(f"{player}: {cards}")

#print_cards(players)
#exchange_cards(players)
#print_cards(players)
# check_revolution(players)