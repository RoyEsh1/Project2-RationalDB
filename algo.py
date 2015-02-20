'''
 Swiss pairing is not at all trivial.
 While many pairing systems I tried work for *most* cases, they didn't work for *all* cases, and didn't find the optimal pairing
 This algorithm ensures that all the players will be paired in an optimal manner
'''

# the main variable, players_pool{} dictionary, looks like this: {1: [2,1,3,0], 2: [1,0,4,1]} 
# which means: Player 1 played against player 2 and won, play 3 and lost; Player 2 played against player 1 and lost, player 4 and won

# Returning all the wins for a player. Since a loss is 0, it doesn't add to the sum
def wins(player):
    return sum(player[1::2])

# Returning a list of who the player played against
def rivals(player):
    return player[::2]

# Returning a list of all the players the player haven't played yet
def can_play_vs(player, player_id, players_pool):
    a = [x for x in players_pool if x not in rivals(player_id) and x <> player]
    return a

# Returning Absolute wins distance from a player. So if P1 has 1 wins and P3 has 3 wins, distance() returns 2
def distance(player, rival, players_pool):
    return abs(wins(players_pool[player]) - wins(players_pool[rival]))

# Returning pairing for next round
def next_round(players_pool, match_round):
    matches = []

    # building all possible matches[] for a round
    for player in players_pool:
        can_play = can_play_vs(player, players_pool[player], players_pool)
        matches = matches + zip(can_play, [player for x in can_play])

    # getting rid of all duplicate matches. E.g. P1 vs P6 equals P6 vs P1
    all_matches = sorted(set([(a,b) if a<b else (b,a) for a,b in matches]))

    ranked_best = -1
    best_round = []

    for i in range(len(all_matches)):
        # To go through every possible matching, it begins the function shifts left by 1 the all_matches[] list in every i iteration 
        # For example if the list shows [1,2,3,4], the second iteration will show [2,3,4,1]
        # This ensures we get all the possible pairing for the round
        if i+1 < len(all_matches): rotate_matches = all_matches[i+1-len(all_matches):] + all_matches[:i+1]
        else: rotate_matches = all_matches
        seq=[]
        for match in rotate_matches:
            if not(any(t[0]==match[0] or t[1]==match[0] for t in seq)) and not any(t[0]==match[1] or t[1]==match[1] for t in seq): seq.append(match)
        
        # Each pairing is assigned with penalty points, which are the 'match quality', but measuring the distance() of the pair.
        # Adding up all the penalty points, we can check if this is the optimal round
        ranked_round = 0
        for l in seq:
            ranked_round = ranked_round + distance(l[0], l[1], players_pool)

        # if the round is better than a stored round, save the current round
        if (ranked_best == -1 or ranked_best > ranked_round) and len(seq) == match_round:
            ranked_best = ranked_round
            best_round = seq

    return best_round   
