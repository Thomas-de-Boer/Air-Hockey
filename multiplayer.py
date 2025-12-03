import pygame
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
pygame.display.init()

WIN_SIZE = pygame.display.get_desktop_sizes()[0]

PLAYER_WIDTH, PLAYER_HEIGHT = WIN_SIZE[0] * 0.09375, WIN_SIZE[1] * 0.1666666666666667
PUCK_WIDTH, PUCK_HEIGHT = WIN_SIZE[0] * 0.05625, WIN_SIZE[1] * 0.1

PUCK_FRICTION = 0.97
PLAYER_FRICTION = 0.75

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

BG = pygame.transform.scale(pygame.image.load("AirHockey/assets/standard_background.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()

RED_MODEL = pygame.transform.scale(pygame.image.load("AirHockey/assets/red_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
BLUE_MODEL = pygame.transform.scale(pygame.image.load("AirHockey/assets/blue_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()  
PUCK_MODEL = pygame.transform.scale(pygame.image.load("AirHockey/assets/temp_puck.png"), (PUCK_WIDTH, PUCK_HEIGHT)).convert_alpha()

# wall positions
walls = [
    ((-WIN_SIZE[0] / 2, 0), (WIN_SIZE[0] * 2, -WIN_SIZE[0])),
    ((WIN_SIZE[0] / 40, 0), (-WIN_SIZE[0], WIN_SIZE[1])),
    ((-WIN_SIZE[0] / 2, WIN_SIZE[1]), (WIN_SIZE[0] * 2, WIN_SIZE[0])),
    ((WIN_SIZE[0] - WIN_SIZE[0] / 40, 0), (WIN_SIZE[0], WIN_SIZE[1])),

    ((WIN_SIZE[0], 0), (-WIN_SIZE[0] / 2, WIN_SIZE[1])),
    ((0, 0), (WIN_SIZE[0] / 2, WIN_SIZE[1]))
    ]
# wall positions in human language
# ((0, 0), (1600, -1)), top wall
# ((0, 0), (-1, 900)), left wall
# ((0, 900), (1600, 1)), bottom wall
# ((1600, 0), (1, 900)), right wall

# middle walls

# ((-WIN_SIZE[0] / 2, 0), (WIN_SIZE[0] * 2, -WIN_SIZE[0])),
# ((0, 0), (-WIN_SIZE[0], WIN_SIZE[1])),
# ((-WIN_SIZE[0] / 2, WIN_SIZE[1]), (WIN_SIZE[0] * 2, WIN_SIZE[0])),
# ((WIN_SIZE[0], 0), (WIN_SIZE[0], WIN_SIZE[1])),


def draw(red_x, red_y, blue_x, blue_y, puck_x, puck_y):
    # draw background
    WIN.blit(BG, (0,0))

    # draw players
    WIN.blit(RED_MODEL, (red_x, red_y))
    WIN.blit(BLUE_MODEL, (blue_x, blue_y))

    # draw puck
    WIN.blit(PUCK_MODEL, (puck_x, puck_y))

    # update display
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    # make walls
    for i in range(len(walls)):
        walls[i] = pygame.Rect(walls[i])

    # make players
    red = pygame.Rect((WIN_SIZE[0] / 9, WIN_SIZE[1] / 2 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))
    blue = pygame.Rect((WIN_SIZE[0] - WIN_SIZE[0] / 5, WIN_SIZE[1] - WIN_SIZE[1] / 2 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))

    # make puck
    puck = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH / 2, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))

    # make drag variable
    red_drag = False
    blue_drag = False

    # make frame variable
    frame = 0

    # make velocity variables
    red_vel_x, red_vel_y = 0, 0
    red_old_x, red_old_y = 0, 0
    blue_vel_x, blue_vel_y = 0, 0
    blue_old_x, blue_old_y = 0, 0
    puck_vel_x, puck_vel_y = 0, 0

    running = True
    while running:
        clock.tick(60)
        if frame < 3:
            frame += 1
        
        # event loop
        for event in pygame.event.get():

            # checks for escape to quit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # red player movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if red.collidepoint(event.pos):
                        red_drag = True
                        mouse_x, mouse_y = event.pos
                        offset_x = red.x - mouse_x
                        offset_y = red.y - mouse_y
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    red_drag = False
                    
            if event.type == pygame.MOUSEMOTION:
                if red_drag:
                    mouse_x, mouse_y = event.pos
                    red.x = mouse_x + offset_x
                    red.y = mouse_y + offset_y

            # blue player movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if blue.collidepoint(event.pos):
                        blue_drag = True
                        mouse_x, mouse_y = event.pos
                        offset_x = blue.x - mouse_x
                        offset_y = blue.y - mouse_y
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    blue_drag = False
                    
            if event.type == pygame.MOUSEMOTION:
                if blue_drag:
                    mouse_x, mouse_y = event.pos
                    blue.x = mouse_x + offset_x
                    blue.y = mouse_y + offset_y

        # set player / puck velocity to 0 when under 0.3
        if -0.3 <= puck_vel_x <= 0.3:
            puck_vel_x = 0
        if -0.3 <= puck_vel_x <= 0.3:
            puck_vel_y = 0

        if -0.3 <= red_vel_x <= 0.3:
            red_vel_x = 0
        if -0.3 <= red_vel_x <= 0.3:
            red_vel_y = 0

        if -0.3 <= blue_vel_x <= 0.3:
            blue_vel_x = 0
        if -0.3 <= blue_vel_x <= 0.3:
            blue_vel_y = 0

        # calculate players velocity
        if red_drag:
            red_vel_x = red.x - red_old_x
            red_vel_y = red.y - red_old_y
        if blue_drag:
            blue_vel_x = blue.x - blue_old_x
            blue_vel_y = blue.y - blue_old_y

        # make players slide
        if frame > 2:
            if red_drag == False:
                red.x += red_vel_x
                red.y += red_vel_y

                red_vel_x *= PLAYER_FRICTION
                red_vel_y *= PLAYER_FRICTION

            if blue_drag == False:
                blue.x += blue_vel_x
                blue.y += blue_vel_y
                blue_vel_x *= PLAYER_FRICTION
                blue_vel_y *= PLAYER_FRICTION

        # puck collision detection
        if red.colliderect(walls[4]):
            pass
        else:
            if red.colliderect(puck):
                if red_vel_x == 0 and red_vel_y == 0:
                    puck_vel_x *= -1
                    puck_vel_y *= -1

                puck_vel_x, puck_vel_y = red_vel_x, red_vel_y
        if blue.colliderect(walls[5]):
            pass
        else:
            if blue.colliderect(puck):
                if blue_vel_x == 0 and blue_vel_y == 0:
                    puck_vel_x *= -1
                    puck_vel_y *= -1

                puck_vel_x, puck_vel_y = blue_vel_x, blue_vel_y
        
        
        puck.x += puck_vel_x
        puck.y += puck_vel_y

        # puck velocity loss over time
        puck_vel_x *= PUCK_FRICTION
        puck_vel_y *= PUCK_FRICTION

        # teleport puck outside player when interacting
        if red.colliderect(walls[4]):
            pass
        else:
            if red.colliderect(puck):
                if puck.centerx > red.centerx:
                    puck.left = red.right
                elif puck.centerx < red.centerx:
                    puck.right = red.left
                elif puck.centery > red.centery:
                    puck.top = red.bottom
                elif puck.centery < red.centery:
                    puck.bottom = red.top

        if blue.colliderect(walls[5]):
            pass
        else:
            if blue.colliderect(puck):
                if puck.centerx > blue.centerx:
                    puck.left = blue.right
                elif puck.centerx < blue.centerx:
                    puck.right = blue.left
                elif puck.centery > blue.centery:
                    puck.top = blue.bottom
                elif puck.centery < blue.centery:
                    puck.bottom = blue.top
        
        # puck/players wall collision detection
        if puck.colliderect(walls[0]):
            puck_vel_y *= -1
            puck.top = walls[0].top
        if puck.colliderect(walls[1]):
            puck_vel_x *= -1
            puck.left = walls[1].left
        if puck.colliderect(walls[2]):
            puck_vel_y *= -1
            puck.bottom = walls[2].top
        if puck.colliderect(walls[3]):
            puck_vel_x *= -1
            puck.right = walls[3].left
        
        if red.colliderect(walls[0]):
            red_vel_y *= -1
            red.top = walls[0].top
        if red.colliderect(walls[1]):
            red_vel_x *= -1
            red.left = walls[1].left
        if red.colliderect(walls[2]):
            red_vel_y *= -1
            red.bottom = walls[2].top
        if red.colliderect(walls[3]):
            red_vel_x *= -1
            red.right = walls[3].left
        if red.colliderect(walls[4]):
            red_vel_x *= -1
            red.right = walls[4].right
        
        if blue.colliderect(walls[0]):
            blue_vel_y *= -1
            blue.top = walls[0].top
        if blue.colliderect(walls[1]):
            blue_vel_x *= -1
            blue.left = walls[1].left
        if blue.colliderect(walls[2]):
            blue_vel_y *= -1
            blue.bottom = walls[2].top
        if blue.colliderect(walls[3]):
            blue_vel_x *= -1
            blue.right = walls[3].left
        if blue.colliderect(walls[5]):
            blue_vel_x *= -1
            blue.left = walls[5].right

        draw(red.x, red.y, blue.x, blue.y, puck.x, puck.y)

        red_old_x, red_old_y = red.x, red.y
        blue_old_x, blue_old_y = blue.x, blue.y

    pygame.quit()

if __name__ == "__main__":
    main()