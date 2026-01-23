import pygame
from classes import *

def main():
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    puck = Puck()
    red = Player("red", puck, "standard", 0)
    blue = Player("blue", puck, "standard", 1)
    
    make_walls_goals("standard walls")

    running = True
    while running:
        clock.tick(60)
        frame += 1

        # event loop
        for event in pygame.event.get():

            # checks for escape to quit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


            if MOVEMENT_TYPE == 0:
                red.mouse_movement(event)
                blue.mouse_movement(event)
            elif MOVEMENT_TYPE == 1:
                red.touchscreen_movement(event)
                blue.touchscreen_movement(event)
            elif MOVEMENT_TYPE == 2:
                red.arcade_movement(event)
                blue.arcade_movement(event)

        if MOVEMENT_TYPE == 1:
            red.drag = red.dragging_finger is not None
            blue.drag = blue.dragging_finger is not None

        elif MOVEMENT_TYPE == 2:
            red.arcade_movement_outside_event()
            blue.arcade_movement_outside_event()
            red.drag = True
            blue.drag = True

        elif MOVEMENT_TYPE == 3:
            red.keyboard_movement()
            blue.keyboard_movement()
            red.drag = True
            blue.drag = True


        reset_games = reset_game()
        if reset_games == "red":
            del red, blue, puck
            puck = Puck("blue side")
            red = Player("red", puck, 0)
            blue = Player("blue", puck, 1)
            game_reset = True
        elif reset_games == "blue":
            del red, blue, puck
            puck = Puck("red side")
            red = Player("red", puck, 0)
            blue = Player("blue", puck, 1)
            game_reset = True
            
        
        # update classes
        red.update("standard walls")
        blue.update("standard walls")
        puck.update("standard walls")

        # calculate old positions
        red.old_x, red.old_y, blue.old_x, blue.old_y = red.x, red.y, blue.x, blue.y

        # draw
        WIN.blit(STANDARD_BG, (0,0))

        WIN.blit(PUCK_MODEL, (puck.x, puck.y))
        WIN.blit(RED_MODEL, (red.x, red.y))
        WIN.blit(BLUE_MODEL, (blue.x, blue.y))
        print_score("standard")

        pygame.display.update()

        if frame == 1:
            countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y)
        if game_reset:
            countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y)
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main()