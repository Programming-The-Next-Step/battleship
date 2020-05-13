#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:16:43 2020

@author: carolinstreitberger
"""
import numpy as np
import random
ships = ("aircraft carrier", "battleship", "cruiser", "destroyer1", "destroyer2", "submarine1", "submarine2")
size_ships = (5, 4, 3, 2, 2, 1, 1)
grid = np.zeros((10, 10)) #0:9
def position_ships():
    """
    This function should randomly create a ships, and check if their position is valid,
    so if it's not too big for the grid, if all spots are free,
    and if the neighbouring spots are free.
    If it passes all tests, the is_position_valid variable should be set to True, 
    and the ship should be added to the grid. Then the same thing happens for the next ship.

    Returns
    -------
    grid : this will be the grid with seven ships

    """
    for ship in range(0, len(ships)):
        ## Randomly position the ships
        is_position_valid = False
        while is_position_valid == False: # until is_position_valid is set to True, this loop continues
            print("Testing: starting the while loop")
            x_start_position = random.randrange(0, 9, 1) # randrange is exclusive, ie 10 is never selected
            y_start_position = random.randrange(0, 9, 1)
            orientation = random.randrange(0, 2, 1) # 0 is vertical and 1 is horizontal orientation
            
            # Define the ships coordinates
            if orientation == 0:
                x_end_position = x_start_position
                y_end_position = y_start_position + size_ships[ship]
            elif orientation == 1:
                x_end_position = x_start_position + size_ships[ship]
                y_end_position = y_start_position
            print("Testing:", x_start_position, x_end_position, y_start_position, y_end_position)       
        
            # FIRST TEST: Is the end position outside of the grid?
            if (x_end_position > 9) or (y_end_position > 9):
                continue # if the end positions are outside of the grid, it jumps back to the beginning of the while loop
            
            # SECOND TEST: Is the position of each part of the ship still free?
            if orientation == 0:
                print("Testing: orientation = 0")
                for coordinate in range(0, size_ships[ship]):
                    print("Testing: coordinate i is", coordinate)
                    if grid[y_start_position + coordinate, x_start_position] != 0:
                        print("Testing: continue statement")
                #continue
                # if I place the continue here, it jumps to the beginning of the while loop
                # I only want this in case the condition of the if statement is true
                # I don't want to do this if the condition is false
                        
            elif orientation == 1:
                print("Testing: orientation = 1")
                for coordinate in range(0, size_ships[ship]):
                    print("Testing: coordinate i is", coordinate)
                    if grid[y_start_position, x_start_position + coordinate] != 0:
                        print("Testing: continue statement")
                #continue
                # same question as before
                
            print("Testing: you should see this if true. You shouldn't see this if false")
            
            # THIRD TEST: Is the ship next to any other ships?
            if orientation == 0: # is the ship vertical?
                for coordinate in range(0, size_ships[ship]):
                    if x_start_position == 0: # is the ship bordering the left?
                        if y_start_position == 0 \ # is the ship bordering the top?
                        and grid[y_start_position + coordinate, x_start_position + 1] != 0 \
                        or grid[y_end_position + 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        elif y_end_position == 9 \ # is the ship bordering the bottom?
                        and grid[y_start_position + coordinate, x_start_position + 1] != 0 \
                        or grid[y_start_position - 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        else \ # is the ship not bordering the top or bottom?
                        and grid[y_start_position + coordinate, x_start_position + 1] != 0 \
                        or grid[y_end_position + 1, x_start_position] != 0 \
                        or grid[y_start_position - 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                                
                    elif x_start_position == 9: # is the ship bordering the right?
                        if y_start_position == 0 \ # is the ship bordering the top?
                        and grid[y_start_position + coordinate, x_start_position - 1] != 0 \
                        or grid[y_end_position + 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        elif y_end_position == 9 \ # is the ship bordering the bottom?
                        and grid[y_start_position + coordinate, x_start_position - 1] != 0 \
                        or grid[y_start_position - 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        else: # is the ship not bordering the top or bottom?
                        and grid[y_start_position + coordinate, x_start_position - 1] != 0 \
                        or grid[y_end_position + 1, x_start_position] != 0 \
                        or grid[y_start_position - 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                                
                    else: # is the ship not bordering the left or right? 
                        if y_start_position == 0 \ # is the ship bordering the top?
                        and grid[y_start_position + coordinate, x_start_position + 1] != 0 \
                        or grid[y_start_position + coordinate, x_start_position - 1] != 0 \
                        or grid[y_end_position + 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        elif y_end_position == 9 \ # is the ship bordering the bottom?
                        and grid[y_start_position + coordinate, x_start_position + 1] != 0 \
                        or grid[y_start_position + coordinate, x_start_position - 1] != 0 \
                        or grid[y_start_position - 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        else \ # is the ship not bordering the top or bottom? 
                        and grid[y_start_position + coordinate, x_start_position + 1] != 0 \
                        or grid[y_start_position + coordinate, x_start_position - 1] != 0 \
                        or grid[y_end_position + 1, x_start_position] != 0 \
                        or grid[y_start_position - 1, x_start_position] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                                
            elif orientation == 1: # is the ship horizontal?
                for coordinate in range(0, size_ships[ship]): 
                    if x_start_position == 0: # is the ship bordering the left?
                        if y_start_position == 0 \ # is the ship bordering the top?
                        and grid[y_start_position + 1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_end_position + 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        elif y_end_position == 9 \ # is the ship bordering the bottom?
                        and grid[y_start_position - 1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_end_position + 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        else \ # is the ship not bordering the top or bottom?
                        and grid[y_start_position + 1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position -1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_end_position + 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                                
                    elif x_end_position == 9: # is the ship bordering the right?
                        if y_start_position == 0 \ # is the ship bordering the top?
                        and grid[y_start_position + 1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_start_position - 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        elif y_end_position == 9 \ # is the ship bordering the bottom?
                        and grid[y_start_position -1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_start_position - 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break  
                        else \ # is the ship not bordering the top or bottom?
                        and grid[y_start_position + 1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position -1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_start_position - 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                                
                    else: # is the ship not bordering the left or right? 
                        if y_start_position == 0 \ # is the ship bordering the top?
                        and grid[y_start_position + 1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_end_position + 1] != 0 \
                        or grid[y_start_position, x_start_position - 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        elif y_end_position == 9 \ # is the ship bordering the bottom?
                        and grid[y_start_position -1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_end_position + 1] != 0 \
                        or grid[y_start_position, x_start_position - 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
                        else \ # is the ship not bordering the top or bottom? 
                        and grid[y_start_position + 1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position -1, x_start_position + coordinate] != 0 \
                        or grid[y_start_position, x_end_position + 1] != 0 \
                        or grid[y_start_position, x_start_position - 1] != 0:
                            #is_position_valid = False
                            #continue
                            #break
            
            # If it passed all these tests it's valid and can be added to the grid          
            is_position_valid = True
        
        for coordinate in range(0, size_ships[ship]):
                if orientation == 0:
                    grid[y_start_position + coordinate, x_start_position] = 1
                elif orientation == 1:
                    grid[y_start_position, x_start_position + coordinate] = 1
            
        print(grid)
        print(x_start_position, x_end_position, y_start_position, y_end_position)
    
    return grid