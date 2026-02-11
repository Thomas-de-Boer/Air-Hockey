import pygame
import classes as c
import webbrowser
import double_pucks, free_for_all, more_pucks, multiplayer, singleplayer, two_vs_two, highscore

TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT = c.WIN_SIZE[0] / 4, c.WIN_SIZE[1] / 4
LOGO_BUTTON_WIDTH, LOGO_BUTTON_HEIGHT = c.WIN_SIZE[0] * 0.09375 * 0.8, c.WIN_SIZE[1] * 0.1666666666666667 * 0.8
SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT = c.WIN_SIZE[0] * 0.09375 * 1.5, c.WIN_SIZE[1] * 0.1666666666666667 * 1.5

BLURRED_STANDARD_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/standard.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()
BLURRED_2V2_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/2v2.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()
BLURRED_FREEFORALL_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/freeforall.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()
BLURRED_MULTIPLAYER_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/multiplayer.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()
BLURRED_DOUBLE_PUCKS_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/double_pucks.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()
BLURRED_MORE_PUCKS_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/more_pucks.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()
BLURRED_HIGHSCORE_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/blurred/highscore.png"), (c.WIN_SIZE[0], c.WIN_SIZE[1])).convert_alpha()


LOGO = pygame.transform.scale(pygame.image.load("assets/logo.png"), (c.WIN_SIZE[0] / 2, c.WIN_SIZE[1] / 2)).convert_alpha()


EXIT_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/exit.png"), (LOGO_BUTTON_WIDTH, LOGO_BUTTON_HEIGHT)).convert_alpha()
EMPTY_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/empty.png"), (c.WIN_SIZE[0] / 3, c.WIN_SIZE[1] / 3.5)).convert_alpha()


SINGLEPLAYER_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/singleplayer.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
MULTIPLAYER_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/multiplayer.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
OTHER_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/other.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
SETTINGS_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/settings.png"), (LOGO_BUTTON_WIDTH, LOGO_BUTTON_HEIGHT)).convert_alpha()
WEBSITE_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/website.png"), (LOGO_BUTTON_WIDTH, LOGO_BUTTON_HEIGHT)).convert_alpha()

TWO_VS_TWO_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/2v2.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
FREEFORALL_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/freeforall.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
DOUBLE_PUCKS_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/double_pucks.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
MORE_PUCKS_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/more_pucks.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
OBSTACLE_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/obstacles.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
HIGHSCORE_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/highscore.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()

FIVE_POINTS_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/5_points.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
TEN_POINTS_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/10_points.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
FIFTEEN_POINTS_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/15_points.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()

ONE_MINUTE_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/1_minute.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
TWO_MINUTES_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/2_minutes.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
THREE_MINUTES_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/3_minutes.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()

EASY_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/easy.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
NORMAL_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/normal.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()
HARD_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/hard.png"), (TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT)).convert_alpha()

MOUSE_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/mouse.png"), (SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT)).convert_alpha()
TOUCHSCREEN_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/touchscreen.png"), (SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT)).convert_alpha()
JOYSTICK_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/joystick.png"), (SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT)).convert_alpha()
KEYBOARD_BUTTON = pygame.transform.scale(pygame.image.load("assets/buttons/keyboard.png"), (SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT)).convert_alpha()


FONT = pygame.font.Font(None, int(c.WIN_SIZE[1] // 15))

global point_amount, minute_amount
point_amount = 0
minute_amount = 0

def main():
    clock = pygame.time.Clock()

    menu_state = "start"

    current_background = BLURRED_STANDARD_BG

    slider = c.Slider(
        x=c.WIN_SIZE[0] / 2 - c.WIN_SIZE[1] / 2.5 / 2,
        y= c.WIN_SIZE[1] / 1.17,
        width=c.WIN_SIZE[1] / 2.5,
        min_value=0,
        max_value=1,
        start_value=c.VOLUME
    )


    exit_button = c.Button(c.WIN_SIZE[0] / 30, c.WIN_SIZE[1] / 30, EXIT_BUTTON)

    singleplayer_button = c.Button(c.WIN_SIZE[0] / 2 - c.WIN_SIZE[0] / 4 - c.WIN_SIZE[0] / 30, c.WIN_SIZE[1] / 2.5, SINGLEPLAYER_BUTTON)
    multiplayer_button = c.Button(c.WIN_SIZE[0] / 2 + c.WIN_SIZE[0] / 30, c.WIN_SIZE[1] / 2.5, MULTIPLAYER_BUTTON)
    other_button = c.Button(c.WIN_SIZE[0] / 2 - c.WIN_SIZE[0] / 4 / 2, c.WIN_SIZE[1] / 1.4, OTHER_BUTTON)
    settings_button = c.Button(c.WIN_SIZE[0] / 2 - c.WIN_SIZE[0] / 4, c.WIN_SIZE[1] / 1.4, SETTINGS_BUTTON)
    website_button = c.Button(c.WIN_SIZE[0] / 2 + c.WIN_SIZE[0] / 4 - LOGO_BUTTON_WIDTH, c.WIN_SIZE[1] / 1.4, WEBSITE_BUTTON)
    
    if c.MOVEMENT_TYPE != 2 or c.MOVEMENT_TYPE != 3:
        two_vs_two_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH * 1.3, c.WIN_SIZE[1] / 10, TWO_VS_TWO_BUTTON)
        freeforall_button = c.Button(c.WIN_SIZE[0] / 2 + TEXT_BUTTON_WIDTH * 0.3, c.WIN_SIZE[1] / 10, FREEFORALL_BUTTON)
        double_pucks_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH * 1.3, c.WIN_SIZE[1] / 2.5, DOUBLE_PUCKS_BUTTON)
        more_pucks_button = c.Button(c.WIN_SIZE[0] / 2 + TEXT_BUTTON_WIDTH * 0.3, c.WIN_SIZE[1] / 2.5, MORE_PUCKS_BUTTON)
        obstacle_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH * 1.3, c.WIN_SIZE[1] / 1.43, OBSTACLE_BUTTON)
        highscore_button = c.Button(c.WIN_SIZE[0] / 2 + TEXT_BUTTON_WIDTH * 0.3, c.WIN_SIZE[1] / 1.43, HIGHSCORE_BUTTON)
    else:
        double_pucks_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH * 1.3, c.WIN_SIZE[1] / 5, DOUBLE_PUCKS_BUTTON)
        more_pucks_button = c.Button(c.WIN_SIZE[0] / 2 + TEXT_BUTTON_WIDTH * 0.3, c.WIN_SIZE[1] / 5, MORE_PUCKS_BUTTON)
        obstacle_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH * 1.3, c.WIN_SIZE[1] / 2, OBSTACLE_BUTTON)
        highscore_button = c.Button(c.WIN_SIZE[0] / 2 + TEXT_BUTTON_WIDTH * 0.3, c.WIN_SIZE[1] / 2, HIGHSCORE_BUTTON)

    five_points_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 10, FIVE_POINTS_BUTTON)
    ten_points_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 2.5, TEN_POINTS_BUTTON)
    fifteen_points_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 1.43, FIFTEEN_POINTS_BUTTON)

    one_minute_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 10, ONE_MINUTE_BUTTON)
    two_minutes_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 2.5, TWO_MINUTES_BUTTON)
    three_minutes_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 1.43, THREE_MINUTES_BUTTON)

    easy_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 10, EASY_BUTTON)
    normal_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 2.5, NORMAL_BUTTON)
    hard_button = c.Button(c.WIN_SIZE[0] / 2 - TEXT_BUTTON_WIDTH / 2, c.WIN_SIZE[1] / 1.43, HARD_BUTTON)

    mouse_button = c.Button(c.WIN_SIZE[0] / 2 - SETTINGS_BUTTON_WIDTH * 1.5, c.WIN_SIZE[1] / 10, MOUSE_BUTTON)
    touchscreen_button = c.Button(c.WIN_SIZE[0] / 2 + SETTINGS_BUTTON_WIDTH * 0.5, c.WIN_SIZE[1] / 10, TOUCHSCREEN_BUTTON)
    joystick_button = c.Button(c.WIN_SIZE[0] / 2 - SETTINGS_BUTTON_WIDTH * 1.5, c.WIN_SIZE[1] / 2.5, JOYSTICK_BUTTON)
    keyboard_button = c.Button(c.WIN_SIZE[0] / 2 + SETTINGS_BUTTON_WIDTH * 0.5, c.WIN_SIZE[1] / 2.5, KEYBOARD_BUTTON)
    empty_button = c.Button(c.WIN_SIZE[0] / 2 - c.WIN_SIZE[0] / 3 / 2, c.WIN_SIZE[1] / 1.45, EMPTY_BUTTON)




    running = True
    while running:
        clock.tick(60)

        # event loop
        events = pygame.event.get()
        for event in events:

            # checks for escape to quit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            slider.handle_event(event)



        if menu_state == "start":
            current_background = BLURRED_STANDARD_BG

            if exit_button.check_click(events):
                running = False

            elif singleplayer_button.check_click(events):
                menu_state = "singleplayer"

            elif multiplayer_button.check_click(events):
                menu_state = "multiplayer"

            elif other_button.check_click(events):
                menu_state = "other"

            elif settings_button.check_click(events):
                menu_state = "settings"

            elif website_button.check_click(events):
                webbrowser.open('https://AirBlitz.leverhet.in/', new=2)


        elif menu_state == "other":
            current_background = BLURRED_STANDARD_BG

            if exit_button.check_click(events):
                menu_state = "start"

            if c.MOVEMENT_TYPE != 2 or c.MOVEMENT_TYPE != 3:
                if two_vs_two_button.check_click(events):
                    menu_state = "2v2"

                if freeforall_button.check_click(events):
                    menu_state = "freeforall"

            if double_pucks_button.check_click(events):
                menu_state = "double pucks"

            elif more_pucks_button.check_click(events):
                point_amount = 9
                more_pucks.main(point_amount)
            
            elif obstacle_button.check_click(events):
                pass

            elif highscore_button.check_click(events):
                menu_state = "highscore"

        elif menu_state == "singleplayer":
            current_background = BLURRED_MULTIPLAYER_BG

            if exit_button.check_click(events):
                menu_state = "start"

            elif five_points_button.check_click(events):
                point_amount = 5
                menu_state = "singleplayer2"

            elif ten_points_button.check_click(events):
                point_amount = 10
                menu_state = "singleplayer2"

            elif fifteen_points_button.check_click(events):
                point_amount = 15
                menu_state = "singleplayer2"

        elif menu_state == "singleplayer2":
            
            if exit_button.check_click(events):
                menu_state = "singleplayer"

            elif easy_button.check_click(events):
                difficulty = c.WIN_SIZE[1] / 108
                singleplayer.main(point_amount, difficulty)

            elif normal_button.check_click(events):
                difficulty = c.WIN_SIZE[1] / 72
                singleplayer.main(point_amount, difficulty)

            elif hard_button.check_click(events):
                difficulty = c.WIN_SIZE[1] / 54
                singleplayer.main(point_amount, difficulty)

        elif menu_state == "multiplayer":
            current_background = BLURRED_MULTIPLAYER_BG

            if exit_button.check_click(events):
                menu_state = "start"

            elif five_points_button.check_click(events):
                point_amount = 5
                multiplayer.main(point_amount)

            elif ten_points_button.check_click(events):
                point_amount = 10
                multiplayer.main(point_amount)

            elif fifteen_points_button.check_click(events):
                point_amount = 15
                multiplayer.main(point_amount)

        elif menu_state == "2v2":
            current_background = BLURRED_2V2_BG

            if exit_button.check_click(events):
                menu_state = "other"

            elif five_points_button.check_click(events):
                point_amount = 5
                two_vs_two.main(point_amount)

            elif ten_points_button.check_click(events):
                point_amount = 10
                two_vs_two.main(point_amount)

            elif fifteen_points_button.check_click(events):
                point_amount = 15
                two_vs_two.main(point_amount)

        elif menu_state == "freeforall":
            current_background = BLURRED_FREEFORALL_BG

            if exit_button.check_click(events):
                menu_state = "other"

            elif five_points_button.check_click(events):
                point_amount = 5
                free_for_all.main(point_amount)

            elif ten_points_button.check_click(events):
                point_amount = 10
                free_for_all.main(point_amount)

            elif fifteen_points_button.check_click(events):
                point_amount = 15
                free_for_all.main(point_amount)

        elif menu_state == "double pucks":
            current_background = BLURRED_DOUBLE_PUCKS_BG

            if exit_button.check_click(events):
                menu_state = "other"

            elif five_points_button.check_click(events):
                point_amount = 5
                double_pucks.main(point_amount)

            elif ten_points_button.check_click(events):
                point_amount = 10
                double_pucks.main(point_amount)

            elif fifteen_points_button.check_click(events):
                point_amount = 15
                double_pucks.main(point_amount)


        elif menu_state == "highscore":
            current_background = BLURRED_HIGHSCORE_BG

            if exit_button.check_click(events):
                menu_state = "other"

            elif one_minute_button.check_click(events):
                minutes_amount = 1
                highscore.main(minutes_amount)

            elif two_minutes_button.check_click(events):
                minutes_amount = 2
                highscore.main(minutes_amount)

            elif three_minutes_button.check_click(events):
                minutes_amount = 3
                highscore.main(minutes_amount)

        elif menu_state == "settings":
            current_background = BLURRED_STANDARD_BG

            if exit_button.check_click(events):
                menu_state = "start"

            if c.MOVEMENT_TYPE == 0:
                mouse_button.target_scale = 1.2
                if touchscreen_button.check_click(events):
                    c.MOVEMENT_TYPE = 1
                    c.write_movement()
                if joystick_button.check_click(events):
                    c.MOVEMENT_TYPE = 2
                    c.write_movement()
                if keyboard_button.check_click(events):
                    c.MOVEMENT_TYPE = 3
                    c.write_movement()

            elif c.MOVEMENT_TYPE == 1:
                if mouse_button.check_click(events):
                    c.MOVEMENT_TYPE = 0
                    c.write_movement()
                touchscreen_button.target_scale = 1.2
                if joystick_button.check_click(events):
                    c.MOVEMENT_TYPE = 2
                    c.write_movement()
                if keyboard_button.check_click(events):
                    c.MOVEMENT_TYPE = 3
                    c.write_movement()

            elif c.MOVEMENT_TYPE == 2:
                if mouse_button.check_click(events):
                    c.MOVEMENT_TYPE = 0
                    c.write_movement()
                if touchscreen_button.check_click(events):
                    c.MOVEMENT_TYPE = 1
                    c.write_movement()
                joystick_button.target_scale = 1.2
                if keyboard_button.check_click(events):
                    c.MOVEMENT_TYPE = 3
                    c.write_movement()

            elif c.MOVEMENT_TYPE == 3:
                if mouse_button.check_click(events):
                    c.MOVEMENT_TYPE = 0
                    c.write_movement()
                if touchscreen_button.check_click(events):
                    c.MOVEMENT_TYPE = 1
                    c.write_movement()
                if joystick_button.check_click(events):
                    c.MOVEMENT_TYPE = 2
                    c.write_movement()
                keyboard_button.target_scale = 1.2       


        # draw
        c.WIN.blit(current_background, (0, 0))

        if menu_state == "start":
            c.WIN.blit(LOGO, (c.WIN_SIZE[0] * 0.25, c.WIN_SIZE[1] - c.WIN_SIZE[1] * 1.03))
            singleplayer_button.draw()
            multiplayer_button.draw()
            other_button.draw()
            settings_button.draw()
            website_button.draw()
        
        if menu_state == "other":
            if c.MOVEMENT_TYPE != 2 or c.MOVEMENT_TYPE != 3:
                two_vs_two_button.draw()
                freeforall_button.draw()
            double_pucks_button.draw()
            more_pucks_button.draw()
            obstacle_button.draw()
            highscore_button.draw()

        if menu_state == "multiplayer" or menu_state == "singleplayer" or menu_state =="2v2" or menu_state == "freeforall" or menu_state == "double pucks":
            five_points_button.draw()
            ten_points_button.draw()
            fifteen_points_button.draw()

        if menu_state == "singleplayer2":
            easy_button.draw()
            normal_button.draw()
            hard_button.draw()

        if menu_state == "highscore":
            one_minute_button.draw()
            two_minutes_button.draw()
            three_minutes_button.draw()

        if menu_state == "settings":
            mouse_button.draw()
            touchscreen_button.draw()
            joystick_button.draw()
            keyboard_button.draw()

            empty_button.draw()
            text = FONT.render(f"VOLUME - {int(c.VOLUME * 100)}", True, (255, 255, 255))
            text_rect = text.get_rect()
            c.WIN.blit(text, (c.WIN_SIZE[0] / 2 - text_rect.centerx, c.WIN_SIZE[1] / 1.33))
            slider.draw(c.WIN)
            c.VOLUME = slider.value
            c.write_volume()


        exit_button.draw()

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()