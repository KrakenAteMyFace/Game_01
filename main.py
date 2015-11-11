from math import atan2, degrees, pi
import pygame
import entity
import constants
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
    key = {"l": False,
           "r": False,
           "u": False,
           "d": False,
           "s": False}

    hud_front_img = pygame.image.load("resources/hud_front.png")
    hud_back_img = pygame.image.load("resources/hud_back.png")

    crosshair_img = pygame.image.load("resources/crosshair.png")
    crosshair_width = crosshair_img.get_width()
    crosshair_height = crosshair_img.get_height()
    crosshair_x = None
    crosshair_y = None

    player = entity.Player("resources/player.png")

    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
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

        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]

        crosshair_x = mx-(crosshair_width/2)
        crosshair_y = my-(crosshair_height/2)

        player.setKeys(key["u"], key["l"], key["d"], key["r"], key["s"])
        player.move()

        screen.fill(constants.COLOR_WHITE)

        screen.blit(crosshair_img, (crosshair_x, crosshair_y))
        player.draw(screen, mx, my)
        screen.blit(hud_back_img, (0, 580))
        pygame.draw.rect(screen, constants.COLOR_RED, [0, 580, int(player.health)*((constants.SCREEN_WIDTH/2)/player.health_max), 20])
        pygame.draw.rect(screen, constants.COLOR_GREEN, [(constants.SCREEN_WIDTH-(player.stamina_max*((constants.SCREEN_WIDTH/2)/player.stamina_max))), 580, int(player.stamina)*((constants.SCREEN_WIDTH/2)/player.stamina_max), 20])
        screen.blit(hud_front_img, (0, 580))


        pygame.display.flip()
        clock.tick(144)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
