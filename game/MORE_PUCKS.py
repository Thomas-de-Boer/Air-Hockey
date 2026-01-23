import pygame
from classes import *

def main():
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    puck1 = Puck("red ffo")
    puck2 = Puck("green ffo")
    puck3 = Puck()
    puck4 = Puck("blue ffo")
    puck5 = Puck("yellow ffo")
    puck6 = Puck("db 1")
    puck7 = Puck("db 2")
    puck8 = Puck("red side")
    puck9 = Puck("blue side")
    red = Player("red", puck1, "standard", 0, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
    blue = Player("blue", puck1, "standard", 1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
    
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
            del red, blue, puck1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9
            puck1 = Puck("blue ffo")
            puck2 = Puck("yellow ffo")
            puck3 = Puck()
            puck4 = Puck("red ffo")
            puck5 = Puck("green ffo")
            puck6 = Puck("db 1")
            puck7 = Puck("db 2")
            puck8 = Puck("red side")
            puck9 = Puck("blue side")
            red = Player("red", puck1, "standard", 0, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            blue = Player("blue", puck1, "standard", 1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            game_reset = True
        elif reset_games == "blue":
            del red, blue, puck1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9
            puck1 = Puck("blue ffo")
            puck2 = Puck("yellow ffo")
            puck3 = Puck()
            puck4 = Puck("red ffo")
            puck5 = Puck("green ffo")
            puck6 = Puck("db 1")
            puck7 = Puck("db 2")
            puck8 = Puck("red side")
            puck9 = Puck("blue side")
            red = Player("red", puck1, "standard", 0, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            blue = Player("blue", puck1, "standard", 1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            game_reset = True
            
        
        # update classes
        red.update("standard walls")
        blue.update("standard walls")
        puck1.update("standard walls")
        puck2.update("standard walls")
        puck3.update("standard walls")
        puck4.update("standard walls")
        puck5.update("standard walls")
        puck6.update("standard walls")
        puck7.update("standard walls")
        puck8.update("standard walls")
        puck9.update("standard walls")

        pucks = [puck1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9]
        for puck in pucks:
            puck1.other_puck_collisions(puck)
            puck2.other_puck_collisions(puck)
            puck3.other_puck_collisions(puck)
            puck4.other_puck_collisions(puck)
            puck5.other_puck_collisions(puck)
            puck6.other_puck_collisions(puck)
            puck7.other_puck_collisions(puck)
            puck8.other_puck_collisions(puck)
            puck9.other_puck_collisions(puck)
        

        # calculate old positions
        red.old_x, red.old_y, blue.old_x, blue.old_y = red.x, red.y, blue.x, blue.y

        # draw
        WIN.blit(STANDARD_BG, (0,0))

        WIN.blit(PUCK_MODEL, (puck1.x, puck1.y))
        WIN.blit(PUCK_MODEL, (puck2.x, puck2.y))
        WIN.blit(PUCK_MODEL, (puck3.x, puck3.y))
        WIN.blit(PUCK_MODEL, (puck4.x, puck4.y))
        WIN.blit(PUCK_MODEL, (puck5.x, puck5.y))
        WIN.blit(PUCK_MODEL, (puck6.x, puck6.y))
        WIN.blit(PUCK_MODEL, (puck7.x, puck7.y))
        WIN.blit(PUCK_MODEL, (puck8.x, puck8.y))
        WIN.blit(PUCK_MODEL, (puck9.x, puck9.y))
        WIN.blit(RED_MODEL, (red.x, red.y))
        WIN.blit(BLUE_MODEL, (blue.x, blue.y))
        print_score("standard")

        pygame.display.update()

        if frame == 1:
            countdown_start(red.x, red.y, blue.x, blue.y, puck1.x, puck1.y, "standard", "more", puck2.x, puck2.y, puck3.x, puck3.y, puck4.x, puck4.y, puck5.x, puck5.y, puck6.x, puck6.y, puck7.x, puck7.y, puck8.x, puck8.y, puck9.x, puck9.y)
        if game_reset:
            countdown_start(red.x, red.y, blue.x, blue.y, puck1.x, puck1.y, "standard", "more", puck2.x, puck2.y, puck3.x, puck3.y, puck4.x, puck4.y, puck5.x, puck5.y, puck6.x, puck6.y, puck7.x, puck7.y, puck8.x, puck8.y, puck9.x, puck9.y)
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main()