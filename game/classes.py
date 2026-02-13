import pygame
import configparser
import os, sys
import ctypes
import time
import math
import random
import highscore as h
ctypes.windll.user32.SetProcessDPIAware()
pygame.display.init()
pygame.font.init()
pygame.joystick.init()
pygame.mixer.init()

pygame.display.set_caption('AirBlitz')

LOGO = pygame.image.load("assets/logo.png")
pygame.display.set_icon(LOGO)

joystick_count = pygame.joystick.get_count()

if joystick_count < 0:
    pygame.quit()

joysticks = [pygame.joystick.Joystick(i) for i in range(joystick_count)]
for joystick in joysticks:
    joystick.init()

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(__file__)

configParser = configparser.RawConfigParser()
configFilePath = os.path.join(base_path, "config.cfg")
configParser.read(configFilePath)

MOVEMENT_TYPE = int(configParser.get("Settings", "movement_type"))
VOLUME = float(configParser.get("Settings", "volume"))

def write_movement():
    configParser.set("Settings", "movement_type", str(MOVEMENT_TYPE))
    with open(configFilePath, "w") as config:
        configParser.write(config)

def write_volume():
    configParser.set("Settings", "volume", str(VOLUME))
    with open(configFilePath, "w") as config:
        configParser.write(config)

    START_GAME_SOUND.set_volume(VOLUME)
    GOAL1_SOUND.set_volume(VOLUME)
    GOAL2_SOUND.set_volume(VOLUME)
    GOAL3_SOUND.set_volume(VOLUME)
    HIT1_SOUND.set_volume(VOLUME)
    HIT2_SOUND.set_volume(VOLUME)
    HIT3_SOUND.set_volume(VOLUME)
    HIT4_SOUND.set_volume(VOLUME)
    HIT5_SOUND.set_volume(VOLUME)


START_GAME_SOUND = pygame.mixer.Sound("assets/audio/start_game.wav")

GOAL1_SOUND = pygame.mixer.Sound("assets/audio/goal1.wav")
GOAL2_SOUND = pygame.mixer.Sound("assets/audio/goal2.wav")
GOAL3_SOUND = pygame.mixer.Sound("assets/audio/goal3.wav")

GOAL_SOUNDS = [GOAL1_SOUND, GOAL2_SOUND, GOAL3_SOUND]

HIT1_SOUND = pygame.mixer.Sound("assets/audio/hit1.wav")
HIT2_SOUND = pygame.mixer.Sound("assets/audio/hit2.wav")
HIT3_SOUND = pygame.mixer.Sound("assets/audio/hit3.wav")
HIT4_SOUND = pygame.mixer.Sound("assets/audio/hit4.wav")
HIT5_SOUND = pygame.mixer.Sound("assets/audio/hit5.wav")

HIT_SOUNDS = [HIT1_SOUND, HIT2_SOUND, HIT3_SOUND, HIT4_SOUND, HIT5_SOUND]


START_GAME_SOUND.set_volume(VOLUME)
GOAL1_SOUND.set_volume(VOLUME)
GOAL2_SOUND.set_volume(VOLUME)
GOAL3_SOUND.set_volume(VOLUME)
HIT1_SOUND.set_volume(VOLUME)
HIT2_SOUND.set_volume(VOLUME)
HIT3_SOUND.set_volume(VOLUME)
HIT4_SOUND.set_volume(VOLUME)
HIT5_SOUND.set_volume(VOLUME)


WIN_SIZE = pygame.display.get_desktop_sizes()[0]

PLAYER_WIDTH, PLAYER_HEIGHT = WIN_SIZE[0] * 0.09375, WIN_SIZE[1] * 0.1666666666666667
PUCK_WIDTH, PUCK_HEIGHT = WIN_SIZE[0] * 0.05625, WIN_SIZE[1] * 0.1

FONT = pygame.font.Font(None, WIN_SIZE[0] // 15)

ANOUNCE_FONT = pygame.font.Font(None, WIN_SIZE[0] // 10)

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
STANDARD_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/standard.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()
FREEFORALL_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/freeforall.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()
TWOVSTWO_BG = pygame.transform.scale(pygame.image.load("assets/backgrounds/2v2.png"), (WIN_SIZE[0], WIN_SIZE[1])).convert_alpha()

RED_MODEL = pygame.transform.scale(pygame.image.load("assets/players/red_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
BLUE_MODEL = pygame.transform.scale(pygame.image.load("assets/players/blue_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
GREEN_MODEL = pygame.transform.scale(pygame.image.load("assets/players/green_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
YELLOW_MODEL = pygame.transform.scale(pygame.image.load("assets/players/yellow_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
PUCK_MODEL = pygame.transform.scale(pygame.image.load("assets/players/puck.png"), (PUCK_WIDTH, PUCK_HEIGHT)).convert_alpha()

def reset_scores():
    # score variables
    global red_score, blue_score, green_score, yellow_score
    global red_scored, blue_scored, green_scored, yellow_scored, last_touch
    global in_red, in_blue, in_green, in_yellow

    red_score = 0
    blue_score = 0
    green_score = 0
    yellow_score = 0

    red_scored = False
    blue_scored = False
    green_scored = False
    yellow_scored = False
    last_touch = []

    in_red = False
    in_blue = False
    in_green = False
    in_yellow = False
reset_scores()

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


def print_score(location, minute_amount, second_amount=0):
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

    if location == "highscore":
        text1 = FONT.render(f"{red_score - blue_score:02d}", True, (255, 0, 0))

        text1_rect = text1.get_rect()

        WIN.blit(text1, (WIN_SIZE[0] / 2 - text1_rect.width * 4.4, WIN_SIZE[1] // 20))

        time_min = FONT.render(f"{minute_amount:02d}", True, (0, 0, 0))
        time_sec = FONT.render(f"{second_amount:02d}", True, (0, 0, 0))
        text = FONT.render(":", True, (0, 0, 0))

        text_rect = text.get_rect()

        WIN.blit(text, (WIN_SIZE[0] / 2 - text_rect.centerx, WIN_SIZE[1] // 20))
        WIN.blit(time_min, (WIN_SIZE[0] / 2 - text_rect.centerx * 8, WIN_SIZE[1] // 20))
        WIN.blit(time_sec, (WIN_SIZE[0] / 2 + text_rect.centerx * 1, WIN_SIZE[1] // 20))


def countdown_start(red_x, red_y, blue_x, blue_y, puck_x, puck_y, score_location="standard", spawn_pos="standard", green_x=0, green_y=0, yellow_x=0, yellow_y=0, puck4_x=0, puck4_y=0, puck5_x=0, puck5_y=0, puck6_x=0, puck6_y=0, puck7_x=0, puck7_y=0, puck8_x=0, puck8_y=0, puck9_x=0, puck9_y=0, minute_amount=0, second_amount=0, first_countdown=False):
    reverse_i = 0

    START_GAME_SOUND.play()

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

        if spawn_pos == "db":
            WIN.blit(STANDARD_BG, (0,0))
            WIN.blit(PUCK_MODEL, (puck_x, puck_y))
            WIN.blit(PUCK_MODEL, (green_x, green_y))
            WIN.blit(RED_MODEL, (red_x, red_y))
            WIN.blit(BLUE_MODEL, (blue_x, blue_y))

        if spawn_pos == "more":
            WIN.blit(STANDARD_BG, (0,0))
            WIN.blit(PUCK_MODEL, (puck_x, puck_y))
            WIN.blit(PUCK_MODEL, (green_x, green_y))
            WIN.blit(PUCK_MODEL, (yellow_x, yellow_y))
            WIN.blit(PUCK_MODEL, (puck4_x, puck4_y))
            WIN.blit(PUCK_MODEL, (puck5_x, puck5_y))
            WIN.blit(PUCK_MODEL, (puck6_x, puck6_y))
            WIN.blit(PUCK_MODEL, (puck7_x, puck7_y))
            WIN.blit(PUCK_MODEL, (puck8_x, puck8_y))
            WIN.blit(PUCK_MODEL, (puck9_x, puck9_y))
            WIN.blit(RED_MODEL, (red_x, red_y))
            WIN.blit(BLUE_MODEL, (blue_x, blue_y))

        if first_countdown:
            if i == 1:
                reverse_i = 3
            elif i == 2:
                reverse_i = 2
            elif i == 3:
                reverse_i = 1
        
        print_score(score_location, minute_amount, second_amount - reverse_i)

        pygame.display.update()
        text = FONT.render(f"{i}", True, (0, 0, 0))
        text_rect = text.get_rect()
        WIN.blit(text, (WIN_SIZE[0] / 2 - text_rect.centerx, WIN_SIZE[1] / 2.65))
        pygame.display.update()
        time.sleep(1)
    return second_amount - reverse_i
        


def reset_game():
    global red_scored, blue_scored, green_scored, yellow_scored
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


def reset_game_ffo():
    global in_red, in_blue, in_green, in_yellow
    if in_red:
        in_red = False
        return "red"
    if in_blue:
        in_blue = False
        return "blue"
    if in_green:
        in_green = False
        return "green"
    if in_yellow:
        in_yellow = False
        return "yellow"
    

def anounce_point(color):
    if color == "red":
        point = ANOUNCE_FONT.render("RED MADE A POINT", True, (255, 0, 0))
    if color == "blue":
        point = ANOUNCE_FONT.render("BLUE MADE A POINT", True, (0, 0, 255))
    if color == "green":
        point = ANOUNCE_FONT.render("GREEN MADE A POINT", True, (0, 255, 0))
    if color == "yellow":
        point = ANOUNCE_FONT.render("YELLOW MADE A POINT", True, (255, 210, 0))

    point_rect = point.get_rect()

    WIN.blit(point, (WIN_SIZE[0] / 2 - point_rect.centerx, WIN_SIZE[1] / 3))

    pygame.display.update()

    time.sleep(1)


def anounce_winner(color):
    if color == "red":
        win = ANOUNCE_FONT.render("RED WON", True, (255, 0, 0))
    if color == "blue":
        win = ANOUNCE_FONT.render("BLUE WON", True, (0, 0, 255))
    if color == "green":
        win = ANOUNCE_FONT.render("GREEN WON", True, (0, 255, 0))
    if color == "yellow":
        win = ANOUNCE_FONT.render("YELLOW WON", True, (255, 210, 0))

    point_rect = win.get_rect()

    WIN.blit(win, (WIN_SIZE[0] / 2 - point_rect.centerx, WIN_SIZE[1] / 3))

    pygame.display.update()

    time.sleep(2.5)


class Player:
    def __init__(self, color, puck, spawn_location, joystick_id=None, puck2="no puck", puck3="no puck", puck4="no puck", puck5="no puck", puck6="no puck", puck7="no puck", puck8="no puck", puck9="no puck"):
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

        # variables for joystick movement
        self.joystick_id = joystick_id

        self.up = False
        self.right = False
        self.down = False
        self.left = False 

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
        self.puck2 = puck2
        self.puck3 = puck3
        self.puck4 = puck4
        self.puck5 = puck5
        self.puck6 = puck6
        self.puck7 = puck7
        self.puck8 = puck8
        self.puck9 = puck9


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


    def arcade_movement(self, event):
        if self.joystick_id is None:
            return

        if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
            if event.joy != self.joystick_id:
                return

            button = event.button

            if event.type == pygame.JOYBUTTONDOWN:
                if button == 4:
                    self.up = True
                elif button == 6:
                    self.right = True
                elif button == 5:
                    self.down = True
                elif button == 7:
                    self.left = True

            elif event.type == pygame.JOYBUTTONUP:
                if button == 4:
                    self.up = False
                elif button == 6:
                    self.right = False
                elif button == 5:
                    self.down = False
                elif button == 7:
                    self.left = False

    def arcade_movement_outside_event(self):
        if self.up:
            self.y -= 25
        if self.right:
            self.x += 25
        if self.down:
            self.y += 25
        if self.left:
            self.x -= 25


    def keyboard_movement(self):
        if self.color == "red":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.y -= 25
            if keys[pygame.K_d]:
                self.x += 25
            if keys[pygame.K_s]:
                self.y += 25
            if keys[pygame.K_a]:
                self.x -= 25
        elif self.color == "blue":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_i]:
                self.y -= 25
            if keys[pygame.K_l]:
                self.x += 25
            if keys[pygame.K_k]:
                self.y += 25
            if keys[pygame.K_j]:
                self.x -= 25


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
        pucks = [self.puck, self.puck2, self.puck3, self.puck4, self.puck5, self.puck6, self.puck7, self.puck8, self.puck9]
        for puck in pucks:
            if puck != "no puck":

                overlap = self.mask.overlap(puck.mask, (puck.x - self.x, puck.y - self.y))
                if not overlap:
                    continue

                random.choice(HIT_SOUNDS).play()

                global last_touch
                last_touch.append(self.color)

                center_player = self.rect.center
                center_puck = puck.rect.center

                dx = center_puck[0] - center_player[0]
                dy = center_puck[1] - center_player[1]
                distance = math.hypot(dx, dy)
                if distance == 0:
                    continue

                normal_x = dx / distance
                normal_y = dy / distance

                if self.nox:
                    normal_x = 0
                    self.nox = False
                if self.noy:
                    normal_y = 0
                    self.noy = False

                length = math.hypot(normal_x, normal_y)
                if length == 0:
                    continue
                normal_x /= length
                normal_y /= length

                tangent_x = -normal_y
                tangent_y = normal_x

                rel_vel_x = puck.vel_x - self.vel_x
                rel_vel_y = puck.vel_y - self.vel_y

                vel_normal = rel_vel_x * normal_x + rel_vel_y * normal_y
                vel_tangent = rel_vel_x * tangent_x + rel_vel_y * tangent_y

                if abs(vel_normal) > 1.5:
                    vel_normal *= -1
                else:
                    vel_normal = 0

                puck.vel_x = vel_normal * normal_x + vel_tangent * tangent_x + self.vel_x
                puck.vel_y = vel_normal * normal_y + vel_tangent * tangent_y + self.vel_y

                overlap_depth = (self.rect.width / 2 + puck.rect.width / 2) - distance + 1
                if overlap_depth > 0:
                    puck.x += normal_x * overlap_depth
                    puck.y += normal_y * overlap_depth

                MAX_PUCK_SPEED = 200

                speed = math.hypot(puck.vel_x, puck.vel_y)
                if speed > MAX_PUCK_SPEED:
                    scale = MAX_PUCK_SPEED / speed
                    puck.vel_x *= scale
                    puck.vel_y *= scale
        

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


    def bot(self, ai_speed): # ai speed should be, easy: WIN_SIZE[1] / 108, normal: WIN_SIZE[1] / 72, hard: WIN_SIZE[1] / 54, imposible: WIN_SIZE[1] / 43, nuclear: WIN_SIZE[1] / 30
        deadzone = ai_speed
        rand = random.randint(-3, 3)

        if self.puck.rect.right < WIN_SIZE[0] / 2:
                
            if self.rect.centerx > WIN_SIZE[0] / 5 * 4 + deadzone:
                self.x -= ai_speed + rand
            elif self.rect.centerx < WIN_SIZE[0] / 5 * 4 - deadzone:
                self.x += ai_speed + rand

        # attack when on blue side
        elif self.puck.rect.right > WIN_SIZE[0] / 2 - WIN_SIZE[0]:
            if self.puck.rect.centerx < self.rect.centerx - deadzone:
                self.x -= ai_speed + rand
            elif self.puck.rect.centerx > self.rect.centerx + deadzone:
                self.x += ai_speed + rand

        if self.puck.rect.centery < self.rect.centery - deadzone:
            self.y -= ai_speed + rand
        elif self.puck.rect.centery > self.rect.centery + deadzone:
            self.y += ai_speed + rand



class Puck:
    def __init__(self, pos="normal"):
        self.image = PUCK_MODEL
        if pos == "normal":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH / 2, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "db 1":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH / 2, WIN_SIZE[1] / 2 - PUCK_WIDTH * 2.2), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "db 2":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH / 2, WIN_SIZE[1] / 2 + PUCK_WIDTH * 1.2), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "red side":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH * 2.3, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "blue side":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 + PUCK_WIDTH * 1.3, WIN_SIZE[1] / 2 - PUCK_HEIGHT / 2), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "red ffo":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH * 1.8, WIN_SIZE[1] / 2 + PUCK_HEIGHT * 0.8), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "blue ffo":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 + PUCK_WIDTH * 0.8, WIN_SIZE[1] / 2 - PUCK_HEIGHT * 1.8), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "green ffo":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 - PUCK_WIDTH * 1.8, WIN_SIZE[1] / 2 - PUCK_HEIGHT * 1.8), (PUCK_WIDTH, PUCK_HEIGHT))
        if pos == "yellow ffo":
            self.rect = pygame.Rect((WIN_SIZE[0] / 2 + PUCK_WIDTH * 0.8, WIN_SIZE[1] / 2 + PUCK_HEIGHT * 0.8), (PUCK_WIDTH, PUCK_HEIGHT))
        self.mask = pygame.mask.from_surface(PUCK_MODEL)

        # variables for physics
        self.x = self.rect.x
        self.y = self.rect.y
        self.vel_x = 0
        self.vel_y = 0

        self.friction = 0.97


    def update(self, walls_type, goals_type="standard"):
        self.physics()
        self.wall_collisions(walls_type)
        return self.goal_collisions(goals_type)


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

    def other_puck_collisions(self, other_puck):
        overlap = self.mask.overlap(other_puck.mask, (other_puck.x - self.x, other_puck.y - self.y))
        if not overlap:
            return

        center_self = (self.rect.centerx, self.rect.centery)
        center_other = (other_puck.rect.centerx, other_puck.rect.centery)

        dx = center_other[0] - center_self[0]
        dy = center_other[1] - center_self[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return

        normal_x = dx / distance
        normal_y = dy / distance

        tangent_x = -normal_y
        tangent_y = normal_x

        vel_self_normal = self.vel_x * normal_x + self.vel_y * normal_y
        vel_self_tangent = self.vel_x * tangent_x + self.vel_y * tangent_y

        vel_other_normal = other_puck.vel_x * normal_x + other_puck.vel_y * normal_y
        vel_other_tangent = other_puck.vel_x * tangent_x + other_puck.vel_y * tangent_y

        new_vel_self_normal = vel_other_normal
        new_vel_other_normal = vel_self_normal

        self.vel_x = new_vel_self_normal * normal_x + vel_self_tangent * tangent_x
        self.vel_y = new_vel_self_normal * normal_y + vel_self_tangent * tangent_y

        other_puck.vel_x = new_vel_other_normal * normal_x + vel_other_tangent * tangent_x
        other_puck.vel_y = new_vel_other_normal * normal_y + vel_other_tangent * tangent_y

        overlap_depth = (self.rect.width / 2 + other_puck.rect.width / 2) - distance + 1
        if overlap_depth > 0:
            self.x -= normal_x * overlap_depth / 2
            self.y -= normal_y * overlap_depth / 2
            other_puck.x += normal_x * overlap_depth / 2
            other_puck.y += normal_y * overlap_depth / 2


    def goal_collisions(self, goals_type):
        global red_score, blue_score, green_score, yellow_score, blue_scored, red_scored, green_scored, yellow_scored
        global in_red, in_blue, in_green, in_yellow
        if goals_type == "standard":
            if self.rect.colliderect(goals[0]):
                blue_score += 1
                blue_scored = True
                random.choice(GOAL_SOUNDS).play()
                anounce_point("blue")
            if self.rect.colliderect(goals[1]):
                red_score += 1
                red_scored = True
                random.choice(GOAL_SOUNDS).play()
                anounce_point("red")

        if goals_type == "more_pucks":
            if self.rect.colliderect(goals[0]):
                blue_score += 1
                random.choice(GOAL_SOUNDS).play()
                anounce_point("blue")
                return True
            if self.rect.colliderect(goals[1]):
                red_score += 1
                random.choice(GOAL_SOUNDS).play()
                anounce_point("red")
                return True

        if goals_type == "freeforall":
            global last_touch
            last_touch.reverse()
            for i in range(2):
                if self.rect.colliderect(goals[i]):
                    random.choice(GOAL_SOUNDS).play()
                    in_green = True
                    for touch in last_touch:
                        if touch == "green":
                            continue
                        elif touch == "red":
                            red_score += 1
                            red_scored = True
                            last_touch.clear()
                            anounce_point("red")
                            break
                        elif touch == "blue":
                            blue_score += 1
                            blue_scored = True
                            last_touch.clear()
                            anounce_point("blue")
                            break
                        elif touch == "yellow":
                            yellow_score += 1
                            yellow_scored = True
                            last_touch.clear()
                            anounce_point("yellow")
                            break

            for i in range(2):
                if self.rect.colliderect(goals[i + 2]):
                    random.choice(GOAL_SOUNDS).play()
                    in_red = True
                    for touch in last_touch:
                        if touch == "green":
                            green_score += 1
                            green_scored = True
                            last_touch.clear()
                            anounce_point("green")
                            break
                        elif touch == "red":
                            continue
                        elif touch == "blue":
                            blue_score += 1
                            blue_scored = True
                            last_touch.clear()
                            anounce_point("blue")
                            break
                        elif touch == "yellow":
                            yellow_score += 1
                            yellow_scored = True
                            last_touch.clear()
                            anounce_point("yellow")
                            break

            for i in range(2):
                if self.rect.colliderect(goals[i + 4]):
                    random.choice(GOAL_SOUNDS).play()
                    in_blue = True
                    for touch in last_touch:
                        if touch == "green":
                            green_score += 1
                            green_scored = True
                            last_touch.clear()
                            anounce_point("green")
                            break
                        elif touch == "red":
                            red_score += 1
                            red_scored = True
                            last_touch.clear()
                            anounce_point("red")
                            break
                        elif touch == "blue":
                            continue
                        elif touch == "yellow":
                            yellow_score += 1
                            yellow_scored = True
                            last_touch.clear()
                            anounce_point("yellow")
                            break

            for i in range(2):
                if self.rect.colliderect(goals[i + 6]):
                    random.choice(GOAL_SOUNDS).play()
                    in_yellow = True
                    for touch in last_touch:
                        if touch == "green":
                            green_score += 1
                            green_scored = True
                            last_touch.clear()
                            anounce_point("green")
                            break
                        elif touch == "red":
                            red_score += 1
                            red_scored = True
                            last_touch.clear()
                            anounce_point("red")
                            break
                        elif touch == "blue":
                            blue_score += 1
                            blue_scored = True
                            last_touch.clear()
                            anounce_point("blue")
                            break
                        elif touch == "yellow":
                            continue

        


    def wall_collisions(self, walls_type):
        if self.rect.colliderect(walls[0]):
            self.vel_y *= -1
            self.y = walls[0].top
            random.choice(HIT_SOUNDS).play()
        if self.rect.colliderect(walls[1]):
            self.vel_x *= -1
            self.x = walls[1].left
            random.choice(HIT_SOUNDS).play()
        if self.rect.colliderect(walls[2]):
            self.vel_y *= -1
            self.y = walls[2].top - self.rect.height
            random.choice(HIT_SOUNDS).play()
        if self.rect.colliderect(walls[3]):
            self.vel_x *= -1
            self.x = walls[3].left - self.rect.width
            random.choice(HIT_SOUNDS).play()

        if walls_type == "freeforall walls":
            if self.rect.colliderect(walls[4]):
                self.vel_y *= -1
                self.y = walls[4].bottom
                random.choice(HIT_SOUNDS).play()
            elif self.rect.colliderect(walls[5]):
                self.vel_y *= -1
                self.y = walls[5].top - self.rect.height
                random.choice(HIT_SOUNDS).play()



class Button:
    def __init__(self, x, y, image):
        self.original_image = image
        self.image = image

        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.15

        self.rect = self.image.get_rect(topleft=(x, y))

        self.hover = False
        self.action = False

    def draw(self):
        # smooth scaling
        self.scale += (self.target_scale - self.scale) * self.scale_speed

        new_size = (
            int(self.original_image.get_width() * self.scale),
            int(self.original_image.get_height() * self.scale)
        )

        self.image = pygame.transform.smoothscale(
            self.original_image, new_size
        )

        # center behouden
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

        WIN.blit(self.image, self.rect)

    def check_click(self, events):
        self.action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.hover = True
            self.target_scale = 1.2

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.action = True
        else:
            self.hover = False
            self.target_scale = 1.0

        return self.action
        

class Slider:
    def __init__(
        self,
        x, y, width,
        min_value, max_value, start_value,
        handle_radius=WIN_SIZE[1] / 54,
        line_height=WIN_SIZE[1] / 108,
        color=(255, 255, 255)
    ):
        self.x = x
        self.y = y
        self.width = width

        self.min = min_value
        self.max = max_value
        self.value = start_value

        self.handle_radius = handle_radius
        self.line_height = line_height
        self.color = color

        self.dragging = False

        self._update_handle_pos()

    def _update_handle_pos(self):
        ratio = (self.value - self.min) / (self.max - self.min)
        self.handle_x = self.x + ratio * self.width

    def _update_value_from_mouse(self, mouse_x):
        ratio = (mouse_x - self.x) / self.width
        ratio = max(0, min(1, ratio))
        self.value = self.min + ratio * (self.max - self.min)
        self._update_handle_pos()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) <= self.handle_radius and \
               abs(event.pos[1] - self.y) <= self.handle_radius:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value_from_mouse(event.pos[0])

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y - self.line_height // 2, self.width, self.line_height)
        )

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.handle_x), self.y),
            self.handle_radius
        )
