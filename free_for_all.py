
import pygame
from classes import *

def main():
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    puck = Puck()
    red = Player("red", puck, "freeforall")
    blue = Player("blue", puck, "freeforall")
    green = Player("green", puck, "freeforall")
    yellow = Player("yellow", puck, "freeforall")
    
    make_walls_goals("freeforall walls", "freeforall")

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
                green.mouse_movement(event)
                yellow.mouse_movement(event)
            elif MOVEMENT_TYPE == 1:
                red.touchscreen_movement(event)
                blue.touchscreen_movement(event)
                green.touchscreen_movement(event)
                yellow.touchscreen_movement(event)

        if MOVEMENT_TYPE == 1:
            red.drag = red.dragging_finger is not None
            blue.drag = blue.dragging_finger is not None
            green.drag = green.dragging_finger is not None
            yellow.drag = yellow.dragging_finger is not None


        reset_games = reset_game()
        if reset_games == "red":
            del red, blue, puck
            puck = Puck("blue side")
            red = Player("red", puck, "freeforall")
            blue = Player("blue", puck, "freeforall")
            green = Player("green", puck, "freeforall")
            yellow = Player("yellow", puck, "freeforall")
            game_reset = True
        elif reset_games == "blue":
            del red, blue, puck
            puck = Puck("red side")
            red = Player("red", puck, "freeforall")
            blue = Player("blue", puck, "freeforall")
            green = Player("green", puck, "freeforall")
            yellow = Player("yellow", puck, "freeforall")
            game_reset = True
            
        
        # update classes
        red.update("freeforall walls")
        blue.update("freeforall walls")
        green.update("freeforall walls")
        yellow.update("freeforall walls")
        puck.update("freeforall walls", "freeforall")

        # calculate old positions
        red.old_x, red.old_y, blue.old_x, blue.old_y = red.x, red.y, blue.x, blue.y
        green.old_x, green.old_y, yellow.old_x, yellow.old_y = green.x, green.y, yellow.x, yellow.y

        # draw
        WIN.blit(FREEFORALL_BG, (0,0))

        WIN.blit(PUCK_MODEL, (puck.x, puck.y))
        WIN.blit(RED_MODEL, (red.x, red.y))
        WIN.blit(BLUE_MODEL, (blue.x, blue.y))
        WIN.blit(GREEN_MODEL, (green.x, green.y))
        WIN.blit(YELLOW_MODEL, (yellow.x, yellow.y))
        
        print_score("freeforall")

        pygame.display.update()

        if frame == 1:
            countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "freeforall", green.x, green.y, yellow.x, yellow.y, "freeforall")
        if game_reset:
            countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "freeforall", green.x, green.y, yellow.x, yellow.y, "freeforall")
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main()