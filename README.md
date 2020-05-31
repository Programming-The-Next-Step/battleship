# Battleship
## The project
This will be a game of battleship. It's a game where two players have a (randomly computed) grid of ships and try to shoot each others' ships by guessing (link to the wiki page: https://en.wikipedia.org/wiki/Battleship_(game)). My goal is to to be able to play battleship against a computer.
If I don't have enough time I will take out the option of the player's grid, so that there is only the computer’s grid and the player tries to shoot all ships with a limited amount of shots.
If I have time left I would make an option for the player to choose the position of his or her ships on the grid. If I have a lot of time left I would upload this online and enable an option to play against a friend by sending a link, i.e. not against a random computer.
My first step will be to create the empty grids and then to create the function where the player and the computer shoot each other's ships.
## The code
To program this game I will use python. I will use the random package to create the random grids. Here are the steps and functions I will create:
1.	Make a matrix of shape 10x10, with 1:10 on the y-axis and A:J on the x-axis.
2.	The player positions his or her 7 ships. They are positioned randomly at first, and if there is enough time, the player will be able to choose the positions. There are 1x aircraft carrier (size 5), 1x battleship (size 4), 1x cruiser (size 3), 2x destroyer (size 2), and 2x submarine (size 1).
3.	The computer also positions its 7 ships. This is done randomly.
4.	The player and the computer take turns shooting at each other. This will be done by entering a row and column position. Then there will be feedback about if it was a successful shot, and if it was the player can shoot again. Otherwise the other player may shoot. There is an announcement that the entire ship is shot once this is the case, along with which ships still have to be shot.
5.	The game ends when the player or the computer has hit all of the others’ ships.
