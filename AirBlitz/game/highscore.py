import pygame
import classes as c
import requests
import datetime

def text_input():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, int(c.WIN_SIZE[1] // 19.28571428571429))
    title_font = pygame.font.Font(None, int(c.WIN_SIZE[1] // 16.875))

    BLUR_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/highscore.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()
    EMPTY_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/empty.png"), (c.WIN_SIZE[0] / 3, c.WIN_SIZE[1] / 3)).convert_alpha()
    EXIT_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/exit.png"), (c.WIN_SIZE[0] * 0.09375 * 0.8, c.WIN_SIZE[1] * 0.1666666666666667 * 0.8)).convert_alpha()


    empty_button = c.Button(c.WIN_SIZE[0] / 2 - c.WIN_SIZE[0] / 6, c.WIN_SIZE[1] / 2 - c.WIN_SIZE[1] / 6, EMPTY_BUTTON)
    exit_button = c.Button(c.WIN_SIZE[0] / 30, c.WIN_SIZE[1] / 30, EXIT_BUTTON)


    input_box = pygame.Rect(
        c.WIN_SIZE[0] // 2 - int(c.WIN_SIZE[1] // 4.909090909090909),
        c.WIN_SIZE[1] // 2,
        int(c.WIN_SIZE[1] // 2.454545454545455),
        int(c.WIN_SIZE[1] // 15.42857142857143)
    )

    text = ""
    max_length = 10

    color = (255, 255, 255)
    border_width = int(c.WIN_SIZE[1] / 135)

    while True:
        clock.tick(60)


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return ""

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                
                if event.key == pygame.K_RETURN:
                    return text

                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                else:
                    if len(text) < max_length and event.unicode.isprintable():
                        text += event.unicode

        if exit_button.check_click(events):
            return ""

        c.WIN.blit(BLUR_BG, (0, 0))

        empty_button.draw()
        exit_button.draw()

        title = title_font.render("ENTER YOUR NAME", True, color)
        c.WIN.blit(title, (c.WIN_SIZE[0] // 2 - title.get_width() // 2, input_box.y - int(c.WIN_SIZE[1] / 12)))

        txt_surface = font.render(text, True, color)
        c.WIN.blit(txt_surface, (input_box.x + 16, input_box.y + int(c.WIN_SIZE[1] / 67.5)))

        pygame.draw.rect(c.WIN, color, input_box, border_width, border_radius=10)

        pygame.display.update()


def input_database(name, score):
    date = str(datetime.datetime.today()).split()[0]
    
    url = "https://airblitz.leverhet.in/khdbhihhgidgbkndfhbojedhvikdfgvjkdfkgjdhrgh/API/index.php"
    
    data = {
        "playername": name,
        "score": score,
        "highscoredate": date,
        "gamemode": gamemode
    }
    
    requests.post(url, data=data)


def main(minute_amount):
    global gamemode
    gamemode = minute_amount
    clock = pygame.time.Clock()
    frame = 0
    game_reset = False

    second_amount = 0

    c.reset_scores()

    puck = c.Puck()
    red = c.Player("red", puck, "standard", 0)
    blue = c.Player("blue", puck, "standard", 1)
    
    c.make_walls_goals("standard walls")

    running = True
    while running:
        clock.tick(60)
        frame += 1

        if second_amount <= -1:
            minute_amount -= 1
            second_amount += 60
        
        if frame % 60 == 0:
            second_amount -= 1

        if minute_amount <= 0 and second_amount <= 0 or minute_amount < 0:
            name = text_input()
            if name == "":
                return
            input_database(name, c.red_score - c.blue_score)
            return

        # event loop
        for event in pygame.event.get():

            # checks for escape to quit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
                
                if event.key == pygame.K_u:
                    second_amount -= 10

            if c.MOVEMENT_TYPE == 0:
                red.mouse_movement(event)
            elif c.MOVEMENT_TYPE == 1:
                red.touchscreen_movement(event)
            elif c.MOVEMENT_TYPE == 2:
                red.arcade_movement(event)

        if c.MOVEMENT_TYPE == 1:
            red.drag = red.dragging_finger is not None

        elif c.MOVEMENT_TYPE == 2:
            red.arcade_movement_outside_event()
            red.drag = True

        elif c.MOVEMENT_TYPE == 3:
            red.keyboard_movement()
            red.drag = True
            
        blue.drag = True
        


        reset_games = c.reset_game()
        if reset_games == "red":
            del red, blue, puck
            puck = c.Puck("blue side")
            red = c.Player("red", puck, "standard", 0)
            blue = c.Player("blue", puck, "standard", 1)
            game_reset = True
        elif reset_games == "blue":
            del red, blue, puck
            puck = c.Puck("red side")
            red = c.Player("red", puck, "standard", 0)
            blue = c.Player("blue", puck, "standard", 1)
            game_reset = True
            
        
        blue.bot(c.WIN_SIZE[1] / 54)

        # update classes
        red.update("standard walls")
        blue.update("standard walls")
        puck.update("standard walls")

        # calculate old positions
        red.old_x, red.old_y, blue.old_x, blue.old_y = red.x, red.y, blue.x, blue.y

        # draw
        c.WIN.blit(c.STANDARD_BG, (0,0))

        c.WIN.blit(c.PUCK_MODEL, (puck.x, puck.y))
        c.WIN.blit(c.RED_MODEL, (red.x, red.y))
        c.WIN.blit(c.BLUE_MODEL, (blue.x, blue.y))
        c.print_score("highscore", minute_amount, second_amount)

        pygame.display.update()

        if frame == 1:
            c.countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "highscore", minute_amount=minute_amount, second_amount=second_amount)
        if game_reset:
            second_amount = c.countdown_start(red.x, red.y, blue.x, blue.y, puck.x, puck.y, "highscore", minute_amount=minute_amount, second_amount=second_amount, first_countdown=True)
            game_reset = False
    pygame.quit()

if __name__ == "__main__":
    main(1)