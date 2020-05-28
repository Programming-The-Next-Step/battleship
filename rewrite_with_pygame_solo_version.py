#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 05:15:43 2020

@author: carolinstreitberger
"""
######## Imports
import numpy as np
import pygame
import sys
import random
# from pygame.locals import * # not sure if I need this

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
    orientation = random.randint(0, 1) # 0 is vertical and 1 is horizontal orientation
    if (orientation == 0):
        y_start_position = random.randint(1, CELLS - size_ship)
        # 10 - size_ship so that the whole ship is never bigger than 10
        x_start_position = random.randint(1, CELLS)
    elif (orientation == 1):
        y_start_position = random.randint(1, CELLS)
        x_start_position = random.randint(1, CELLS - size_ship)
    
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

    if np.any(grid[y_to_check, x_to_check] == 1): # if any part of the area surrounding the ship is equal to 1 
        is_position_valid = False # it won't be added
    else:
        is_position_valid = True # it will be added
        
    return (is_position_valid)

def position_ships(ships, size_ships, user):
    """
    This function should position the ships of the computer or the player.
    The ones of the computer are chosen at random and the player chooses their own.

    Parameters
    ----------
    ships : TYPE
        List of the ships to be positioned.
    size_ships : TYPE
        List of the size of the ships to be positioned.
    user : TYPE
        Can be "computer" or "player".

    Returns
    -------
    grid : TYPE
        The grid with the ships that the computer or the player positioned.
    """
    grid = np.zeros((12, 12))
    
    for ship in range(0, len(size_ships)):
        size_ship = size_ships[ship]
        is_position_valid = False
        while is_position_valid == False: # until is_position_valid is set to True, this loop continues
            if (user == "computer"):
                orientation, y_start_position, x_start_position = generate_random_position(size_ship)
                is_position_valid = check_position(grid, size_ship, orientation, y_start_position, x_start_position)
            elif (user == "player"):
                print("You now have to place the", ships[ship], "which has the size", size_ship)
                orientation = int(input("Enter which orientation you want your ship to have (0 is vertical and 1 is horizontal): "))
                y_start_position = int(input("Enter at which row you want your ship to start (a value between 1 and 10):"))
                x_start_position = int(input("Enter at which column you want your ship to start (a value between 1 and 10):"))
                is_position_valid = check_position(grid, size_ship, orientation, y_start_position, x_start_position)
                if (is_position_valid == False):
                    print("You cannot place this ship here. Enter a new position")
                
        # Once the position is valid, the grid is filled with the current ship
        if (orientation == 0):
            y_to_fill = slice((y_start_position), (y_start_position + size_ship), 1)
            x_to_fill = x_start_position
        elif (orientation == 1):
            y_to_fill = y_start_position
            x_to_fill = slice((x_start_position), (x_start_position + size_ship), 1)
        
        grid[y_to_fill, x_to_fill] = 1

    # Now remove the first and last columns and rows because they were only included to allow the check_position function
    grid = grid[1:11, 1:11]
    
    return (grid) 
    
######## Then begin the game
def shoot():
    
    pygame.init() # initialize
    # Screen
    WINDOWWIDTH = WIDTH*CELLS + MARGIN*(CELLS + 1)
    WINDOWHEIGHT = HEIGHT*CELLS + MARGIN*(CELLS + 1)
    screen = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
     
    pygame.display.set_caption("Battleship") # title
    
    computers_grid = position_ships(ships, size_ships, "computer")
    computers_ships_uncovered = counter = 0
    visible_grid_for_player = np.zeros((CELLS, CELLS))
    
    # start the game
    done = False # loop until done = True
    while not done:
        while (computers_ships_uncovered < sum(size_ships)): # until either is a list with 18 items, this loop continues
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN: # player chooses coordinates that they want to shoot at
                    pos = pygame.mouse.get_pos() # get the screen coordinates of the mouse press
                    y = pos[0] // (WIDTH + MARGIN) # convert the screen coordinates to grid coordinates
                    x = pos[1] // (HEIGHT + MARGIN) 
                    
                    visible_grid_for_player[y][x] = 1 # set the grid coordinates in the visible_grid_for_player equal to 1
                    if (visible_grid_for_player[y][x] == 1) and (computers_grid[y][x] == 1):
                        computers_ships_uncovered += 1
                    counter += 1
                    
            screen.fill(BLACK) # set the screen background
         
            # draw the grid with the positions that the player chose to shoot at
            for y in range(10):
                for x in range(10):
                    color = WHITE # default is white
                    if (visible_grid_for_player[y][x] == 1) and (computers_grid[y][x] == 1): # if the position that the player chose is equal to 1 on the computer's grid
                        color = GREEN # then the shot was successful
                    elif (visible_grid_for_player[y][x] == 1) and (computers_grid[y][x] != 1): # if the position that the player chose is not equal to 1 on the computer's grid
                        color = RED # then the shot was unsuccessful
                    pygame.draw.rect(screen,
                                      color,
                                      [(MARGIN + WIDTH) * y + MARGIN,
                                      (MARGIN + HEIGHT) * x + MARGIN,
                                      WIDTH,
                                      HEIGHT])

            pygame.display.update() # update
            FPSCLOCK = pygame.time.Clock()
            FPSCLOCK.tick(FPS)
            
        done = True  # if it ran through all these while loops, the game is finished
    
    # # Show a screen at end of game
    # while True:
    #     BIGFONT = pygame.font.Font('freesansbold.ttf', 50)
        
    #     screen.fill(BLACK)
        
    #     title = BIGFONT.render('Congrats! Puzzle solved in:', True, WHITE)
    #     titleRect = title.get_rect()
    #     titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    #     screen.blit(title, titleRect)
        
    #     title = BIGFONT.render((str(counter) + ' shots'), True, WHITE)
    #     titleRect = title.get_rect()
    #     titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 + 50))
    #     screen.blit(title, titleRect)  
        
    #     pygame.display.update()
    #     FPSCLOCK.tick(FPS)
        
    pygame.quit()
    sys.exit()
            
######## Run the functions
# Define colors
BLACK = (0, 0, 0) # background
WHITE = (255, 255, 255) # didn't check yet
GREEN = (0, 255, 0) # success
RED = (255, 0, 0) # fail
 
# Each grid cell
WIDTH = 20
HEIGHT = 20
MARGIN = 5
CELLS = 10

FPS = 30 # Number of frames per second

ships = ["aircraft carrier", "battleship", "cruiser", "destroyer1", "destroyer2", "submarine1", "submarine2"]
size_ships = [5, 4, 3, 2, 2, 1, 1]

game = shoot()   
                
