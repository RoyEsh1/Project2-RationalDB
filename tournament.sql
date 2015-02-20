-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE players ( id SERIAL primary key,
                       name TEXT);

-- the matches table store games, as id of players - it's connected to the players.id primary key
CREATE TABLE matches ( winner INT references players,
					   loser INT references players);

-- Creating winning games VIEW of a player
CREATE VIEW games_won as 
	select p.id, p.name, count(m.winner) ng
    from players p left join matches m
    on p.id=m.winner
    group by p.id, p.name;

-- Creating losing games VIEW of a player
CREATE VIEW games_lost as 
	select p.id, p.name, count(m.loser) as ng
    from players p left join matches m 
    on p.id=m.loser
    group by p.id, p.name;

-- Creating the standings VIEW, using both games_lost and games_won VIEWs
CREATE VIEW standings as 
    select w.id, w.name, w.ng as wins, w.ng+l.ng as matches 
    from games_won w INNER JOIN games_lost l 
    on w.id=l.id
    order by wins desc;

