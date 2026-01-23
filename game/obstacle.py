import pygame
import ctypes
import math

# Scherm scherp maken op Windows
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

# Fullscreen
WIN_SIZE = pygame.display.get_desktop_sizes()[0]
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Air Hockey - Volledige Game")

# === CONSTANTEN ===
PLAYER_WIDTH = int(WIN_SIZE[0] * 0.09375)
PLAYER_HEIGHT = int(WIN_SIZE[1] * 0.1666666666666667)
PUCK_SIZE = int(WIN_SIZE[0] * 0.05625)

PUCK_FRICTION = 0.97
PLAYER_FRICTION = 0.75
PUSH_STRENGTH = 5.0
KICK_STRENGTH = 7.0
MAX_SCORE = 7

# === ASSETS ===
BG = pygame.transform.scale(pygame.image.load("assets/standard_background.png"), WIN_SIZE).convert_alpha()
RED_MODEL = pygame.transform.scale(pygame.image.load("assets/red_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
BLUE_MODEL = pygame.transform.scale(pygame.image.load("assets/blue_player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
PUCK_MODEL = pygame.transform.scale(pygame.image.load("assets/puck.png"), (PUCK_SIZE, PUCK_SIZE)).convert_alpha()

# Pixel-perfect collision masks
RED_MASK = pygame.mask.from_surface(RED_MODEL)
BLUE_MASK = pygame.mask.from_surface(BLUE_MODEL)
PUCK_MASK = pygame.mask.from_surface(PUCK_MODEL)

# Fonts
FONT_BIG = pygame.font.SysFont("Arial", 120, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 80)

# === OBJECTEN ===
red = pygame.Rect(WIN_SIZE[0] // 9, WIN_SIZE[1] // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
blue = pygame.Rect(WIN_SIZE[0] - WIN_SIZE[0] // 5, WIN_SIZE[1] // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
puck = pygame.Rect(WIN_SIZE[0] // 2 - PUCK_SIZE // 2, WIN_SIZE[1] // 2 - PUCK_SIZE // 2, PUCK_SIZE, PUCK_SIZE)

# Middenlijn (voor botsing)
CENTER_LINE = pygame.Rect(WIN_SIZE[0] // 2 - 5, 0, 10, WIN_SIZE[1])

# Scores
red_score = blue_score = 0

# Snelheden
red_vel_x = red_vel_y = blue_vel_x = blue_vel_y = puck_vel_x = puck_vel_y = 0
red_old = red.topleft
blue_old = blue.topleft

# Input status
red_drag = blue_drag = False
red_offset = blue_offset = (0, 0)
red_finger = blue_finger = None

# === FUNCTIE: Ronde resetten ===
def reset_round():
    global puck_vel_x, puck_vel_y, red_vel_x, red_vel_y, blue_vel_x, blue_vel_y
    red.topleft = (WIN_SIZE[0] // 9, WIN_SIZE[1] // 2 - PLAYER_HEIGHT // 2)
    blue.topleft = (WIN_SIZE[0] - WIN_SIZE[0] // 5, WIN_SIZE[1] // 2 - PLAYER_HEIGHT // 2)
    puck.center = (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2)
    puck_vel_x = puck_vel_y = red_vel_x = red_vel_y = blue_vel_x = blue_vel_y = 0
    pygame.time.wait(800)

# === MAIN LOOP ===
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # --- MUIS ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if not red_drag:
                offset = RED_MASK.overlap(pygame.mask.from_surface(pygame.Surface((1,1))), (mx - red.x, my - red.y))
                if offset:
                    red_drag = True
                    red_offset = (red.x - mx, red.y - my)
            if not blue_drag:
                offset = BLUE_MASK.overlap(pygame.mask.from_surface(pygame.Surface((1,1))), (mx - blue.x, my - blue.y))
                if offset:
                    blue_drag = True
                    blue_offset = (blue.x - mx, blue.y - my)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            red_drag = blue_drag = False

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if red_drag:
                red.topleft = (mx + red_offset[0], my + red_offset[1])
            if blue_drag:
                blue.topleft = (mx + blue_offset[0], my + blue_offset[1])

        # --- TOUCHSCREEN ---
        if event.type == pygame.FINGERDOWN:
            x = int(event.x * WIN_SIZE[0])
            y = int(event.y * WIN_SIZE[1])
            if red_finger is None:
                if RED_MASK.overlap(pygame.mask.from_surface(pygame.Surface((1,1))), (x - red.x, y - red.y)):
                    red_finger = event.finger_id
                    red_offset = (red.x - x, red.y - y)
            if blue_finger is None:
                if BLUE_MASK.overlap(pygame.mask.from_surface(pygame.Surface((1,1))), (x - blue.x, y - blue.y)):
                    blue_finger = event.finger_id
                    blue_offset = (blue.x - x, blue.y - y)

        if event.type == pygame.FINGERUP:
            if red_finger == event.finger_id: red_finger = None
            if blue_finger == event.finger_id: blue_finger = None

        if event.type == pygame.FINGERMOTION:
            x = int(event.x * WIN_SIZE[0])
            y = int(event.y * WIN_SIZE[1])
            if red_finger == event.finger_id:
                red.topleft = (x + red_offset[0], y + red_offset[1])
            if blue_finger == event.finger_id:
                blue.topleft = (x + blue_offset[0], y + blue_offset[1])

    # === PHYSICS ===
    red_vel_x = red.x - red_old[0]
    red_vel_y = red.y - red_old[1]
    blue_vel_x = blue.x - blue_old[0]
    blue_vel_y = blue.y - blue_old[1]
    red_old = red.topleft
    blue_old = blue.topleft

    # Spelers glijden als niet vastgehouden
    if not red_drag and red_finger is None:
        red.x += red_vel_x
        red.y += red_vel_y
        red_vel_x *= PLAYER_FRICTION
        red_vel_y *= PLAYER_FRICTION

    if not blue_drag and blue_finger is None:
        blue.x += blue_vel_x
        blue.y += blue_vel_y
        blue_vel_x *= PLAYER_FRICTION
        blue_vel_y *= PLAYER_FRICTION

    # Puck beweging
    puck.x += puck_vel_x
    puck.y += puck_vel_y
    puck_vel_x *= PUCK_FRICTION
    puck_vel_y *= PUCK_FRICTION
    if abs(puck_vel_x) < 0.3: puck_vel_x = 0
    if abs(puck_vel_y) < 0.3: puck_vel_y = 0

    # === COLLISIE MET SPELERS ===
    for player, mask, vel_x, vel_y in [(red, RED_MASK, red_vel_x, red_vel_y), (blue, BLUE_MASK, blue_vel_x, blue_vel_y)]:
        offset = (puck.x - player.x, puck.y - player.y)
        overlap = mask.overlap(PUCK_MASK, offset)
        if overlap:
            px, py = overlap
            cx, cy = player.width // 2, player.height // 2
            dx = px - cx
            dy = py - cy
            length = math.hypot(dx, dy) or 1
            nx, ny = dx / length, dy / length

            puck.x += nx * PUSH_STRENGTH
            puck.y += ny * PUSH_STRENGTH

            dot = puck_vel_x * nx + puck_vel_y * ny
            puck_vel_x = puck_vel_x - 2 * dot * nx + nx * KICK_STRENGTH + vel_x
            puck_vel_y = puck_vel_y - 2 * dot * ny + ny * KICK_STRENGTH + vel_y

    # === MUUR & MIDDENLIJN ===
    if puck.top <= 0: puck.top = 0; puck_vel_y *= -1
    if puck.bottom >= WIN_SIZE[1]: puck.bottom = WIN_SIZE[1]; puck_vel_y *= -1
    if puck.colliderect(CENTER_LINE):
        if puck.centerx < WIN_SIZE[0] // 2:
            puck.right = CENTER_LINE.left
        else:
            puck.left = CENTER_LINE.right
        puck_vel_x *= -1

    # Spelers binnen hun helft houden
    red.clamp_ip(pygame.Rect(0, 0, WIN_SIZE[0]//2 - 50, WIN_SIZE[1]))
    blue.clamp_ip(pygame.Rect(WIN_SIZE[0]//2 + 50, 0, WIN_SIZE[0]//2, WIN_SIZE[1]))

    # === SCORING ===
    if puck.left < -100:
        blue_score += 1
        reset_round()
    if puck.right > WIN_SIZE[0] + 100:
        red_score += 1
        reset_round()

    # === TEKENEN ===
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, (80, 80, 80), CENTER_LINE)

    WIN.blit(RED_MODEL, red.topleft)
    WIN.blit(BLUE_MODEL, blue.topleft)
    WIN.blit(PUCK_MODEL, puck.topleft)

    # Score
    red_text = FONT_BIG.render(str(red_score), True, (220, 20, 20))
    blue_text = FONT_BIG.render(str(blue_score), True, (20, 20, 220))
    WIN.blit(red_text, (WIN_SIZE[0]//4 - red_text.get_width()//2, 50))
    WIN.blit(blue_text, (3*WIN_SIZE[0]//4 - blue_text.get_width()//2, 50))

    pygame.display.update()

    # === WINSTSCHERM ===
    if red_score >= MAX_SCORE or blue_score >= MAX_SCORE:
        winner = "ROOD" if red_score >= MAX_SCORE else "BLAUW"
        text1 = FONT_BIG.render(f"{winner} WINT!", True, (255, 255, 255))
        text2 = FONT_MED.render("Druk op ESC om af te sluiten", True, (200, 200, 200))
        WIN.blit(text1, (WIN_SIZE[0]//2 - text1.get_width()//2, WIN_SIZE[1]//3))
        WIN.blit(text2, (WIN_SIZE[0]//2 - text2.get_width()//2, WIN_SIZE[1]//2))
        pygame.display.update()
        pygame.time.wait(5000)
        running = False

pygame.quit()