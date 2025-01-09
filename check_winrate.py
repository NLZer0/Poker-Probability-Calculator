import random
import argparse
from itertools import product

from poc.utils import calc_max_combination
from poc.pocl import Card, Hand, Bord, Deck
from poc.const import VALUE_COUNTS, SUITS


parser = argparse.ArgumentParser()
parser.add_argument('-mh', '--main_hand', type=str)
parser.add_argument('-pn', '--players_num', type=int, default=1)
parser.add_argument('-oh', '--other_hand', type=str, default=None)
parser.add_argument('-b', '--bord', type=str, default=None)
parser.add_argument('-n', '--random_num', type=int, default=100)
args = parser.parse_args()


if __name__ == '__main__':
    deck = Deck()
    
    wins = 0
    losses = 0

    for it in range(args.random_num):
        deck.shuffle_cards()

        main_hand = args.main_hand.split(',')
        main_hand = Hand(**{f'card_{i}': Card(*it.split(':')) for i, it in enumerate(main_hand, start=1)})
        
        other_hands = []
        if args.other_hand is None:
            for player_n in range(args.players_num):
                other_hands.append(
                    Hand(
                        deck.get_rand_card(),
                        deck.get_rand_card()
                    )
                )
        else:
            other_hands_str = args.other_hand.split(';')
            for hand in other_hands_str:
                other_hands.append(
                    Hand(**{f'card_{i}': Card(*it.split(':')) for i, it in enumerate(hand.split(','), start=1)})
                )
            
            while len(other_hands) < args.players_num:
                other_hands.append(
                    Hand(
                        deck.get_rand_card(),
                        deck.get_rand_card()
                    )
                )

        if args.bord is None:
            bord = Bord(*[deck.get_rand_card() for _ in range(5)])
        else:
            bord = args.bord.split(',')
            bord_cards = [Card(*it.split(':')) for it in bord]
            while len(bord_cards) < 5:
                bord_cards.append(deck.get_rand_card())
            bord = Bord(*bord_cards)

        main_rank, _, _ = calc_max_combination(main_hand, bord)
        players_max_rank = max([calc_max_combination(hand, bord)[0] for hand in other_hands])

        if main_rank >= players_max_rank:
            wins += 1
        else:
            losses += 1
    
    print(f'Avg winrate: {wins/(wins+losses):.3f}')

    