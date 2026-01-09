import pygame
import ctypes
import time
ctypes.windll.user32.SetProcessDPIAware()
pygame.display.init()
pygame.font.init()

WIN_SIZE = pygame.display.get_desktop_sizes()[0]

PLAYER_WIDTH, PLAYER_HEIGHT = WIN_SIZE[0] * 0.09375, WIN_SIZE[1] * 0.1666666666666667
PUCK_WIDTH, PUCK_HEIGHT = WIN_SIZE[0] * 0.05625, WIN_SIZE[1] * 0.1

FONT = pygame.font.Font(None, WIN_SIZE[0] // 15)

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
STANDARD_BG = pygame.transform.scale(pygame.image.load("assets/standard_background.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()
FREEFORALL_BG = pygame.transform.scale(pygame.image.load("assets/freeforall_background.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()
TWOVSTWO_BG = pygame.transform.scale(pygame.image.load("assets/2v2_background.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()

RED_MODEL = pygame.transform.scale(pygame.image.load("assets/red_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
BLUE_MODEL = pygame.transform.scale(pygame.image.load("assets/blue_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
GREEN_MODEL = pygame.transform.scale(pygame.image.load("assets/green_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
YELLOW_MODEL = pygame.transform.scale(pygame.image.load("assets/yellow_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
PUCK_MODEL = pygame.transform.scale(pygame.image.load("assets/puck.png"), (PUCK_WIDTH, PUCK_HEIGHT)).convert_alpha()

# 0 for mouse, 1 for touchscreen
MOVEMENT_TYPE = 0

# score variables
red_score = 0
blue_score = 0
green_score = 0
yellow_score = 0
red_scored = False
blue_scored = False
green_scored = False
yellow_scored = False
last_touch = []

# all wall positions and sizes
side_walls = [
    ((-WIN_SIZE[0] / 2, 0), (WIN_SIZE[0] * 2, -WIN_SIZE[0])), # top wall
    ((WIN_SIZE[0] / 40, 0), (-WIN_SIZE[0], WIN_SIZE[1])), # left wall
    ((-WIN_SIZE[0] / 2, WIN_SIZE[1]), (WIN_SIZE[0] * 2, WIN_SIZE[0])), # bottom wall
    ((WIN_SIZE[0] - WIN_SIZE[0] / 40, 0), (WIN_SIZE[0], WIN_SIZE[1])), # right wall
]

standard_walls = [
    ((WIN_SIZE[0], 0), (-WIN_SIZE[0] / 2, WIN_SIZE[1])), # blue side wall (right)
    ((0, 0), (WIN_SIZE[0] / 2, WIN_SIZE[1])) # red side wall (left)
]

freeforall_walls = [
    ((0, 0), (WIN_SIZE[0], WIN_SIZE[1] * 0.040)), # top wall
    ((0, WIN_SIZE[1] - WIN_SIZE[1] * 0.040), (WIN_SIZE[0], WIN_SIZE[1] * 0.040)), # bottom wall

    ((0, 0), (WIN_SIZE[0] / 2, WIN_SIZE[1] / 2)),
    ((0, WIN_SIZE[1] / 2), (WIN_SIZE[0] / 2, WIN_SIZE[1] / 2)),
    ((WIN_SIZE[0] / 2, 0), (WIN_SIZE[0] / 2, WIN_SIZE[1] / 2)),
    ((WIN_SIZE[0] / 2, WIN_SIZE[1] / 2), (WIN_SIZE[0] / 2, WIN_SIZE[1] / 2))
]


standard_goals = [
    ((WIN_SIZE[0] / 40 + 1, WIN_SIZE[1] / 3 + PUCK_HEIGHT / 2), (1, WIN_SIZE[1] / 3 - PUCK_HEIGHT / 2)),
    ((WIN_SIZE[0] - WIN_SIZE[0] / 40 - 1, WIN_SIZE[1] / 3 + PUCK_HEIGHT / 2), (1, WIN_SIZE[1] / 3 - PUCK_HEIGHT / 2))
]
freeforall_goals = [
    ((WIN_SIZE[0] / 40 + 1, 0), (1, WIN_SIZE[1] / 3 - PUCK_HEIGHT / 2)), # vertical green
    ((0, WIN_SIZE[1] * 0.04 + 1), (WIN_SIZE[0] * 0.21 - PUCK_WIDTH / 2, 1)), # horizontal green
    ((WIN_SIZE[0] / 40 + 1, WIN_SIZE[1] / 3 * 2 + PUCK_HEIGHT / 2), (1, WIN_SIZE[1] / 3)), # vertical red
    ((0, WIN_SIZE[1] - WIN_SIZE[1] * 0.04 - 1), (WIN_SIZE[0] * 0.21, 1)), # horizontal red
    ((WIN_SIZE[0] - WIN_SIZE[0] / 40 - 1, 0), (1, WIN_SIZE[1] / 3 - PUCK_HEIGHT / 2)), # vertical blue
    ((WIN_SIZE[0] - WIN_SIZE[0] * 0.21 + PUCK_WIDTH / 2, WIN_SIZE[1] * 0.04 + 1), (WIN_SIZE[0] * 0.21, 1)), # horizontal blue
    ((WIN_SIZE[0] - WIN_SIZE[0] / 40 - 1, WIN_SIZE[1] / 3 * 2 + PUCK_HEIGHT / 2), (1, WIN_SIZE[1] / 3)), # vertical yellow
    ((WIN_SIZE[0] - WIN_SIZE[0] * 0.21 + PUCK_WIDTH / 2, WIN_SIZE[1] - WIN_SIZE[1] * 0.04 - 1), (WIN_SIZE[0] * 0.21, 1)) # horizontal yellow
]

def make_walls_goals(walls_type, goals_type="standard"):
    global walls
    walls = []
    walls.clear()
    for wall in side_walls:
        walls.append(pygame.Rect(wall))

    if walls_type == "standard walls":
        for wall in standard_walls:
            walls.append(pygame.Rect(wall))

    if walls_type == "freeforall walls":
        for wall in freeforall_walls:
            walls.append(pygame.Rect(wall))

    global goals
    goals = []
    goals.clear()
    if goals_type == "standard":
        for goal in standard_goals:
            goals.append(pygame.Rect(goal))

    if goals_type == "freeforall":
        for goal in freeforall_goals:
            goals.append(pygame.Rect(goal))


def print_score(location):
    if location == "standard":
        text1 = FONT.render("-", True, (0, 0, 0))
        text2 = FONT.render(f"{red_score:02d}", True, (255, 0, 0))
        text3 = FONT.render(f"{blue_score:02d}", True, (0, 0, 255))

        text1_rect = text1.get_rect()

        WIN.blit(text1, (WIN_SIZE[0] / 2 - text1_rect.centerx, WIN_SIZE[1] // 100))
        WIN.blit(text2, (WIN_SIZE[0] / 2 - text1_rect.width * 4.4, WIN_SIZE[1] // 100))
        WIN.blit(text3, (WIN_SIZE[0] / 2 + text1_rect.width, WIN_SIZE[1] // 100))

    if location == "freeforall":
        text1 = FONT.render("-", True, (0, 0, 0))
        text2 = FONT.render(f"{red_score:02d}", True, (255, 0, 0))
        text3 = FONT.render(f"{blue_score:02d}", True, (0, 0, 255))
        text4 = FONT.render(f"{green_score:02d}", True, (0, 255, 0))
        text5 = FONT.render(f"{yellow_score:02d}", True, (255, 210, 0))

        text1_rect = text1.get_rect()

        WIN.blit(text1, (WIN_SIZE[0] / 2 - text1_rect.centerx, WIN_SIZE[1] // 20))
        WIN.blit(text4, (WIN_SIZE[0] / 2 - text1_rect.width * 4.4, WIN_SIZE[1] // 20))
        WIN.blit(text3, (WIN_SIZE[0] / 2 + text1_rect.width, WIN_SIZE[1] // 20))

        WIN.blit(text1, (WIN_SIZE[0] / 2 - text1_rect.centerx, WIN_SIZE[1] - text1_rect.height * 1.5))
        WIN.blit(text2, (WIN_SIZE[0] / 2 - text1_rect.width * 4.4, WIN_SIZE[1] - text1_rect.height * 1.5))
        WIN.blit(text5, (WIN_SIZE[0] / 2 + text1_rect.width, WIN_SIZE[1] - text1_rect.height * 1.5))

def countdown_start(red_x, red_y, blue_x, blue_y, puck_x, puck_y, spawn_pos="standard", green_x = 0, green_y = 0, yellow_x = 0, yellow_y = 0, score_location="standard"):
    for i in range(3, 0, -1):
        if spawn_pos == "standard":
            WIN.blit(STANDARD_BG, (0,0))
            WIN.blit(PUCK_MODEL, (puck_x, puck_y))
            WIN.blit(RED_MODEL, (red_x, red_y))
            WIN.blit(BLUE_MODEL, (blue_x, blue_y))
        
        if spawn_pos == "2v2":
            WIN.blit(TWOVSTWO_BG, (0,0))
            WIN.blit(GREEN_MODEL, (green_x, green_y))
            WIN.blit(YELLOW_MODEL, (yellow_x, yellow_y))
            WIN.blit(PUCK_MODEL, (puck_x, puck_y))
            WIN.blit(RED_MODEL, (red_x, red_y))
            WIN.blit(BLUE_MODEL, (blue_x, blue_y))

        if spawn_pos == "freeforall":
            WIN.blit(FREEFORALL_BG, (0,0))
            WIN.blit(GREEN_MODEL, (green_x, green_y))
            WIN.blit(YELLOW_MODEL, (yellow_x, yellow_y))
            WIN.blit(PUCK_MODEL, (puck_x, puck_y))
            WIN.blit(RED_MODEL, (red_x, red_y))
            WIN.blit(BLUE_MODEL, (blue_x, blue_y))
        
        print_score(score_location)

        pygame.display.update()
        text = FONT.render(f"{i}", True, (0, 0, 0))
        text_rect = text.get_rect()
        WIN.blit(text, (WIN_SIZE[0] / 2 - text_rect.centerx, WIN_SIZE[1] / 3))
        pygame.display.update()
        time.sleep(1)


def reset_game():
    global red_scored, blue_scored, green_scored, yellow_scored, last_touch
    if red_scored:
        red_scored = False
        return "red"
    if blue_scored:
        blue_scored = False
        return "blue"
    if green_scored:
        green_scored = False
        return "red"
    if yellow_scored:
        yellow_scored = False
        return "blue"
    

class Player:
    def __init__(self, color, puck, spawn_location="standard"):
        self.color = color
        if self.color == "red":
            self.image = RED_MODEL
        if self.color == "blue":
            self.image = BLUE_MODEL
        if self.color == "green":
            self.image = GREEN_MODEL
        if self.color == "yellow":
            self.image = YELLOW_MODEL

        if spawn_location == "standard":
            if self.color == "red":
                self.rect = pygame.Rect((WIN_SIZE[0] / 9, WIN_SIZE[1] / 2 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))
            if self.color == "blue":
                self.rect = pygame.Rect((WIN_SIZE[0] - WIN_SIZE[0] / 5, WIN_SIZE[1] - WIN_SIZE[1] / 2 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))

        if spawn_location == "2v2" or spawn_location == "freeforall":
            if self.color == "red":
                self.rect = pygame.Rect((WIN_SIZE[0] / 9, WIN_SIZE[1] / 4 * 3 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))
            if self.color == "blue":
                self.rect = pygame.Rect((WIN_SIZE[0] - WIN_SIZE[0] / 5, WIN_SIZE[1] - WIN_SIZE[1] / 4 * 3 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))                
            if self.color == "green":
                self.rect = pygame.Rect((WIN_SIZE[0] / 9, WIN_SIZE[1] / 4 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))
            if self.color == "yellow":
                self.rect = pygame.Rect((WIN_SIZE[0] - WIN_SIZE[0] / 5, WIN_SIZE[1] - WIN_SIZE[1] / 4 - PLAYER_WIDTH / 2), (PLAYER_WIDTH, PLAYER_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        # variable for mouse movement
        self.mouse = pygame.Surface((1, 1))
        self.mouse_mask = pygame.mask.from_surface(self.mouse)
        self.mouse_offset = [0, 0]
        self.drag = False

        # variables for touchscreen movement
        self.finger = pygame.Surface((1, 1))
        self.finger_mask = pygame.mask.from_surface(self.finger)
        self.dragging_finger = None
        self.drag_offset = (0, 0)

        # variables for physics
        self.x = self.rect.x
        self.y = self.rect.y
        self.old_x = 0
        self.old_y = 0

        self.vel_x = 0
        self.vel_y = 0
        self.nox = False
        self.noy = False

        self.friction = 0.75

        # make puck for collisions
        self.puck = puck


    def update(self, wall_type):
        self.physics()
        self.wall_collisions(wall_type)
        self.check_right_side_and_collisions(wall_type)
        


    def mouse_movement(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.mask.overlap(self.mouse_mask, (mouse_pos[0] - self.x, mouse_pos[1] - self.y)):
                    self.drag = True
                    self.mouse_offset[0] = self.x - mouse_pos[0]
                    self.mouse_offset[1] = self.y - mouse_pos[1]
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = False
                
        if event.type == pygame.MOUSEMOTION:
            if self.drag:
                self.x = mouse_pos[0] + self.mouse_offset[0]
                self.y = mouse_pos[1] + self.mouse_offset[1]


    def touchscreen_movement(self, event):
        if event.type == pygame.FINGERDOWN:
            x = int(event.x * WIN_SIZE[0])
            y = int(event.y * WIN_SIZE[1])

            # check if finger is on player
            if self.dragging_finger is None:
                offset_x = self.x - x
                offset_y = self.y - y
                if self.mask.overlap(self.finger_mask, (x - self.x, y - self.y)):
                    self.dragging_finger = event.finger_id
                    self.drag_offset = (offset_x, offset_y)

        if event.type == pygame.FINGERUP:
            # let go when finger is lifted
            if self.dragging_finger == event.finger_id:
                self.dragging_finger = None

        if event.type == pygame.FINGERMOTION:
            # update position when moving
            x = int(event.x * WIN_SIZE[0])
            y = int(event.y * WIN_SIZE[1])

            # move player when dragged
            if self.dragging_finger == event.finger_id:
                self.x = x + self.drag_offset[0]
                self.y = y + self.drag_offset[1]


    def physics(self):
        # calculate velocity
        if self.drag:
            self.vel_x = self.x - self.old_x
            self.vel_y = self.y - self.old_y

        # set velocity to 0 when close to 0
        if -0.3 <= self.vel_x <= 0.3:
            self.vel_x = 0
        if -0.3 <= self.vel_y <= 0.3:
            self.vel_y = 0

        # make player slide
        if self.drag == False:
            self.x += self.vel_x
            self.y += self.vel_y

            self.vel_x *= self.friction
            self.vel_y *= self.friction
        
        self.rect.topleft = (self.x, self.y)

    
    def check_right_side_and_collisions(self, walls_type):
        if walls_type == "standard walls":
            if self.color == "red" and self.rect.colliderect(walls[4]):
                self.nox = True

            elif self.color == "blue" and self.rect.colliderect(walls[5]):
                self.nox = True
            
            elif self.color == "green" and self.rect.colliderect(walls[4]):
                self.nox = True
            
            elif self.color == "yellow" and self.rect.colliderect(walls[5]):
                self.nox = True
            
        if walls_type == "freeforall walls":
            if self.color == "green":
                if self.rect.colliderect(walls[7]):
                    self.noy = True
                if self.rect.colliderect(walls[8]):
                    self.nox = True
                if self.rect.colliderect(walls[9]):
                    self.nox = True
                    self.noy = True

            elif self.color == "red":
                if self.rect.colliderect(walls[6]):
                    self.noy = True
                if self.rect.colliderect(walls[8]):
                    self.nox = True
                    self.noy = True
                if self.rect.colliderect(walls[9]):
                    self.nox = True
            
            elif self.color == "blue":
                if self.rect.colliderect(walls[6]):
                    self.nox = True
                if self.rect.colliderect(walls[7]):
                    self.nox = True
                    self.noy = True
                if self.rect.colliderect(walls[9]):
                    self.noy = True
            
            elif self.color == "yellow":
                if self.rect.colliderect(walls[6]):
                    self.nox = True
                    self.noy = True
                if self.rect.colliderect(walls[7]):
                    self.nox = True
                if self.rect.colliderect(walls[8]):
                    self.noy = True
        
        self.collisions()

    
    def collisions(self):
        overlap = self.mask.overlap(self.puck.mask, (self.puck.x - self.x, self.puck.y - self.y))
        if overlap:
            global last_touch
            last_touch.append(self.color)
            # if len(last_touch) > 10:
            #     last_touch = last_touch[-10:]
            # if player is still reflect puck
            if self.vel_x == 0 and self.vel_y == 0:
                dx = self.puck.rect.centerx - self.rect.centerx
                dy = self.puck.rect.centery - self.rect.centery
                if abs(dx) > abs(dy):
                    self.puck.vel_x *= -1
                else:
                    self.puck.vel_y *= -1

            # give puck velocity
            else:
                if not self.nox:
                    self.puck.vel_x = self.vel_x
                else:
                    self.nox = False
                if not self.noy:
                    self.puck.vel_y = self.vel_y
                else:
                    self.noy = False

            # teleport puck outside player if overlapping
            dir_x = overlap[0] - self.rect.width // 2
            dir_y = overlap[1] - self.rect.height // 2

            length = (dir_x ** 2 + dir_y ** 2) ** 0.5
            if length > 0:
                dir_x /= length
                dir_y /= length

            self.puck.x += dir_x * 4
            self.puck.y += dir_y * 4


    def wall_collisions(self, walls_type):
        if self.rect.colliderect(walls[0]):
            self.vel_y *= -1
            self.y = walls[0].top
        if self.rect.colliderect(walls[1]):
            self.vel_x *= -1
            self.x = walls[1].left
        if self.rect.colliderect(walls[2]):
            self.vel_y *= -1
            self.y = walls[2].top - self.rect.height
        if self.rect.colliderect(walls[3]):
            self.vel_x *= -1
            self.x = walls[3].left - self.rect.width


        if walls_type == "standard walls":
            if self.color == "red":
                if self.rect.colliderect(walls[4]):
                    self.vel_x *= -1
                    self.x = walls[4].right - self.rect.width
            elif self.color == "blue":
                if self.rect.colliderect(walls[5]):
                    self.vel_x *= -1
                    self.x = walls[5].right
            elif self.color == "green":
                if self.rect.colliderect(walls[4]):
                    self.vel_x *= -1
                    self.x = walls[4].right - self.rect.width
            elif self.color == "yellow":
                if self.rect.colliderect(walls[5]):
                    self.vel_x *= -1
                    self.x = walls[5].right

        elif walls_type == "freeforall walls":
            if self.rect.colliderect(walls[4]):
                self.vel_y *= -1
                self.y = walls[4].bottom
            elif self.rect.colliderect(walls[5]):
                self.vel_y *= -1
                self.y = walls[5].top - self.rect.height

            if self.color == "green":
                if self.rect.colliderect(walls[7]):
                    self.vel_y *= -1
                    self.y = walls[7].top - self.rect.height
                if self.rect.colliderect(walls[8]):
                    self.vel_x *= -1
                    self.x = walls[8].left - self.rect.width
                if self.rect.colliderect(walls[9]):
                    self.x = walls[9].left - self.rect.width
                    self.y = walls[9].top - self.rect.height
            elif self.color == "red":
                if self.rect.colliderect(walls[6]):
                    self.vel_y *= -1
                    self.y = walls[6].bottom
                if self.rect.colliderect(walls[9]):
                    self.vel_x *= -1
                    self.x = walls[9].left - self.rect.width
                if self.rect.colliderect(walls[8]):
                    self.x = walls[8].left - self.rect.width
                    self.y = walls[8].bottom
            elif self.color == "blue":
                if self.rect.colliderect(walls[6]):
                    self.vel_x *= -1
                    self.x = walls[6].right
                if self.rect.colliderect(walls[7]):
                    self.x = walls[7].right
                    self.y = walls[7].top - self.rect.height
                if self.rect.colliderect(walls[9]):
                    self.vel_y *= -1
                    self.y = walls[9].top - self.rect.height
            elif self.color == "yellow":
                if self.rect.colliderect(walls[6]):
                    self.x = walls[6].right
                    self.y = walls[6].bottom
                if self.rect.colliderect(walls[7]):
                    self.vel_x *= -1
                    self.x = walls[7].right
                if self.rect.colliderect(walls[8]):
                    self.vel_y *= -1
                    self.y = walls[8].bottom





class Puck:
    def __init__(self, pos="normal"):
        self.image = PUCK_MODEL
        if pos == "normal":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH / 2, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "red side":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH * 2.3, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "blue side":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 + PUCK_WIDTH * 1.3, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))
        self.mask = pygame.mask.from_surface(PUCK_MODEL)

        # variables for physics
        self.x = self.rect.x
        self.y = self.rect.y
        self.vel_x = 0
        self.vel_y = 0

        self.friction = 0.97


    def update(self, walls_type, goals_type="standard"):
        self.physics()
        self.goal_collisions(goals_type)
        self.wall_collisions(walls_type)


    def physics(self):
        # set velocity to 0 when close to 0
        if -0.3 <= self.vel_x <= 0.3:
            self.vel_x = 0
        if -0.3 <= self.vel_y <= 0.3:
            self.vel_y = 0

        # update location
        self.x += self.vel_x
        self.y += self.vel_y

        # apply friction
        self.vel_x *= self.friction
        self.vel_y *= self.friction


        self.rect.topleft = (self.x, self.y)


    def goal_collisions(self, goals_type):
        global red_score, blue_score, green_score, yellow_score, blue_scored, red_scored, green_scored, yellow_scored
        if goals_type == "standard":
            if self.rect.colliderect(goals[0]):
                blue_score += 1
                blue_scored = True
            if self.rect.colliderect(goals[1]):
                red_score += 1
                red_scored = True

        if goals_type == "freeforall":
            global last_touch
            last_touch.reverse()
            for i in range(2):
                if self.rect.colliderect(goals[i]):
                    for touch in last_touch:
                        if touch == "green":
                            continue
                        elif touch == "red":
                            red_score += 1
                            red_scored = True
                            last_touch.clear()
                            break
                        elif touch == "blue":
                            blue_score += 1
                            blue_scored = True
                            last_touch.clear()
                            break
                        elif touch == "yellow":
                            yellow_score += 1
                            yellow_scored = True
                            last_touch.clear()
                            break

            for i in range(2):
                if self.rect.colliderect(goals[i + 2]):
                    for touch in last_touch:
                        if touch == "green":
                            green_score += 1
                            green_scored = True
                            last_touch.clear()
                            break
                        elif touch == "red":
                            continue
                        elif touch == "blue":
                            blue_score += 1
                            blue_scored = True
                            last_touch.clear()
                            break
                        elif touch == "yellow":
                            yellow_score += 1
                            yellow_scored = True
                            last_touch.clear()
                            break

            for i in range(2):
                if self.rect.colliderect(goals[i + 4]):
                    for touch in last_touch:
                        if touch == "green":
                            green_score += 1
                            green_scored = True
                            last_touch.clear()
                            break
                        elif touch == "red":
                            red_score += 1
                            red_scored = True
                            last_touch.clear()
                            break
                        elif touch == "blue":
                            continue
                        elif touch == "yellow":
                            yellow_score += 1
                            yellow_scored = True
                            last_touch.clear()
                            break

            for i in range(2):
                if self.rect.colliderect(goals[i + 6]):
                    for touch in last_touch:
                        if touch == "green":
                            green_score += 1
                            green_scored = True
                            last_touch.clear()
                            break
                        elif touch == "red":
                            red_score += 1
                            red_scored = True
                            last_touch.clear()
                            break
                        elif touch == "blue":
                            blue_score += 1
                            blue_scored = True
                            last_touch.clear()
                            break
                        elif touch == "yellow":
                            continue


    def wall_collisions(self, walls_type):
        if self.rect.colliderect(walls[0]):
            self.vel_y *= -1
            self.y = walls[0].top
        if self.rect.colliderect(walls[1]):
            self.vel_x *= -1
            self.x = walls[1].left
        if self.rect.colliderect(walls[2]):
            self.vel_y *= -1
            self.y = walls[2].top - self.rect.height
        if self.rect.colliderect(walls[3]):
            self.vel_x *= -1
            self.x = walls[3].left - self.rect.width

        if walls_type == "freeforall walls":
            if self.rect.colliderect(walls[4]):
                self.vel_y *= -1
                self.y = walls[4].bottom
            elif self.rect.colliderect(walls[5]):
                self.vel_y *= -1
                self.y = walls[5].top - self.rect.height
