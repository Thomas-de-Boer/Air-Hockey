import pygame
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
pygame.display.init()

WIN_SIZE = pygame.display.get_desktop_sizes()[0]

PLAYER_WIDTH, PLAYER_HEIGHT = WIN_SIZE[0] * 0.09375, WIN_SIZE[1] * 0.1666666666666667
PUCK_WIDTH, PUCK_HEIGHT = WIN_SIZE[0] * 0.05625, WIN_SIZE[1] * 0.1

PUCK_FRICTION = 0.97
PLAYER_FRICTION = 0.75

MOUSE_MOVEMENT = True
TOUCHSCREEN_MOVEMENT = False

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

BG = pygame.transform.scale(pygame.image.load("AirHockey/assets/standard_background.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()

RED_MODEL = pygame.transform.scale(pygame.image.load("AirHockey/assets/red_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
BLUE_MODEL = pygame.transform.scale(pygame.image.load("AirHockey/assets/blue_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()  
PUCK_MODEL = pygame.transform.scale(pygame.image.load("AirHockey/assets/puck.png"), (PUCK_WIDTH, PUCK_HEIGHT)).convert_alpha()

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

    red_mask = pygame.mask.from_surface(RED_MODEL)
    blue_mask = pygame.mask.from_surface(BLUE_MODEL)

    # make puck
    puck = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH / 2, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))

    puck_mask = pygame.mask.from_surface(PUCK_MODEL)

    # make mouse
    mouse = pygame.Surface((1, 1))
    mouse_mask = pygame.mask.from_surface(mouse)

    # make finger
    finger = pygame.Surface((1, 1))
    finger_mask = pygame.mask.from_surface(finger)

    # make touchscreen variables
    red_dragging_finger = None
    blue_dragging_finger = None
    red_drag_offset = (0, 0)
    blue_drag_offset = (0, 0)

    # make drag variable for mouse controlls
    red_drag = False
    blue_drag = False
    red_offset = [0, 0]
    blue_offset = [0, 0]

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

            # get mouse pos
            mouse_pos = pygame.mouse.get_pos()

            if MOUSE_MOVEMENT:
                # red player mouse movement
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if red_mask.overlap(mouse_mask, (mouse_pos[0] - red.x, mouse_pos[1] - red.y)):
                            red_drag = True
                            red_offset[0] = red.x - mouse_pos[0]
                            red_offset[1] = red.y - mouse_pos[1]
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        red_drag = False
                        
                if event.type == pygame.MOUSEMOTION:
                    if red_drag:
                        red.x = mouse_pos[0] + red_offset[0]
                        red.y = mouse_pos[1] + red_offset[1]

                # blue player mouse movement
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if blue_mask.overlap(mouse_mask, (mouse_pos[0] - blue.x, mouse_pos[1] - blue.y)):
                            blue_drag = True
                            blue_offset[0] = blue.x - mouse_pos[0]
                            blue_offset[1] = blue.y - mouse_pos[1]
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        blue_drag = False
                        
                if event.type == pygame.MOUSEMOTION:
                    if blue_drag:
                        blue.x = mouse_pos[0] + blue_offset[0]
                        blue.y = mouse_pos[1] + blue_offset[1]


            # touchscreen movement
            if TOUCHSCREEN_MOVEMENT:
                if event.type == pygame.FINGERDOWN:
                    x = int(event.x * WIN_SIZE[0])
                    y = int(event.y * WIN_SIZE[1])

                    # check if finger is on red
                    if red_dragging_finger is None:
                        offset_x = red.x - x
                        offset_y = red.y - y
                        if red_mask.overlap(finger_mask, (x - red.x, y - red.y)):
                            red_dragging_finger = event.finger_id
                            red_drag_offset = (offset_x, offset_y)

                    # check if finger is on blue
                    if blue_dragging_finger is None:
                        offset_x = blue.x - x
                        offset_y = blue.y - y
                        if blue_mask.overlap(finger_mask, (x - blue.x, y - blue.y)):
                            blue_dragging_finger = event.finger_id
                            blue_drag_offset = (offset_x, offset_y)

                if event.type == pygame.FINGERUP:
                    # let go when finger is lifted
                    if red_dragging_finger == event.finger_id:
                        red_dragging_finger = None
                    if blue_dragging_finger == event.finger_id:
                        blue_dragging_finger = None

                if event.type == pygame.FINGERMOTION:
                    # update position when moving
                    x = int(event.x * WIN_SIZE[0])
                    y = int(event.y * WIN_SIZE[1])

                    # move player when dragged
                    if red_dragging_finger == event.finger_id:
                        red.x = x + red_drag_offset[0]
                        red.y = y + red_drag_offset[1]

                    # move player when dragged
                    if blue_dragging_finger == event.finger_id:
                        blue.x = x + blue_drag_offset[0]
                        blue.y = y + blue_drag_offset[1]

        if TOUCHSCREEN_MOVEMENT:
            red_drag = red_dragging_finger is not None
            blue_drag = blue_dragging_finger is not None

        # calculate players velocity
        if red_drag:
            red_vel_x = red.x - red_old_x
            red_vel_y = red.y - red_old_y
        if blue_drag:
            blue_vel_x = blue.x - blue_old_x
            blue_vel_y = blue.y - blue_old_y

        # set player / puck velocity to 0 when under 0.3
        if -0.3 <= puck_vel_x <= 0.3:
            puck_vel_x = 0
        if -0.3 <= puck_vel_y <= 0.3:
            puck_vel_y = 0

        if -0.3 <= red_vel_x <= 0.3:
            red_vel_x = 0
        if -0.3 <= red_vel_y <= 0.3:
            red_vel_y = 0

        if -0.3 <= blue_vel_x <= 0.3:
            blue_vel_x = 0
        if -0.3 <= blue_vel_y <= 0.3:
            blue_vel_y = 0

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
            if red_mask.overlap(puck_mask, (puck.x - red.x, puck.y - red.y)):
                if red_vel_x == 0 and red_vel_y == 0:
                    if puck.centerx > red.centerx:
                        puck_vel_x *= -1
                    elif puck.centerx < red.centerx:
                        puck_vel_x *= -1
                    elif puck.centery > red.centery:
                        puck_vel_y *= -1
                    elif puck.centery < red.centery:
                        puck_vel_y *= -1

                else:
                    puck_vel_x, puck_vel_y = red_vel_x, red_vel_y
        if blue.colliderect(walls[5]):
            pass
        else:
            if blue_mask.overlap(puck_mask, (puck.x - blue.x, puck.y - blue.y)):
                if blue_vel_x == 0 and blue_vel_y == 0:
                    if puck.centerx > blue.centerx:
                        puck_vel_x *= -1
                    elif puck.centerx < blue.centerx:
                        puck_vel_x *= -1
                    elif puck.centery > blue.centery:
                        puck_vel_y *= -1
                    elif puck.centery < blue.centery:
                        puck_vel_y *= -1

                else:
                    puck_vel_x, puck_vel_y = blue_vel_x, blue_vel_y
        
        puck.x += puck_vel_x
        puck.y += puck_vel_y

        # puck velocity loss over time
        puck_vel_x *= PUCK_FRICTION
        puck_vel_y *= PUCK_FRICTION

        # teleport puck outside player when interacting
        # if red.colliderect(walls[4]):
        #     pass
        # else:
        #     if red_mask.overlap(puck_mask, (puck.x - red.x, puck.y - red.y)):
        #         if puck.centerx > red.centerx:
        #             puck.left = red.right
        #         elif puck.centerx < red.centerx:
        #             puck.right = red.left
        #         if puck.centery > red.centery:
        #             puck.top = red.bottom
        #         elif puck.centery < red.centery:
        #             puck.bottom = red.top

        # if blue.colliderect(walls[5]):
        #     pass
        # else:
        #     if blue_mask.overlap(puck_mask, (puck.x - blue.x, puck.y - blue.y)):
        #         if puck.centerx > blue.centerx:
        #             puck_vel_x += 2
        #         elif puck.centerx < blue.centerx:
        #             puck_vel_x -= 2
        #         if puck.centery > blue.centery:
        #             puck_vel_x += 2
        #         elif puck.centery < blue.centery:
        #             puck_vel_x -= 2

        # overlapx = puck.centerx - blue.centerx
        # overlapy = puck.centery - blue.centery
        # if blue.colliderect(walls[5]):
        #     pass
        # else:
        #     if overlapx < ((PLAYER_WIDTH / 2) - 1) and overlapx > -((PLAYER_WIDTH / 2) - 1):
        #         puck_vel_x -= 0.4
        #     elif overlapx > (0) and overlapx < ((PLAYER_WIDTH / 2) + 1):
        #         puck_vel_x += 0.4
        #     if overlapy < ((PLAYER_WIDTH / 2) - 1) and overlapy > -((PLAYER_WIDTH / 2) - 1):
        #         puck_vel_y -= 0.4
        #     elif overlapy > (0) and overlapy < -((PLAYER_WIDTH / 2) - 1):
        #         puck_vel_y += 0.4
                
        
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
