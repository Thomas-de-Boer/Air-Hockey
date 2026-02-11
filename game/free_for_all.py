import pygame
import classes as c

def main(point_amount):
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    c.reset_scores()

    puck = c.Puck()
    red = c.Player("red", puck, "freeforall")
    blue = c.Player("blue", puck, "freeforall")
    green = c.Player("green", puck, "freeforall")
    yellow = c.Player("yellow", puck, "freeforall")
    
    c.make_walls_goals("freeforall walls", "freeforall")

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
                green.mouse_movement(event)
                yellow.mouse_movement(event)
            elif c.MOVEMENT_TYPE == 1:
                red.touchscreen_movement(event)
                blue.touchscreen_movement(event)
                green.touchscreen_movement(event)
                yellow.touchscreen_movement(event)

        if c.MOVEMENT_TYPE == 1:
            red.drag = red.dragging_finger is not None
            blue.drag = blue.dragging_finger is not None
            green.drag = green.dragging_finger is not None
            yellow.drag = yellow.dragging_finger is not None

        if c.red_score >= point_amount:
            c.anounce_winner("red")
            return
        elif c.blue_score >= point_amount:
            c.anounce_winner("blue")
            return
        elif c.green_score >= point_amount:
            c.anounce_winner("green")
            return
        elif c.yellow_score >= point_amount:
            c.anounce_winner("yellow")
            return

        reset_games = c.reset_game_ffo()
        if reset_games == "red":
            del red, blue, green, yellow, puck
            puck = c.Puck("red ffo")
            red = c.Player("red", puck, "freeforall")
            blue = c.Player("blue", puck, "freeforall")
            green = c.Player("green", puck, "freeforall")
            yellow = c.Player("yellow", puck, "freeforall")
            game_reset = True
        elif reset_games == "blue":
            del red, blue, green, yellow, puck
            puck = c.Puck("blue ffo")
            red = c.Player("red", puck, "freeforall")
            blue = c.Player("blue", puck, "freeforall")
            green = c.Player("green", puck, "freeforall")
            yellow = c.Player("yellow", puck, "freeforall")
            game_reset = True
        elif reset_games == "green":
            del red, blue, green, yellow, puck
            puck = c.Puck("green ffo")
            red = c.Player("red", puck, "freeforall")
            blue = c.Player("blue", puck, "freeforall")
            green = c.Player("green", puck, "freeforall")
            yellow = c.Player("yellow", puck, "freeforall")
            game_reset = True
        elif reset_games == "yellow":
            del red, blue, green, yellow, puck
            puck = c.Puck("yellow ffo")
            red = c.Player("red", puck, "freeforall")
            blue = c.Player("blue", puck, "freeforall")
            green = c.Player("green", puck, "freeforall")
            yellow = c.Player("yellow", puck, "freeforall")
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
        c.WIN.blit(c.FREEFORALL_BG, (0,0))

        c.WIN.blit(c.PUCK_MODEL, (puck.x, puck.y))
        c.WIN.blit(c.RED_MODEL, (red.x, red.y))
        c.WIN.blit(c.BLUE_MODEL, (blue.x, blue.y))
        c.WIN.blit(c.GREEN_MODEL, (green.x, green.y))
        c.WIN.blit(c.YELLOW_MODEL, (yellow.x, yellow.y))
        
        c.print_score("freeforall", 5)

        pygame.display.update()

        if frame == 1:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "freeforall", "freeforall", green.x, green.y, yellow.x, yellow.y)
        if game_reset:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "freeforall", "freeforall", green.x, green.y, yellow.x, yellow.y)
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main()