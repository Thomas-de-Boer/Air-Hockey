import pygame
import classes as c

def main(point_amount):
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    c.reset_scores()

    puck1 = c.Puck("db 1")
    puck2 = c.Puck("db 2")
    red = c.Player("red", puck1, "standard", 0, puck2)
    blue = c.Player("blue", puck1, "standard", 1, puck2)
    
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
            del red, blue, puck1, puck2
            puck1 = c.Puck("blue ffo")
            puck2 = c.Puck("yellow ffo")
            red = c.Player("red", puck1, "standard", 0, puck2)
            blue = c.Player("blue", puck1, "standard", 1, puck2)
            game_reset = True
        elif reset_games == "blue":
            del red, blue, puck1, puck2
            puck1 = c.Puck("green ffo")
            puck2 = c.Puck("red ffo")
            red = c.Player("red", puck1, "standard", 0, puck2)
            blue = c.Player("blue", puck1, "standard", 1, puck2)
            game_reset = True            
        
        # update classes
        red.update("standard walls")
        blue.update("standard walls")
        puck1.update("standard walls")
        puck2.update("standard walls")

        puck1.other_puck_collisions(puck2)
        puck2.other_puck_collisions(puck1)

        # calculate old positions
        red.old_x, red.old_y, blue.old_x, blue.old_y = red.x, red.y, blue.x, blue.y

        # draw
        c.WIN.blit(c.STANDARD_BG, (0,0))

        c.WIN.blit(c.PUCK_MODEL, (puck1.x, puck1.y))
        c.WIN.blit(c.PUCK_MODEL, (puck2.x, puck2.y))
        c.WIN.blit(c.RED_MODEL, (red.x, red.y))
        c.WIN.blit(c.BLUE_MODEL, (blue.x, blue.y))
        c.print_score("standard", 5)

        pygame.display.update()

        if frame == 1:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck1.x, puck1.y, "standard", "db", puck2.x, puck2.y)
        if game_reset:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck1.x, puck1.y, "standard", "db", puck2.x, puck2.y)
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main()