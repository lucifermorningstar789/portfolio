import random
from treys import Deck, Evaluator, Card
from itertools import combinations

# Define ranges
your_range = ['KJo', 'KJs', 'KQo', 'KQs', 'AKo', 'AKs',
    'QJo', 'QJs', 'AQo', 'AQs',
    'AJo', 'AJs'
    'JQo', 'JQs',
    '99', 'TT', 'JJ', 'QQ', 'KK', 'AA']

opponent_range = ['22','22','22','22','22','22','33','33','33','33','33','33','44','44','44','44','44','44','55','55','55','55','55','55','66','66','66','66','66','66','77','77','77','77','77','77','88','88','88','88','88','88','99','99','99','99','99','99','TT','TT','TT','TT','TT','TT','JJ','JJ','JJ','JJ','JJ','JJ','QQ','QQ','QQ','QQ','QQ','QQ','KK','KK','KK','KK','KK','KK','AA','AA','AA','AA','AA','AA','J8s','J9s','JTs','JQs','JKs','JAs','J8o','J9o','JTo','JQo','JKo','JAo','Q8s','Q9s','QTs','QJs','QKs','QAs','Q8o','Q9o','QTo','QJo','QKo','QAo','K8s','K9s','KTs','KJs','KQs','KAs','K8o',
                  'K9o','KTo','KJo','KQo','KAo','A8s','A9s','ATs','AJs','AQs','AKs','A8o','A9o','ATo','AJo','AQo','AKo']

def generate_hands(range_list):
    deck = Deck()
    all_hands = []
    for hand_code in range_list:
        if hand_code.endswith('s'):
            rank1, rank2 = hand_code[0], hand_code[1]
            suited = True
        elif hand_code.endswith('o'):
            rank1, rank2 = hand_code[0], hand_code[1]
            suited = False
        else:
            rank1, rank2 = hand_code[0], hand_code[1]
            suited = None  # pocket pair

        combos = []
        for c1 in 'cdhs':
            for c2 in 'cdhs':
                if c1 == c2:
                    continue
                if suited is True and c1 != c2:
                    continue
                if suited is False and c1 == c2:
                    continue

                card1 = Card.new(rank1 + c1)
                card2 = Card.new(rank2 + c2)

                if card1 != card2:
                    if suited is None and rank1 == rank2:
                        combos.append((card1, card2))
                    elif rank1 != rank2:
                        combos.append((card1, card2))
        all_hands.extend(combos)
    return all_hands

your_hands = generate_hands(your_range)
opp_hands = generate_hands(opponent_range)

evaluator = Evaluator()
iterations = 10000
win, lose, tie = 0, 0, 0

x = []
y = []

for i in range(iterations):
    deck = Deck()
    
    your_hand = random.choice(your_hands)
    opp_hand = random.choice(opp_hands)

    # Ensure no duplicate cards
    all_used = set(your_hand + opp_hand)
    deck.cards = [card for card in deck.cards if card not in all_used]

    board = deck.draw(5)

    your_score = evaluator.evaluate(board, list(your_hand))
    opp_score = evaluator.evaluate(board, list(opp_hand))

    if your_score < opp_score:
        win += 1
    elif your_score > opp_score:
        lose += 1
    else:
        tie += 1

    if (i + 1) % 1000 == 0:
        total = win + lose + tie
        if total > 0:
            winrate = win / total * 100
            x.append(i + 1)
            y.append(winrate)

print(f"Results after {iterations} simulations:")
print(f"Win: {win/iterations:.2%}")
print(f"Lose: {lose/iterations:.2%}")
print(f"Tie: {tie/iterations:.2%}")
import matplotlib.pyplot as plt

plt.plot(x, y, color='blue', linewidth=2)
plt.title('Your Win Rate Over Simulations')
plt.xlabel('Number of Simulations')
plt.ylabel('Win Rate (%)')
plt.grid(True)
plt.tight_layout()
plt.show()