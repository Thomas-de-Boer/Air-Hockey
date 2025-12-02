import pygame, sys
mainClock = pygame.time.Clock()
from pygame.locals import*
pygame.init()

WINDOW_SIZE = pygame.display.get_desktop_sizes()[0]

WIN_WIDTH, WIN_HEIGHT = WINDOW_SIZE

pygame.display.set_caption('AirHockey')

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

BG = pygame.transform.scale(pygame.image.load("temp_multiplayer_bg.png"), (WIN_WIDTH, WIN_HEIGHT))

font = pygame.font.SysFont(None, 30)

def draw_text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


click = False


screen_width = screen.get_width()
screen_height = screen.get_height()


def menu():
    run = True
    positie = [0,0]
    while run == True:
        screen.blit(BG, [0,0])
        draw_text('Airhockey', font, (0,0,0), screen, 250, 40)
        mx, my = positie[0],positie[1]


        #buttons locatie/grootte
        button_multi = pygame.Rect(200,100,200,50)
        button_single = pygame.Rect(200,180,200,50)
        button_free = pygame.Rect(200,260,200,50)
        button_2v2 = pygame.Rect(200,340,200,50)
        button_double = pygame.Rect(200,420,200,50)
        button_obst = pygame.Rect(200,500,200,50)
        button_ex = pygame.Rect(200,580,200,50)

        #button kleur
        pygame.draw.rect(screen, (255,0,0), button_multi)
        pygame.draw.rect(screen, (255,0,0), button_single)
        pygame.draw.rect(screen, (255,0,0), button_free)
        pygame.draw.rect(screen, (255,0,0), button_2v2)
        pygame.draw.rect(screen, (255,0,0), button_double)
        pygame.draw.rect(screen, (255,0,0), button_obst)
        pygame.draw.rect(screen, (255,0,0), button_ex)

        #Tekst Button
        draw_text('Multiplayer', font,(255,255,255), screen, 203,115)
        draw_text('Singleplayer', font,(255,255,255), screen, 203,195)
        draw_text('4 Players free for all', font,(255,255,255), screen, 203,275)
        draw_text('2v2', font,(255,255,255), screen, 203,355)
        draw_text('Double puck', font,(255,255,255), screen, 203,435)
        draw_text('With obstacle', font,(255,255,255), screen, 203,515)
        draw_text('Exit game', font,(255,255,255), screen, 203,595)

        
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            #click effecten
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_multi.collidepoint(event.pos):
                        print("Multiplayer!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_single.collidepoint(event.pos):
                        print("singleplayer!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_free.collidepoint(event.pos):
                        print("free for all!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_2v2.collidepoint(event.pos):
                        print("2v2!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_double.collidepoint(event.pos):
                        print("Double ball")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_obst.collidepoint(event.pos):
                        print("More obstacles!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_ex.collidepoint(event.pos):
                      run = False

        pygame.display.update()
        mainClock.tick(60)

menu()