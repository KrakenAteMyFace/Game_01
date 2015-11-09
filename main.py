from math import atan2, degrees, pi
import pygame
import sys

def rotate(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def get_angle(x1, y1, x2, y2):
    diff_x = x2 - x1
    diff_y = y2 - y1
    rads = atan2(-diff_y,diff_x)
    rads %= 2*pi
    return degrees(rads)

def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    SCREEN_BUFFER_L = 0
    SCREEN_BUFFER_R = 0
    SCREEN_BUFFER_U = 0
    SCREEN_BUFFER_D = 20

    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (255, 0, 0)

    key = {"l": False,
           "r": False,
           "u": False,
           "d": False,
           "s": False}

    PLAYER_WIDTH = 24
    PLAYER_HEIGHT = 24
    PLAYER_RADIUS = 10

    PLAYER_MAXSPEED_RUN = 1.5
    PLAYER_MAXSPEED_DEFAULT = 0.7
    PLAYER_MAXSPEED = 0.7
    PLAYER_MAXSTAMINA = 100
    PLAYER_STAMINA = 100
    PLAYER_STAMINA_LOSS = 0.25
    PLAYER_STAMINA_REGEN = 0.1
    PLAYER_MAXHEALTH = 100
    PLAYER_HEALTH = 100
    PLAYER_ACCELERATION = 0.1
    PLAYER_SLOWDOWN = 0.05

    hud_front_img = pygame.image.load("resources/hud_front.png")
    hud_back_img = pygame.image.load("resources/hud_back.png")

    crosshair_img = pygame.image.load("resources/crosshair.png")
    crosshair_width = crosshair_img.get_width()
    crosshair_height = crosshair_img.get_height()
    crosshair_x = None
    crosshair_y = None

    mouse_x = None
    mouse_y = None

    player_img = pygame.image.load("resources/player.png")
    player_x = (SCREEN_WIDTH/2)-(PLAYER_WIDTH/2)
    player_y = (SCREEN_HEIGHT/2)-(PLAYER_HEIGHT/2)
    player_xvel = 0.0000
    player_yvel = 0.0000

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game_01")
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(False)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    key["l"] = True
                elif event.key == pygame.K_d:
                    key["r"] = True
                elif event.key == pygame.K_w:
                    key["u"] = True
                elif event.key == pygame.K_s:
                    key["d"] = True
                elif event.key == pygame.K_LSHIFT:
                    key["s"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    key["l"] = False
                elif event.key == pygame.K_d:
                    key["r"] = False
                elif event.key == pygame.K_w:
                    key["u"] = False
                elif event.key == pygame.K_s:
                    key["d"] = False
                elif event.key == pygame.K_LSHIFT:
                    key["s"] = False

        #GET MOUSE POSITION
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        #APPLY "RUN" SPEED MODIFIER
        if key["s"]:
            if PLAYER_STAMINA >= PLAYER_STAMINA_LOSS:
                PLAYER_MAXSPEED = PLAYER_MAXSPEED_RUN
                PLAYER_STAMINA -= PLAYER_STAMINA_LOSS
            else:
                PLAYER_MAXSPEED = PLAYER_MAXSPEED_DEFAULT
        else:
            if PLAYER_STAMINA < PLAYER_MAXSTAMINA:
                PLAYER_STAMINA += PLAYER_STAMINA_REGEN
            PLAYER_MAXSPEED = PLAYER_MAXSPEED_DEFAULT


        #CHANGE PLAYER VELOCITY BASED ON INPUTS
        if key["l"] and player_xvel > -PLAYER_MAXSPEED:
            if player_xvel <= 0:
                player_xvel = -player_xvel
                player_xvel += PLAYER_ACCELERATION
                player_xvel = -player_xvel
            else:
                player_xvel-=PLAYER_ACCELERATION
        if key["r"] and player_xvel < PLAYER_MAXSPEED:
            player_xvel+=PLAYER_ACCELERATION
        if key["u"] and player_yvel > -PLAYER_MAXSPEED:
            if player_yvel <= 0:
                player_yvel = -player_yvel
                player_yvel += PLAYER_ACCELERATION
                player_yvel = -player_yvel
            else:
                player_yvel-=PLAYER_ACCELERATION
        if key["d"] and player_yvel < PLAYER_MAXSPEED:
            player_yvel+=PLAYER_ACCELERATION

        #SLOW DOWN PLAYER IF NO MOVEMENT INPUT
        if not key["l"] and not key["r"] or player_xvel > PLAYER_MAXSPEED or -player_xvel > PLAYER_MAXSPEED:
            if player_xvel > 0:
                player_xvel -= PLAYER_SLOWDOWN
            elif player_xvel < 0:
                player_xvel += PLAYER_SLOWDOWN
        if not key["u"] and not key["d"] or player_yvel > PLAYER_MAXSPEED or -player_yvel > PLAYER_MAXSPEED:
            if player_yvel > 0:
                player_yvel -= PLAYER_SLOWDOWN
            elif player_yvel < 0:
                player_yvel += PLAYER_SLOWDOWN

        #REMOVE RECCURING DECIMAL SPEEDS
        if player_xvel > -PLAYER_SLOWDOWN and player_xvel < PLAYER_SLOWDOWN:
            player_xvel = 0
        if player_yvel > -PLAYER_SLOWDOWN and player_yvel < PLAYER_SLOWDOWN:
            player_yvel = 0

        #ADD THE VELOCITIES TO THE X AND Y POSITIONS AND CHECK BORDER COLLISION
        if (player_x+player_xvel)-(player_img.get_width()/2) > 0+SCREEN_BUFFER_L:
            if (player_x+player_xvel)+(player_img.get_width()/2) < SCREEN_WIDTH-SCREEN_BUFFER_R:
                player_x += player_xvel
        if (player_y+player_yvel)-(player_img.get_height()/2) > 0+SCREEN_BUFFER_U:
            if (player_y+player_yvel)+(player_img.get_height()/2) < SCREEN_HEIGHT-SCREEN_BUFFER_D:
                player_y += player_yvel

        #CALCULATE CROSSHAIR POSITION
        crosshair_x = mouse_x-(crosshair_width/2)
        crosshair_y = mouse_y-(crosshair_height/2)

        #CALCULATE PlAYER ROTATION/IMAGE AND POSITION
        player_img_rotated = rotate(player_img, get_angle(int(player_x), int(player_y), int(mouse_x), int(mouse_y))-90)

        #DRAW EVERYTHING TO THE SCREEN
        screen.fill(COLOR_WHITE)

        #pygame.draw.rect(screen, COLOR_BLACK, [player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT])

        screen.blit(player_img_rotated, (player_x-(player_img_rotated.get_width()/2), player_y-(player_img_rotated.get_height()/2)))

        screen.blit(crosshair_img, (crosshair_x, crosshair_y))

        screen.blit(hud_back_img, (0, 580))
        pygame.draw.rect(screen, COLOR_RED, [0, 580, int(PLAYER_HEALTH)*((SCREEN_WIDTH/2)/PLAYER_MAXHEALTH), 20])
        pygame.draw.rect(screen, COLOR_GREEN, [(SCREEN_WIDTH-(PLAYER_MAXSTAMINA*((SCREEN_WIDTH/2)/PLAYER_MAXSTAMINA))), 580, int(PLAYER_STAMINA)*((SCREEN_WIDTH/2)/PLAYER_MAXSTAMINA), 20])
        screen.blit(hud_front_img, (0, 580))


        #FLIP DISPLAY AND TICK CLOCK
        pygame.display.flip()
        clock.tick(144)


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
