import argparse
from typing import List
from const import VALUE_COUNTS, SUITS


class Card:
    def __init__(self, value:str = None, suit:str = None):
        assert value in VALUE_COUNTS, 'Недопустимое значение карты!'
        assert suit in SUITS, 'Недопустимое значение масти'
        self.value = value
        self.suit = suit
    
    def get_value_rank(self):
        return VALUE_COUNTS[self.value]

    # Определение оператора ==
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.get_value_rank() == other.get_value_rank()
        return False
    
    # Определение оператора !=
    def __ne__(self, other):
        return not self.__eq__(other)       
    
    # Определение оператора <
    def __lt__(self, other):
        if isinstance(other, Card):
            return self.get_value_rank() < other.get_value_rank()
        return False

    # Определение оператора <=
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    # Определение оператора >
    def __gt__(self, other):
        return not self.__le__(other)

    # Определение оператора >=
    def __ge__(self, other):
        return not self.__lt__(other)

    # Определение str
    def __str__(self):
        return self.value + self.suit
    
    def __hash__(self):
        # Используем комбинацию value и suit для хеширования
        return hash((self.value, self.suit))
    

class Hand:
    def __init__(self, card_1: Card, card_2: Card):
        self.card_1 = card_1
        self.card_2 = card_2
    
class Bord:
    def __init__(
        self,
        card_1: Card = Card(),
        card_2: Card = Card(),
        card_3: Card = Card(),
        card_4: Card = Card(),
        card_5: Card = Card(),
    ):
        self.card_1 = card_1
        self.card_2 = card_2
        self.card_3 = card_3
        self.card_4 = card_4
        self.card_5 = card_5
        
    def get_card_list(self):
        return [
            self.card_1, 
            self.card_2,
            self.card_3,
            self.card_4,
            self.card_5,
        ]


def senior_card_check(all_cards: List[Card]):
    senior_card = None
    senior_card_rank = 0
    for card in all_cards:
        if senior_card_rank < card.get_value_rank():
            senior_card_rank = card.get_value_rank()
            senior_card = card
    return senior_card_rank, senior_card
    

def calc_max_combination(hand: Hand, bord: Bord):
    comb_rank = 0
    comb_cards = set()
    
    all_cards = [hand.card_1, hand.card_2] + bord.get_card_list()
    all_cards = list(filter(lambda x: (x.value is not None) and (x.suit is not None), all_cards))
    
    senior_card_rank, senior_card = senior_card_check(all_cards)
    if comb_rank < senior_card_rank:
        comb_rank = senior_card_rank
        comb_cards.add(senior_card)
    
    return comb_rank, comb_cards


def parse_card(card_str: str):
    value, suit = card_str[:-1], card_str[-1]
    card = Card(value.upper(), suit.upper())
    return card


hand_1 = Hand(card_1=Card('2', 'D'), card_2=Card('2', 'S'))
hand_2 = Hand(card_1=Card('A', 'D'), card_2=Card('Q', 'S'))
bord = Bord(
    card_1=Card('J', 'D'),
    card_2=Card('3', 'D')
)

comb_rank_1, comb_cards_1 = calc_max_combination(hand_1, bord)
comb_rank_2, comb_cards_2 = calc_max_combination(hand_2, bord)

print(comb_rank_1)
for it in comb_cards_1:
    print(it)
    
print(comb_rank_2)
for it in comb_cards_2:
    print(it)


# card_1 = parse_card(input('Первая карта в руке: '))
# card_2 = parse_card(input('Вторая карта в руке: '))        
 
# print(card_1)
# print(card_2)