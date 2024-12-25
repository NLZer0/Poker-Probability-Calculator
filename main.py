import argparse
from typing import List
from collections import Counter
from const import VALUE_COUNTS, SUITS

import numpy as np


class Card:
    def __init__(self, value:str = None, suit:str = None):
        assert value in VALUE_COUNTS, 'Недопустимое значение карты!'
        assert suit in SUITS, 'Недопустимое значение масти'
        self.value = value
        self.suit = suit
    
    def is_similar(self, other):
        if isinstance(other, Card):
            if (self.value == other.value) & (self.suit == other.suit): 
                return True
        return False

    def get_value_rank(self):
        return VALUE_COUNTS[self.value]

    # Определение оператора in
    def __contains__(self, card_list):
        return any(self.is_similar(it) for it in card_list)

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
    
    def isin(self, card: Card):
        if isinstance(card, Card):
            if self.card_1.is_similar(card) | self.card_2.is_similar(card):
                return True
        return False
    
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


def get_card_value_rank(card_value: str):
    return VALUE_COUNTS[card_value]


def senior_card_check(all_cards: List[Card]):
    senior_card = None
    senior_card_rank = 0
    for card in all_cards:
        if senior_card_rank < card.get_value_rank():
            senior_card_rank = card.get_value_rank()
            senior_card = card
    return senior_card_rank, senior_card
    

def pair_check(all_cards: List[Card]):
    counter = Counter([card.value for card in all_cards])
    pair_cards = np.array([item for item, value in counter.items() if value == 2])
    pair_rank = np.array([get_card_value_rank(it) for it in pair_cards])
    
    if len(pair_cards) == 1:
        pair_rank = pair_rank[0] + get_card_value_rank('A')
        pair_cards = [it for it in all_cards if it.value == pair_cards[0]]
        assert len(pair_cards) == 2, 'Ошибка при подсчете пар'
        return pair_rank, pair_cards

    if len(pair_cards) >= 2:
        max_rank_pairs = np.argsort(-1*pair_rank)[:2]
        pair_cards = pair_cards[max_rank_pairs]
        pair_rank = pair_rank[max_rank_pairs]
        
        c1_rank = str(pair_rank[0])
        c2_rank = str(pair_rank[1])
        c1_rank = f'0{c1_rank}' if len(c1_rank) == 1 else c1_rank
        c2_rank = f'0{c2_rank}' if len(c2_rank) == 1 else c2_rank
        
        pair_rank = int(c1_rank+c2_rank)
        pair_cards = [it for it in all_cards if (it.value == pair_cards[0]) | (it.value == pair_cards[1])]
        return pair_rank, pair_cards
    
    return 0, []


def trips_check(all_cards: List[Card]):
    counter = Counter([card.value for card in all_cards])
    trips_cards_value = np.array([item for item, value in counter.items() if value == 3])
    trips_rank = np.array([get_card_value_rank(it) for it in trips_cards_value])

    if len(trips_rank) == 0:
        return 0, []
    
    max_trips_idx = 0
    if len(trips_rank) > 1:
        max_trips_idx = np.argmax(trips_rank)

    trips_rank = trips_rank[max_trips_idx]
    trips_cards_value = trips_cards_value[max_trips_idx]

    trips_rank = trips_rank + 1313
    trips_cards = [it for it in all_cards if it.value == trips_cards_value]
    return trips_rank, trips_cards


def calc_max_combination(hand: Hand, bord: Bord):
    comb_rank = 0
    comb_cards = set()
    
    all_cards = [hand.card_1, hand.card_2] + bord.get_card_list()
    all_cards = list(filter(lambda x: (x.value is not None) and (x.suit is not None), all_cards))
    
    senior_card_rank, senior_card = senior_card_check(all_cards)
    if comb_rank < senior_card_rank:
        comb_rank = senior_card_rank
        comb_cards = set([senior_card])

    pair_rank, pair_cards = pair_check(all_cards)
    if comb_rank < pair_rank:
        comb_cards = pair_cards
        comb_rank = pair_rank

    trips_rank, trips_cards = trips_check(all_cards)
    if comb_rank < trips_rank:
        comb_cards = trips_cards
        comb_rank = trips_rank

    if len(comb_cards) < 5:
        non_usage_cards = []
        for card in all_cards:
            if card not in comb_cards:
                non_usage_cards.append(card)
        non_usage_cards = sorted(non_usage_cards, reverse=True)
        
        kikers_num = 5 - len(comb_cards)
        kikers_cards = non_usage_cards[:kikers_num]
        kiker_rank = int(''.join([str(get_card_value_rank(it.value)) for it in kikers_cards]))
        
    return comb_rank, comb_cards, kiker_rank


def parse_card(card_str: str):
    value, suit = card_str[:-1], card_str[-1]
    card = Card(value.upper(), suit.upper())
    return card


hand_1 = Hand(card_1=Card('2', 'S'), card_2=Card('J', 'S'))
hand_2 = Hand(card_1=Card('2', 'C'), card_2=Card('Q', 'S'))
bord = Bord(
    card_1=Card('2', 'D'),
    card_2=Card('10', 'S'),
    card_3=Card('K', 'S'),
    card_4=Card('4', 'D'),
    card_5=Card('3', 'H')
)

comb_rank_1, comb_cards_1, kiker_rank_1 = calc_max_combination(hand_1, bord)
comb_rank_2, comb_cards_2, kiker_rank_2 = calc_max_combination(hand_2, bord)

print(comb_rank_1)
print(kiker_rank_1)
for it in comb_cards_1:
    print(it)

print('-'*10)

print(comb_rank_2)
print(kiker_rank_2)
for it in comb_cards_2:
    print(it)

# card_1 = parse_card(input('Первая карта в руке: '))
# card_2 = parse_card(input('Вторая карта в руке: '))        
 
# print(card_1)
# print(card_2)

# card = Card('10', 'S')
# card_list = [Card('2', 'S'), Card('10', 'S')]
# print(card in card_list)