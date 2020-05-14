#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:16:43 2020

@author: carolinstreitberger
"""
import numpy as np
import random

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
    print(grid[y_to_check, x_to_check])
    print("If these are all zeros then they will be added to the grid. Otherwise new positions will be generated")
    
    if np.any(grid[y_to_check, x_to_check] == 1):
        is_position_valid = False
    else:
        is_position_valid = True
        
    return (is_position_valid)
            
def position_ships(grid, ships, size_ships):
    """
    This function should add the ships to the grid if the position is valid.

    Parameters
    ----------
    grid : TYPE
        The grid with the boats that are already positioned.
    ships :  TYPE
        List of the ships to be positioned.
    size_ships : TYPE
        List of the size of the ships to be positioned.

    Returns
    -------
    grid : TYPE
        The grid with the boats that are already positioned including the current ship.
    """
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
        # I have the list of ships below, but I don't use and maybe it would be helpful later to be able to call the ship by the name
        print("Current grid:")
        print(grid)
    
    # Now remove the first and last columns and rows because they were only included to allow the check_position function
    grid = grid[1:11, 1:11]
    print("Final grid:")
    print(grid)
    
    return (grid)

ships = ("aircraft carrier", "battleship", "cruiser", "destroyer1", "destroyer2", "submarine1", "submarine2")
size_ships = (5, 4, 3, 2, 2, 1, 1)
initial_grid = np.zeros((12, 12)) # 0 and 11 are just there to allow the check_position function
computer_grid = position_ships(initial_grid, ships, size_ships)
