#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:16:43 2020

@author: carolinstreitberger
"""
######## Imports
import numpy as np
import random

######## The first step is to create the grid of the computer
def generate_random_position(size_ship):
    """
    This function will generate the position of a ship of a given size.

    Parameters
    ----------
    size_ship : TYPE #?
        Size of the ship whose position will be determined.

    Returns
    -------
    orientation : TYPE
        Vertical or horizontal.
    y_start_position : TYPE
        Starting point of the ship on the y-axis.
    x_start_position : TYPE
        Starting point of the ship on the x-axis.
    """
    orientation = random.randrange(0, 2, 1) # 0 is vertical and 1 is horizontal orientation
    if (orientation == 0):
        y_start_position = random.randrange(1, 11 - size_ship, 1)
        # 11 - size_ship so that the ship is never bigger than 10
        x_start_position = random.randrange(1, 11, 1)
        # randrange is exclusive, ie 10 is never selected
        # randrange is from 1 to 11 (so any number between 1 and 10) because 0 and 11 will be deleted later
    elif (orientation == 1):
        y_start_position = random.randrange(1, 11, 1)
        x_start_position = random.randrange(1, 11 - size_ship, 1)
    
    return (orientation, y_start_position, x_start_position)

def check_position(grid, size_ship, orientation, y_start_position, x_start_position):
    """
    This function will check if the position of the ship is valid.
    So if the area including the ship and surrounding the ship on the grid is still free.

    Parameters
    ----------
    grid : TYPE
        The grid with the boats that are already positioned.
    size_ship : TYPE
        Size of the ship whose position will be checked.
    orientation : TYPE
        Vertical or horizontal.
    y_start_position : TYPE
        Starting point of the ship on the y-axis.
    x_start_position : TYPE
        Starting point of the ship on the x-axis.

    Returns
    -------
    is_position_valid : TYPE
        Variable to continue or stop the while loop (if True, the while loop is interrupted).
    """
    
    if (orientation == 0):
        y_to_check = slice((y_start_position - 1), (y_start_position + size_ship + 1), 1)
        x_to_check = slice((x_start_position - 1), (x_start_position + 2), 1) # + 2 instead of + 1 because of python counting
    elif (orientation == 1):
        y_to_check = slice((y_start_position - 1), (y_start_position + 2), 1)
        x_to_check = slice((x_start_position - 1), (x_start_position + size_ship + 1), 1)
    
    print("Part of the grid to be checked")
    # remove these three print statements because they are dumb in the position_players_ships
    print(grid[y_to_check, x_to_check])
    print("If these are all zeros then they will be added to the grid. Otherwise new positions will be generated")
    
    if np.any(grid[y_to_check, x_to_check] == 1):
        is_position_valid = False
    else:
        is_position_valid = True
        
    return (is_position_valid)
            
def position_computers_ships(ships, size_ships):
    """
    This function should add the ships to the computer's grid if the position is valid.

    Parameters
    ----------
    ships :  TYPE
        List of the ships to be positioned.
    size_ships : TYPE
        List of the size of the ships to be positioned.

    Returns
    -------
    grid : TYPE
        The grid with the boats that are already positioned including the current ship.
    """
    grid = np.zeros((12, 12))
    for ship in range(0, len(size_ships)):
        # Randomly position the ships
        size_ship = size_ships[ship]
        is_position_valid = False
        while is_position_valid == False: # until is_position_valid is set to True, this loop continues
            orientation, y_start_position, x_start_position = generate_random_position(size_ship)
            is_position_valid = check_position(grid, size_ship, orientation, y_start_position, x_start_position)
        
        # Once the position is valid, the grid is filled with the current ship
        if (orientation == 0):
            y_to_fill = slice((y_start_position), (y_start_position + size_ship), 1)
            x_to_fill = x_start_position
        elif (orientation == 1):
            y_to_fill = y_start_position
            x_to_fill = slice((x_start_position), (x_start_position + size_ship), 1)
        
        grid[y_to_fill, x_to_fill] = 1
        # Is there a way to name the ship that I'm currently using?
        print("The", ships[ship], "was just placed")
        print("Current grid:")
        print(grid)
    
    # Now remove the first and last columns and rows because they were only included to allow the check_position function
    grid = grid[1:11, 1:11]
    print("Final grid:")
    print(grid)
    
    return (grid)

######## Then create the player's grid
def position_players_ships(ships, size_ships):
    """
    This function should position the ships that the player chooses to the player's grid.

    Parameters
    ----------
    ships : TYPE
        List of the ships to be positioned.
    size_ships : TYPE
        List of the size of the ships to be positioned.

    Returns
    -------
    grid : TYPE
        The grid with the ships that the player positioned.

    """
    grid = np.zeros((12, 12))
    for ship in range(0, len(size_ships)):
        size_ship = size_ships[ship]
        print("You now have to place the", ships[ship], "which has the size", size_ship)
        is_position_valid = False
        while is_position_valid == False: # until is_position_valid is set to True, this loop continues
            orientation = int(input("Enter which orientation you want your ship to have (0 is vertical and 1 is horizontal): "))
            y_start_position = int(input("Enter at which row you want your ship to start (a value between 1 and 10):"))
            x_start_position = int(input("Enter at which column you want your ship to start (a value between 1 and 10):"))
            is_position_valid = check_position(grid, size_ship, orientation, y_start_position, x_start_position)
            print("You cannot place this ship here. Enter a new position")
        
        # Once the position is valid, the grid is filled with the current ship
        if (orientation == 0):
            y_to_fill = slice((y_start_position), (y_start_position + size_ship), 1)
            x_to_fill = x_start_position
        elif (orientation == 1):
            y_to_fill = y_start_position
            x_to_fill = slice((x_start_position), (x_start_position + size_ship), 1)
        
        grid[y_to_fill, x_to_fill] = 1
        # Is there a way to name the ship that I'm currently using?
        print("You just placed the", ships[ship])
        print("Current grid:")
        print(grid)
    
    # Now remove the first and last columns and rows because they were only included to allow the check_position function
    grid = grid[1:11, 1:11]
    print("Final grid:")
    print(grid)
    
    return (grid)

######## Then the player and the computer take turns at shooting each other
def players_shot(visible_grid_for_player, computers_ships_uncovered):
    """
    This function should allow the player and the computer to shoot at each other.

    Parameters
    ----------
    visible_grid_for_player : TYPE
        DESCRIPTION.
    computers_ships_uncovered : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    guess_y = int(input("Enter which row you want to shoot at (a value between 0 and 9): "))
    guess_x = int(input("Enter which column you want to shoot at (a value between 0 and 9): "))
    
    if visible_grid_for_player[guess_y, guess_x] != 0:
        print("This point is not unknown. Please choose an unknown point")
        players_turn = True
        
        return(players_turn, visible_grid_for_player, computers_ships_uncovered) # start over
    
    elif visible_grid_for_player[guess_y, guess_x] == 0:
        visible_grid_for_player[guess_y, guess_x] = 999
        print("This is the position you selected:")
        print(visible_grid_for_player)
        
        # confirm = input("Enter 'yes' to confirm, enter 'no' to enter new input")
        # if (confirm == "yes"):
        #     break
        # elif (confirm == "no"):
        #     players_turn = True
        # return(players_turn, visible_grid_for_player) # start over
    
    if (computers_grid[guess_y, guess_x] == 1):
        visible_grid_for_player[guess_y, guess_x] = 1
        print("Your shot was succesful. This is the computer's grid currently visible to you:")
        print(visible_grid_for_player)
        computers_ships_uncovered.append(True)
        
        players_turn = True
        
    elif (computers_grid[guess_y, guess_x] != 1):
        visible_grid_for_player[guess_y, guess_x] = 2
        print("Your shot was unsuccesful. This is the computer's grid currently visible to you:")
        print(visible_grid_for_player)
        
        players_turn = False
        
    return(players_turn, visible_grid_for_player, computers_ships_uncovered)

def computers_shot(visible_grid_for_computer, players_ships_uncovered):
    guess_y = random.randrange(0, 10, 1)
    guess_x = random.randrange(0, 10, 1)
    
    if visible_grid_for_computer[guess_y, guess_x] != 0:
        
        players_turn = False
        
        return(players_turn, visible_grid_for_computer) # computer will start over
    
    if (players_grid[guess_y, guess_x] == 1):
        print("The computer's shot was succesful.")
        visible_grid_for_computer[guess_y, guess_x] = 1
        players_ships_uncovered.append(True)
        
        players_turn = False # computer has another go
        
    elif (players_grid[guess_y, guess_x] != 1):
        print("The computer's shot was unsuccesful.")
        visible_grid_for_computer[guess_y, guess_x] = 2
        
        players_turn = True # computer missed, so it's the player's turn
        
    return(players_turn, visible_grid_for_computer, players_ships_uncovered)

def shoot(computers_grid, players_grid):
    visible_grid_for_player = np.zeros((10, 10))
    visible_grid_for_computer = np.zeros((10, 10))
    players_ships_uncovered = list()
    computers_ships_uncovered = list()

    # 0 is unknown; 1 is successful shot; 2 is unsuccesful shot; 999 is current selection
    while (len(players_ships_uncovered) != 18 or len(computers_ships_uncovered) != 18): # until either is a list with 18 items, this loop continues
    # right now the problem is that the loop doesnt stop once it's sucessful because it first has to break out of the loops below
        players_turn = True
        
        while players_turn == True:
            print("It is your turn.")
            players_turn, visible_grid_for_player, computers_ships_uncovered = players_shot(visible_grid_for_player, computers_ships_uncovered)
            
        while players_turn == False:
            print("It is the computer's turn.")
            players_turn, visible_grid_for_computer, players_ships_uncovered = computers_shot(visible_grid_for_computer, players_ships_uncovered)
            
    if (len(players_ships_uncovered) == 18):
        print("The computer won")
        print("Your grid:")
        print(players_grid)
        print("and the grid visible to the computer:")
        print(visible_grid_for_computer)
        
        return ("Good luck next time.")
        
    elif (len(computers_ships_uncovered) == 18):
        print("You won")
        print("The computer's grid':")
        print(computers_grid)
        print("and what's visible to you':")
        print(visible_grid_for_player)
        
        return ("Congratulations.")

######## Run the functions
ships = ["aircraft carrier", "battleship", "cruiser", "destroyer1", "destroyer2", "submarine1", "submarine2"]
size_ships = [5, 4, 3, 2, 2, 1, 1]
computers_grid = position_computers_ships(ships, size_ships)
players_grid = position_players_ships(ships, size_ships) 
game = shoot(computers_grid, players_grid)
    
        
        
            
