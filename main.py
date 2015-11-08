import pygame
import sys

def rotate(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)

    key = {"l": False,
           "r": False,
           "u": False,
           "d": False}

    PLAYER_WIDTH = 24
    PLAYER_HEIGHT = 24
    PLAYER_RADIUS = 10

    PLAYER_MAXSPEED = 4
    PLAYER_ACCELERATION = 0.1
    PLAYER_SLOWDOWN = 0.05

    crosshair_img = pygame.image.load("resources/crosshair.png")
    crosshair_width = crosshair_img.get_width()
    crosshair_height = crosshair_img.get_height()
    crosshair_x = None
    crosshair_y = None

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    key["l"] = False
                elif event.key == pygame.K_d:
                    key["r"] = False
                elif event.key == pygame.K_w:
                    key["u"] = False
                elif event.key == pygame.K_s:
                    key["d"] = False

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
        if not key["l"] and not key["r"]:
            if player_xvel > 0:
                player_xvel -= PLAYER_SLOWDOWN
            elif player_xvel < 0:
                player_xvel += PLAYER_SLOWDOWN
        if not key["u"] and not key["d"]:
            if player_yvel > 0:
                player_yvel -= PLAYER_SLOWDOWN
            elif player_yvel < 0:
                player_yvel += PLAYER_SLOWDOWN

        #REMOVE RECCURING DECIMAL SPEEDS
        if player_xvel > -PLAYER_SLOWDOWN and player_xvel < PLAYER_SLOWDOWN:
            player_xvel = 0
        if player_yvel > -PLAYER_SLOWDOWN and player_yvel < PLAYER_SLOWDOWN:
            player_yvel = 0

        #ADD THE VELOCITIES TO THE X AND Y POSITIONS
        player_x += player_xvel
        player_y += player_yvel

        #CALCULATE CROSSHAIR POSITION
        crosshair_x = (pygame.mouse.get_pos()[0])-(crosshair_width/2)
        crosshair_y = (pygame.mouse.get_pos()[1])-(crosshair_height/2)

        screen.fill(COLOR_WHITE)
        #pygame.draw.rect(screen, COLOR_BLACK, [player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT])
        pygame.draw.circle(screen, COLOR_BLACK, (int(player_x), int(player_y)), PLAYER_RADIUS)
        screen.blit(crosshair_img, (crosshair_x, crosshair_y))

        pygame.display.flip()
        clock.tick(144)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
