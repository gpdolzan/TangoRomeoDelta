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

""" if player_count >= 4 and player_count <= 8: """

# Revolution check: if player has two jesters, they can start a revolution
def revolution_check(players):
    for player, cards in players.items():
        if cards.count("Jester (alone)") == 2:
            return True
        else:
            return False

deck = []
for card, count in cards.items():
    if card == "Jester (alone)":
        # Add two Jester cards
        deck.extend([(card, count)] * 2)
    else:
        # Add cards based on their count
        deck.extend([(card, count)] * count)


def shuffle_deck(deck):
    random.shuffle(deck)


shuffle_deck(deck)

# function to distribute cards for players evenly, starting with the Greater Dalmuti and giving one card to each player clockwise

player_names = list(players.keys())  # Get a list of player names
num_players = len(players)  # Get the number of players
card_index = 0  # Initialize the card index

for card in deck:
    # Select the player based on the card index
    player = player_names[card_index % num_players]
    players[player].append(card)  # Assign the card to the player
    card_index += 1  # Increment the card index

for player, cards in players.items():
    # Sort the cards in each player's hand
    players[player] = sorted(cards, key=lambda x: x[1], reverse=False)

# Print the cards assigned to each player

def print_cards(players):
    for player, cards in players.items():
        print(f"Number of cards: {len(cards)}")
        print(f"{player}: {cards}")

if revolution_check(players):
    print("Revolution!")

print_cards(players)
