from poc.const import VALUE_COUNTS, SUITS

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
