######## Imports
import numpy as np
import pygame
import random
import sys
import time

######## The first step is to create the grid of the computer
def generate_random_position(size_ship):
    """
    This function will generate the position of a ship of a given size.

    Parameters
    ----------
    size_ship : Size of the ship whose position will be determined.

    Returns
    -------
    orientation : Vertical or horizontal.
    y_start_position : Starting point of the ship on the y-axis.
    x_start_position : Starting point of the ship on the x-axis.
    """
    orientation = random.randint(0, 1) # 0 is vertical and 1 is horizontal
    if (orientation == 0):
        y_start_position = random.randint(1, cells - size_ship)
        # 10 - size_ship so that the ship is never bigger than 10
        x_start_position = random.randint(1, cells)
    elif (orientation == 1):
        y_start_position = random.randint(1, cells)
        x_start_position = random.randint(1, cells - size_ship)
    
    return (orientation, y_start_position, x_start_position)

def check_position(grid, size_ship, orientation,
                   y_start_position,x_start_position):
    """
    This function will check if the position of the ship is valid.
    So if the area including the ship and surrounding the ship on the grid is
    still free.

    Parameters
    ----------
    grid : Grid with the boats that are already positioned.
    size_ship : Size of the ship whose position will be checked.
    orientation : Vertical or horizontal.
    y_start_position : Starting point of the ship on the y-axis.
    x_start_position : Starting point of the ship on the x-axis.

    Returns
    -------
    is_position_valid : Variable to continue or stop the while loop (if True,
    the while loop is interrupted).
    """
    
    if (orientation == 0):
        y_to_check = slice((y_start_position - 1),
                           (y_start_position + size_ship + 1), 1)
        x_to_check = slice((x_start_position - 1),
                           (x_start_position + 2), 1)
                            # + 2 instead of + 1 because of python counting
    elif (orientation == 1):
        y_to_check = slice((y_start_position - 1),
                           (y_start_position + 2), 1)
        x_to_check = slice((x_start_position - 1),
                           (x_start_position + size_ship + 1), 1)

    if np.any(grid[y_to_check, x_to_check] == 1):
        # is any part of the area surrounding the ship equal to 1?
        is_position_valid = False
    else:
        is_position_valid = True
        
    return (is_position_valid)

def position_ships(ships, size_ships):
    """
    This function will position the ships on the grid.

    Parameters
    ----------
    ships : List of the ships to be positioned.
    size_ships : List of the size of the ships to be positioned.

    Returns
    -------
    grid : The grid with the ships that the computer or the player positioned.
    """
    grid = np.zeros((12, 12))
    # with two extra columns and rows to allow the check_position function
    
    for ship in range(0, len(size_ships)):
        size_ship = size_ships[ship]
        is_position_valid = False
        while is_position_valid == False:
            # until is_position_valid is set to True, this loop continues
            orientation, y_start_position, x_start_position = generate_random_position(size_ship)
            is_position_valid = check_position(grid, size_ship, orientation,
                                               y_start_position,
                                               x_start_position)

        # once the position is valid, the current ship is added to the grid
        if (orientation == 0):
            y_to_fill = slice((y_start_position),
                              (y_start_position + size_ship), 1)
            x_to_fill = x_start_position
        elif (orientation == 1):
            y_to_fill = y_start_position
            x_to_fill = slice((x_start_position),
                              (x_start_position + size_ship), 1)
        grid[y_to_fill, x_to_fill] = 1

    grid = grid[1:11, 1:11]
    # once all ships are positioned, remove the extra columns and rows
    
    return (grid) 
    
######## Then begin the game
def shoot():
    """
    This function will initiate the game using pygame.
    First there are some settings to initiate pygame.
    Then, there is a screen with instructions, then the actual game comes on,
    and at last, there is a game over screen.
    """
    
    pygame.init() # initialize
    
    # set the screen
    windowwidth = width * cells + margin * (cells + 1)
    windowheight = height * cells + margin * (cells + 1)
    screen = pygame.display.set_mode([windowwidth * 2, windowheight * 2])
    
    bigfont = pygame.font.Font("freesansbold.ttf", 25) # font for titles
    basicfont = pygame.font.Font("freesansbold.ttf", 20) # font for texts
     
    pygame.display.set_caption("Battleship") # title
    
    explosion_img = pygame.image.load("explosion.jpg") # load image
    
    computers_grid = position_ships(ships, size_ships)
    visible_grid_for_player = np.zeros((cells, cells))
    computers_ships_uncovered = 0 # can be range(sum(size_ships))
    success = 0 # can be range(1), where 0 is not success, and 1 is success
    shots_total = 0 # can be range(cells*cells)
    
    ######## instructions ########
    done = False # loop until done = True
    display_instructions = True # loop until display_instructions = False
    instruction_page = 1
 
    while not done and display_instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN: # player clicks
                instruction_page += 1
                if instruction_page == 2:
                    display_instructions = False
                    # there is only one page for the introduction, so if the
                    # player clicks, the instructions loop is interrupted and
                    # the main game loop begins

        screen.fill(black) # set the screen background
     
        if instruction_page == 1: # give the instructions
            
            text = bigfont.render("INSTRUCTIONS", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            screen.blit(text, text_rect)
     
            text = basicfont.render("This is a solo version of the " + 
                                    "game battleship.", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 50)
            screen.blit(text, text_rect)
            
            text = basicfont.render("You have to sink the ships in as few " + 
                                    "shots as", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 90)
            screen.blit(text, text_rect)
            
            text = basicfont.render("possible. Shoot at a field by clicking ",
                                    True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 130)
            screen.blit(text, text_rect)
            
            text = basicfont.render("with your mouse. If it turns green, " + 
                                    "your shot", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 170)
            screen.blit(text, text_rect)
            
            text = basicfont.render("was successful and if it turns red, " +
                                    "your shot", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 210)
            screen.blit(text, text_rect)
            
            text = basicfont.render("was not successful.", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 250)
            screen.blit(text, text_rect)
            
            text = basicfont.render("There are the following ships: 1x " + 
                                    "aircraft", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 290)
            screen.blit(text, text_rect)
            
            text = basicfont.render("carrier (size 5), 1x battleship " + 
                                    "(size 4),", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 330)
            screen.blit(text, text_rect)
            
            text = basicfont.render("1x cruiser (size 3), 2x destroyer " +
                                    "(size 2),", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 370)
            screen.blit(text, text_rect)   
            
            text = basicfont.render("and 2x submarine (size 1).", True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 410)
            screen.blit(text, text_rect) 
            
            text = basicfont.render("Start the game by clicking anywhere.",
                                    True, white)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 450)
            screen.blit(text, text_rect)

        pygame.display.update() # update the screen
    
    ######## main loop ########
    display_main_loop = True # loop until display_main_loop = False
    while not done and display_main_loop: 
        while (computers_ships_uncovered != sum(size_ships)):
            # until there are 18 ships uncovered, this loop continues
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # player chooses coordinates that they want to shoot at
                    pos = pygame.mouse.get_pos()
                    # this gets the screen coordinates of the mouse click
                    y = pos[0] // (width + margin)
                    # this converts the screen coordinates to grid coordinates
                    x = pos[1] // (height + margin) 
                    visible_grid_for_player[y][x] = 1
                    # this sets the grid coordinates in the
                    # visible_grid_for_player equal to 1
                    if (visible_grid_for_player[y][x] == 1):
                        if (computers_grid[y][x] == 1):
                            computers_ships_uncovered += 1
                            # one more field was uncovered
                            success = 1 # the current mouse click was a success
                    shots_total += 1 # one more click
                    
            screen.fill(black) # set the screen background
            
            # draw the overview on the right side
            shots_total_surface = basicfont.render("Number of shots: " +
                                                    str(shots_total), True,
                                                    white)
            shots_total_rect = shots_total_surface.get_rect()
            shots_total_rect.topleft = (260, 20)
            screen.blit(shots_total_surface, shots_total_rect)
            
            ships_left_surface = basicfont.render("Number of fields left: " +
                                                  str(sum(size_ships) -
                                                  computers_ships_uncovered),
                                                  True, white)
            ships_left_rect = ships_left_surface.get_rect()
            ships_left_rect.topleft = (260, 60)
            screen.blit(ships_left_surface, ships_left_rect)            
         
            # draw the grid with the positions that the player chose to shoot
            for y in range(10):
                for x in range(10):
                    color = white # default is white
                    if (visible_grid_for_player[y][x] == 1) \
                        and (computers_grid[y][x] == 1):
                            # if the position that the player chose is equal
                            # to 1 on the computer's grid
                            color = green # then the shot was successful
                    elif (visible_grid_for_player[y][x] == 1) \
                        and (computers_grid[y][x] != 1):
                            # if the position that the player chose is not
                            # equal to 1 on the computer's grid
                            color = red # then the shot was unsuccessful
                    pygame.draw.rect(screen,
                                      color,
                                      [(width + margin) * y + margin,
                                      (height + margin) * x + margin,
                                      width,
                                      height])
                    
            pygame.display.update() # update the screen

            if success:
                # if the current mouse click was a success,
                # then give a small explosion image 
                explosion_img = pygame.transform.scale(
                    explosion_img, (int(300 * 0.8), int(168 * 0.8)))
                # rescale the original size to 80%
                explosion_img_rect = explosion_img.get_rect()
                explosion_img_rect.center = (255 / 2, 255 * 1.5)
                screen.blit(explosion_img, explosion_img_rect)
                pygame.display.update() # update the screen
                success = 0
                # reset the success variable, otherwise the image stays on
                
            time.sleep(0.1)
            # wait shortly so that the player can see the explosion (if the
            # shot was successful) and to slow down the game
            
        display_main_loop = False
        # if the player sank all 18 ships, the main game loop is interrupted
        # and the game over loop begins
    
    ######## game over ########
    display_game_over = True # loop until display_game_over = False
    game_over_page = 1
 
    while not done and display_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN: # player clicks
                game_over_page += 1
                if game_over_page == 3:
                    display_game_over = False
                    # there are two pages for the game over, so if the player
                    # clicks three times the game is finished

        screen.fill(black) # set the screen background
     
        if game_over_page == 1: # give a big explosion image 
            
            text = bigfont.render("GAME OVER", True, white)
            text_rect = text.get_rect()
            text_rect.center = (255, 100)
            screen.blit(text, text_rect)
            
            explosion_img = pygame.transform.scale(
                explosion_img, (int(300 * 1.5), int(168 * 1.5)))
            # rescale the original size to 150%
            explosion_img_rect = explosion_img.get_rect()
            explosion_img_rect.center = (255, 255)
            screen.blit(explosion_img, explosion_img_rect)
            
        pygame.display.update() # update the screen
            
        if game_over_page == 2: # give the number of shots the player took
            
            text = bigfont.render("GAME OVER", True, white)
            text_rect = text.get_rect()
            text_rect.center = (255, 100)
            screen.blit(text, text_rect)
     
            text = basicfont.render("You sank all of the ships with only",
                                    True, white)
            text_rect = text.get_rect()
            text_rect.center = (255, 150)
            screen.blit(text, text_rect)
            
            text = basicfont.render(str(shots_total) + " shots. " +
                                    "Congratulations!", True, white)
            text_rect = text.get_rect()
            text_rect.center = (255, 190)
            screen.blit(text, text_rect)
            
        pygame.display.update() # update the screen
    
    pygame.quit()
    sys.exit()
            
# Define colors
black = (0, 0, 0) # background
white = (255, 255, 255) # didn't check yet
green = (0, 255, 0) # success
red = (255, 0, 0) # fail
 
# Each grid cell
width = 20
height = 20
margin = 5
cells = 10

ships = ["aircraft carrier", "battleship", "cruiser", "destroyer1",
         "destroyer2", "submarine1", "submarine2"]
size_ships = [5, 4, 3, 2, 2, 1, 1]

game = shoot()   
                
