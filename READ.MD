Project 2 Rational Database

A Swiss-system tournament is a tournament which uses a non-elimination format. 
There are several rounds of competition, so each competitor (team or individual) does not play every other competitor. 
Competitors meet one-to-one, where each round can end only in win/lose.
The pairing is being done by strength, so the strongest players will play against each other, and weakest player will play
among themselves.

This project is an engine that calcuates the competitors pairing.
It does so by ensuring an optimal match between any number of competitors at any round.

Written in Python and PostgreSQL.

Files:
tournament.sql: creating the SQL tables and VIEWs, to be used to store the players info
algo.py: the matching algorithm
tournament.py: contains all the functions to swiss pairing. Please look inside the file for further 
              comments and explanations.

Installation notes:
In order to run it smoothly, you'll need 
1. PostgreSQL server installed
2. Python Bleach library package (can be found here - http://pypi.python.org/pypi/bleach)

Install:
1. Copy all files to the same directory
2. Create tournament database and run 'tournament.sql' to setup the SQL program environment
3. Run 'tournament_test.py' to check everything works properly
4. You can now import 'tournament.py' into your program

(c) 2015
