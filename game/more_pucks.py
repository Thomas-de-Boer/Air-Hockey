import pygame
import classes as c

def main(point_amount):
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    c.reset_scores()

    puck1 = c.Puck("red ffo")
    puck2 = c.Puck("green ffo")
    puck3 = c.Puck()
    puck4 = c.Puck("blue ffo")
    puck5 = c.Puck("yellow ffo")
    puck6 = c.Puck("db 1")
    puck7 = c.Puck("db 2")
    puck8 = c.Puck("red side")
    puck9 = c.Puck("blue side")
    red = c.Player("red", puck1, "standard", 0, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
    blue = c.Player("blue", puck1, "standard", 1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
    
    pucks = [puck1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9]
    
    c.make_walls_goals("standard walls")

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
                    return


            if c.MOVEMENT_TYPE == 0:
                red.mouse_movement(event)
                blue.mouse_movement(event)
            elif c.MOVEMENT_TYPE == 1:
                red.touchscreen_movement(event)
                blue.touchscreen_movement(event)
            elif c.MOVEMENT_TYPE == 2:
                red.arcade_movement(event)
                blue.arcade_movement(event)

        if c.MOVEMENT_TYPE == 1:
            red.drag = red.dragging_finger is not None
            blue.drag = blue.dragging_finger is not None

        elif c.MOVEMENT_TYPE == 2:
            red.arcade_movement_outside_event()
            blue.arcade_movement_outside_event()
            red.drag = True
            blue.drag = True

        elif c.MOVEMENT_TYPE == 3:
            red.keyboard_movement()
            blue.keyboard_movement()
            red.drag = True
            blue.drag = True

        if c.red_score >= point_amount:
            c.anounce_winner("red")
            return
        elif c.blue_score >= point_amount:
            c.anounce_winner("blue")
            return

        reset_games = c.reset_game()
        if reset_games == "red":
            del red, blue, puck1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9
            puck1 = c.Puck("blue ffo")
            puck2 = c.Puck("yellow ffo")
            puck3 = c.Puck()
            puck4 = c.Puck("red ffo")
            puck5 = c.Puck("green ffo")
            puck6 = c.Puck("db 1")
            puck7 = c.Puck("db 2")
            puck8 = c.Puck("red side")
            puck9 = c.Puck("blue side")
            red = c.Player("red", puck1, "standard", 0, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            blue = c.Player("blue", puck1, "standard", 1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            game_reset = True
        elif reset_games == "blue":
            del red, blue, puck1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9
            puck1 = c.Puck("blue ffo")
            puck2 = c.Puck("yellow ffo")
            puck3 = c.Puck()
            puck4 = c.Puck("red ffo")
            puck5 = c.Puck("green ffo")
            puck6 = c.Puck("db 1")
            puck7 = c.Puck("db 2")
            puck8 = c.Puck("red side")
            puck9 = c.Puck("blue side")
            red = c.Player("red", puck1, "standard", 0, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            blue = c.Player("blue", puck1, "standard", 1, puck2, puck3, puck4, puck5, puck6, puck7, puck8, puck9)
            game_reset = True
            
        
        # update classes
        red.update("standard walls")
        blue.update("standard walls")
        for puck in pucks:
            if puck.update("standard walls", "more_pucks"):
                pucks.remove(puck)
                del puck
            

        for puck in pucks:
            for puckk in pucks:
                puck.other_puck_collisions(puckk)        

        # calculate old positions
        red.old_x, red.old_y, blue.old_x, blue.old_y = red.x, red.y, blue.x, blue.y

        # draw
        c.WIN.blit(c.STANDARD_BG, (0,0))

        for puck in pucks:
            c.WIN.blit(c.PUCK_MODEL, (puck.x, puck.y))
        c.WIN.blit(c.RED_MODEL, (red.x, red.y))
        c.WIN.blit(c.BLUE_MODEL, (blue.x, blue.y))
        c.print_score("standard", 5)

        pygame.display.update()

        if frame == 1:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck1.x, puck1.y, "standard", "more", puck2.x, puck2.y, puck3.x, puck3.y, puck4.x, puck4.y, puck5.x, puck5.y, puck6.x, puck6.y, puck7.x, puck7.y, puck8.x, puck8.y, puck9.x, puck9.y)
        if game_reset:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck1.x, puck1.y, "standard", "more", puck2.x, puck2.y, puck3.x, puck3.y, puck4.x, puck4.y, puck5.x, puck5.y, puck6.x, puck6.y, puck7.x, puck7.y, puck8.x, puck8.y, puck9.x, puck9.y)
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main(9)