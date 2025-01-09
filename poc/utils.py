from typing import List
from collections import Counter

import numpy as np

from poc.pocl import Card, Bord, Hand 
from poc.const import VALUE_COUNTS

def get_card_value_rank(card_value: str):
    return VALUE_COUNTS[card_value]


def senior_card_check(all_cards: List[Card]):
    senior_card = None
    senior_card_rank = 0
    for card in all_cards:
        if senior_card_rank < card.get_value_rank():
            senior_card_rank = card.get_value_rank()
            senior_card = card
    return senior_card_rank, set([senior_card]), 'senior'
    

def pair_check(all_cards: List[Card]):
    counter = Counter([card.value for card in all_cards])
    pair_cards = np.array([item for item, value in counter.items() if value > 1])
    pair_rank = np.array([get_card_value_rank(it) for it in pair_cards])
    
    if len(pair_cards) == 1:
        pair_rank = pair_rank[0] + get_card_value_rank('A')
        pair_cards = [it for it in all_cards if it.value == pair_cards[0]]
        assert len(pair_cards) > 1, 'Ошибка при подсчете пар'
        return pair_rank, pair_cards, 'pair'

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
        return pair_rank, pair_cards, 'pair'
    
    return 0, [], 'pair'


def trips_check(all_cards: List[Card]):
    counter = Counter([card.value for card in all_cards])
    trips_cards_value = np.array([item for item, value in counter.items() if value == 3])
    trips_rank = np.array([get_card_value_rank(it) for it in trips_cards_value])

    if len(trips_rank) == 0:
        return 0, [], 'triplet'
    
    max_trips_idx = 0
    if len(trips_rank) > 1:
        max_trips_idx = np.argmax(trips_rank)

    trips_rank = trips_rank[max_trips_idx]
    trips_cards_value = trips_cards_value[max_trips_idx]

    trips_rank = trips_rank + 1313
    trips_cards = [it for it in all_cards if it.value == trips_cards_value]
    return trips_rank, trips_cards, 'triplet'


def straight_check(all_cards: List[Card]):
    unique_card_values = np.array(list(set([it.value for it in all_cards])))
    unique_card_rank = np.array([get_card_value_rank(it) for it in unique_card_values])
    sorted_idx = np.argsort(unique_card_rank)
    unique_card_rank = unique_card_rank[sorted_idx]
    unique_card_values = unique_card_values[sorted_idx]
    
    if 'A' in unique_card_values:
        unique_card_values = np.insert(unique_card_values, 0, 'A')
        unique_card_rank = np.insert(unique_card_rank, 0, 0)

    ordered_cards = 1
    straight_card_values = [unique_card_values[0]]
    for i in range(1, len(unique_card_values)):
        value_diff = unique_card_rank[i] - unique_card_rank[i-1]
        if value_diff == 1:
            ordered_cards += 1
            straight_card_values.append(unique_card_values[i])
        else:
            if ordered_cards < 5:
                ordered_cards = 1
                straight_card_values = [unique_card_values[i]]
            else:
                break

    if ordered_cards < 5:
        return 0, [], 'straight'
    
    strit_rank = get_card_value_rank(straight_card_values[-1])
    strit_rank += 13 + 1313 # more than high set

    straight_cards = []
    for value in straight_card_values[-5:]:
        for card in all_cards:
            if card.value == value:
                straight_cards.append(card)
    
    return strit_rank, straight_cards, 'straight'


def flush_check(all_cards: List[Card]):
    counter = Counter([card.suit for card in all_cards])
    flush_suit = np.array([item for item, value in counter.items() if value > 4])
    if len(flush_suit) == 0:
        return 0, [], 'flush'
    
    flush_suit = flush_suit[0] # can be only one flush
    flush_cards = [it for it in all_cards if it.suit == flush_suit]
    sorted_flush_cards = sorted(flush_cards, reverse=True)[:5] # use 5 max card values
    flush_rank = ''.join([str(get_card_value_rank(it.value)) for it in sorted_flush_cards])
    return int(flush_rank), sorted_flush_cards, 'flush'


def check_full_house(all_cards: List[Card]):
    _, pair_cards, _ = pair_check(all_cards) 
    _, trips_cards, _ = trips_check(all_cards)

    if (len(pair_cards) == 0) | (len(trips_cards) == 0):
        return 0, [], 'full_house'

    pair_value = np.array(list(set([it.value for it in pair_cards]))) # get value of all pairs
    trips_value = max(list(set([it.value for it in trips_cards]))) # get only one value of trips
    pair_value = pair_value[pair_value != trips_value] # drop pair if it is a trips
    if len(pair_value) == 0:
        return 0, [], 'full_house'
    
    pair_value = max(pair_value) # get max pair

    full_house_cards = [it for it in all_cards if (it.value == pair_value) | (it.value == trips_value)]
    pair_rank = str(get_card_value_rank(pair_value))
    trips_rank = str(get_card_value_rank(trips_value))

    pair_rank = '0'+pair_rank if len(pair_rank) < 2 else pair_rank
    trips_rank = '0'+trips_rank if len(trips_rank) < 2 else trips_rank

    full_house_rank = str(trips_rank) + str(pair_rank) + '13'*5 # more than max flush
    full_house_rank = int(full_house_rank)
    return full_house_rank, full_house_cards, 'full_house'


def check_square(all_cards: List[Card]):
    counter = Counter([card.value for card in all_cards])
    square_cards_value = np.array([item for item, value in counter.items() if value == 4])
    if len(square_cards_value) == 0:
        return 0, [], 'square'

    square_cards_value = square_cards_value[0]
    square_cards = [it for it in all_cards if it.value == square_cards_value]
    square_rank = get_card_value_rank(square_cards_value)
    square_rank = square_rank + int('13'*7)
    return square_rank, square_cards, 'square'


def check_straight_flush(all_cards: List[Card]):
    # calc all flush card
    counter = Counter([card.suit for card in all_cards])
    flush_suit = np.array([item for item, value in counter.items() if value > 4])
    if len(flush_suit) == 0:
        return 0, [], 'straight_flush'
    
    flush_suit = flush_suit[0] # can be only one flush
    flush_cards = [it for it in all_cards if it.suit == flush_suit]

    straight_rank, straight_cards, _ = straight_check(flush_cards)
    if len(straight_cards) == 0:
        return 0, [], 'straight_flush'

    straight_flush_rank = straight_rank + int('13'*7) + 13
    return straight_flush_rank, straight_cards, 'straight_flush'


def calc_max_combination(hand: Hand, bord: Bord):
    comb_rank = 0
    comb_cards = set()
    
    all_cards = [hand.card_1, hand.card_2] + bord.get_card_list()
    all_cards = list(filter(lambda x: (x.value is not None) and (x.suit is not None), all_cards))
    max_combination = None

    combination_func_list = [
        senior_card_check,
        pair_check,
        trips_check,
        straight_check,
        flush_check,
        check_full_house,
        check_square,
        check_straight_flush,
    ]

    for combination_func in combination_func_list:
        rank, cards, combination = combination_func(all_cards)
        if comb_rank < rank:
            comb_rank = rank
            comb_cards = cards
            max_combination = combination

    kiker_rank = 0
    if len(comb_cards) < 5:
        non_usage_cards = []
        for card in all_cards:
            if card not in comb_cards:
                non_usage_cards.append(card)
        non_usage_cards = sorted(non_usage_cards, reverse=True)
        
        kikers_num = 5 - len(comb_cards)
        kikers_cards = non_usage_cards[:kikers_num]
        kiker_rank = int(''.join([str(get_card_value_rank(it.value)) for it in kikers_cards]))
        
    return comb_rank, kiker_rank, max_combination


def parse_card(card_str: str):
    value, suit = card_str[:-1], card_str[-1]
    card = Card(value.upper(), suit.upper())
    return card


def parse_test_case(test_case: str):
    try:
        hands, bord, result = test_case.replace(' ', '').split('\n')
    except:
        pass
    hand_list = []
    for hand in hands.split(';'):
        hand_list.append(
            Hand(*[
                Card(*it.split(':')) for it in hand.split(',')
            ])
        )
    bord = [Card(*it.split(':')) for it in bord.split(',')]
    bord = Bord(*bord)
    result = [int(it) for it in result.split(',')]
    return hand_list, bord, result 


def read_test_cases(file_name):
    test_cases = []
    with open(file_name, 'r') as f:
        test_data = f.read().split('\n\n')
        for test_case in test_data:
            hand_list, bord, result = parse_test_case(test_case)
            test_cases.append(dict(
                hand_list=hand_list,
                bord=bord,
                result=result,
            ))
    return test_cases
        

def get_hand_result(
    hand_list: List[Hand],
    bord: Bord,
    **args,
):
    hand_results = [calc_max_combination(hand, bord) for hand in hand_list]
    hand_value_results = np.array([it[0] for it in hand_results])
    hand_kiker_results = np.array([it[1] for it in hand_results])

    max_value_mask = hand_value_results == max(hand_value_results)
    max_kiker_of_win_hand = max(hand_kiker_results[max_value_mask])
    max_value_with_kiker = (
        (hand_kiker_results == max_kiker_of_win_hand)
        & max_value_mask
    )

    return np.where(max_value_with_kiker)[0] + 1