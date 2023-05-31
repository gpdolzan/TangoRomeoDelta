import random

card_name_array = ["The Great Dalmuti", "Archbishop", "Earl Marshal", "Baroness",
    "Abbess", "Knight", "Seamstress", "Mason", "Cook", "Shepherdess",
    "Stonecutter", "Peasants", "Jester"]

class Card:
    def __init__(self, rank):
        self.rank = rank
        self.name = card_name_array[rank - 1]
    def printCard(card):
        print("[" + str(card.rank) + " - " + card.name + "]")

# Object Deck
class Deck:
    cards = []
    def __init__(self):
        for i in range(1, 13): # 1 to 12
            for j in range(1, (i + 1)):
                c = Card(i)
                self.cards.append(c)
        for i in range(1, 3): # 1 to 2
            c = Card(13)
            self.cards.append(c)
    def printDeck(deck):
        for card in deck.cards:
            print("[" + str(card.rank) + " - " + card.name + "]")
    # Random remove a card from deck and return it
    def popCard(deck):
        random_index = random.randint(0, len(deck.cards) - 1)
        return deck.cards.pop(random_index)

#deck = Deck()
#card = deck.popCard()
#card.printCard()