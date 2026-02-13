import pygame
import classes as c

def main(point_amount):
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    c.reset_scores()

    puck = c.Puck()
    red = c.Player("red", puck, "2v2")
    blue = c.Player("blue", puck, "2v2")
    green = c.Player("green", puck, "2v2")
    yellow = c.Player("yellow", puck, "2v2")
    
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

        reset_games = c.reset_game()
        if reset_games == "red":
            del red, blue, puck
            puck = c.Puck("blue side")
            red = c.Player("red", puck, "2v2")
            blue = c.Player("blue", puck, "2v2")
            green = c.Player("green", puck, "2v2")
            yellow = c.Player("yellow", puck, "2v2")
            game_reset = True
        elif reset_games == "blue":
            del red, blue, puck
            puck = c.Puck("red side")
            red = c.Player("red", puck, "2v2")
            blue = c.Player("blue", puck, "2v2")
            green = c.Player("green", puck, "2v2")
            yellow = c.Player("yellow", puck, "2v2")
            game_reset = True
            
        
        # update classes
        red.update("standard walls")
        blue.update("standard walls")
        green.update("standard walls")
        yellow.update("standard walls")
        puck.update("standard walls")

        # calculate old positions
        red.old_x, red.old_y, blue.old_x, blue.old_y = red.x, red.y, blue.x, blue.y
        green.old_x, green.old_y, yellow.old_x, yellow.old_y = green.x, green.y, yellow.x, yellow.y

        # draw
        c.WIN.blit(c.TWOVSTWO_BG, (0,0))

        c.WIN.blit(c.PUCK_MODEL, (puck.x, puck.y))
        c.WIN.blit(c.RED_MODEL, (red.x, red.y))
        c.WIN.blit(c.BLUE_MODEL, (blue.x, blue.y))
        c.WIN.blit(c.GREEN_MODEL, (green.x, green.y))
        c.WIN.blit(c.YELLOW_MODEL, (yellow.x, yellow.y))
        
        c.print_score("standard", 5)

        pygame.display.update()

        if frame == 1:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "standard", "2v2", green.x, green.y, yellow.x, yellow.y)
        if game_reset:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "standard", "2v2", green.x, green.y, yellow.x, yellow.y)
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main()