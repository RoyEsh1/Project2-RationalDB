#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import algo

def connect(): 
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches(): 
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE from matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT count(*) as num from players")
    number_of_players = c.fetchone()
    DB.close()
    return number_of_players[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    # Taking care of SQL injections by using bleach module and inserting tuple
    # Every player is assigned to a unique serial number which is automatically generated
    clean_name = bleach.clean(name)
    c.execute("INSERT INTO players(name) values(%s)", (clean_name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    # Creating 'standings' list
    # Using explicit columns and not '*'' in case more data will put in 'standings' SQL table in the future
    c.execute("SELECT id, name, wins, matches from standings") 
    standings = list(c.fetchall())
    DB.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    # inserting the winner,loser into the matches database as a tuple, blocking
    c.execute("INSERT INTO matches(winner,loser) values(%s,%s)", (winner,loser))
    DB.commit()
    DB.close()

    
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()

    standings = playerStandings()
    players_pool={}
    swissPair=[]
    games_played=[]

    # Assigning pairs
    for player in standings:

        # Building dictionary of all players (players_pool), while extracting from the database player's wins and loses.
        c.execute("SELECT loser from matches where winner=%s", (player[0],))
        won_against = [i[0] for i in c.fetchall()]
        c.execute("SELECT winner from matches where loser=%s", (player[0],))
        lost_against = [i[0] for i in c.fetchall()]
        games_played = sum([[i, 1] for i in won_against], []) + sum([[i, 0] for i in lost_against], [])
        players_pool[player[0]] = games_played

    # Calculating the optimal next round using the algorithm module, and assigning names to the player IDs
    next_round = algo.next_round(players_pool,len(games_played))
    for pairing in next_round:
        name1=''.join([i[1] for i in standings if i[0] == pairing[0]])
        name2=''.join([i[1] for i in standings if i[0] == pairing[1]])
        swissPair.append((pairing[0],name1,pairing[1],name2))
        
    DB.close()
    return swissPair


