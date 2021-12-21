from random import shuffle
import random


def fill_deck(deck):
    deck.extend([-2]*5)
    deck.extend([0]*15)
    deck.extend([-1]*10)
    deck.extend([1]*10)
    deck.extend([2]*10)
    deck.extend([3]*10)
    deck.extend([4]*10)
    deck.extend([5]*10)
    deck.extend([6]*10)
    deck.extend([7]*10)
    deck.extend([8]*10)
    deck.extend([9]*10)
    deck.extend([10]*10)
    deck.extend([11]*10)
    deck.extend([12]*10)

def fill_table(table, deck):
    for i in range(len(table)):
        for j in range(len(table[i])):
            for k in range(len(table[i][j])):
                table[i][j][k]["num"] = deck[0]
                del deck[0]

def game_over(table):
    #if all cards are faceup for one player, game is over
    for player in table:
        all_cards_up = True
        for row in player:
            for card in row:
                if (card["view"] == False):
                    all_cards_up = False
        if (all_cards_up):
            return True
        return False

def sum_player_cards(player_table):
    sum = 0
    for i in range(3):
        for j in range(4):
            if player_table[i][j]["view"] == True:
                sum += player_table[i][j]["num"]
    return sum

def get_first_player(table):
    sums = []
    for player in table:
        sums.append(sum_player_cards(player))
    return sums.index(max(sums))

def highest_open_card(player_table):
    maxnum = -2
    maxindex = (-1,-1)
    for i in range(len(player_table)):
        for j in range(len(i)):
            if (player_table[i][j]["view"] == True and player_table[i][j]["num"] > max):
                maxnum = player_table[i][j]["num"]
                maxindex = (i, j)
    result = [maxnum, maxindex]
    return result

def random_closed_card(player_table):
    
    is_closed = True

    while(is_closed):
        i = random.randint(0,2)
        j = random.randint(0,3)
        is_closed = player_table[i][j]["view"]

    return (i,j)

def num_replace_strat(player_table, deck):
    result = highest_open_card(player_table)

    #if the faceup card is less than a highest card, swap it with your highest card
    if (deck[0] < result[0]):
        player_table[result[1][0]][result[1][1]], deck[0] = deck[0], player_table[result[1][0]][result[1][1]]

    #else, draw a card to try your luck again; if it's less, do the swap
    elif (deck[1] < result[0]):
        player_table[result[1][0]][result[1][1]], deck[1] = deck[1], player_table[result[1][0]][result[1][1]]
        del deck[0]

    #else, discard the drawn card and then flip over one of your cards
    else:
        del deck[0]
        closed_card = random_closed_card(player_table)
        player_table[closed_card[0]][closed_card[1]]["view"] = True


def start_game(table, deck):
    #make two cards "face up" for each player
    for player in table:
        for i in range(2):
            player[random.randint(0,2)][random.randint(0,3)]["view"] = True

    #start playing, player 1 is "highest num replace" strategy,
    #player 2 is "make rows" strategy

    #player that goes first
    first_player = get_first_player(table)

    #first round, which is truncated depending on who goes first
    #make_rows_strat
    #random_cards_strat
    while (not game_over(table)):
        for i in range(len(table)):
            if (i == 0):
                num_replace_strat(table[i], deck)
            elif (i == 1):
                num_replace_strat(table[i], deck)
            elif (i == 2):
                num_replace_strat(table[i], deck)
    
    sums = []
    for player in table:
        sums.append(sum_player_cards(player))
    
    winner = sums.index(min(sums))
    return winner
        
def setup_game(num_players):
    random.seed()

    #create, fill, and shuffle the deck
    deck = []
    fill_deck(deck)
    shuffle(deck)

    #create a list to hold all of the player's table cards
    table = []

    #give each player an index on the table with a place to put their cards
    for i in range(num_players):
        table.append([[{"num": 0, "view":False}]*4]*3)
        

    #fill each table set with random cards from the deck
    fill_table(table, deck)

    winner = []
    for i in range(100):
        winner.append(start_game(table, deck))

    print(winner)

setup_game(2)