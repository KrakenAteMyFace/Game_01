import pygame
import sys

def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)

    key = {"l": False,
           "r": False,
           "u": False,
           "d": False}

    PLAYER_WIDTH = 10
    PLAYER_HEIGHT = 30

    player_x = (SCREEN_WIDTH/2)-(PLAYER_WIDTH/2)
    player_y = (SCREEN_HEIGHT/2)-(PLAYER_HEIGHT/2)
    player_xvel = 0.0000
    player_yvel = 0.0000

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game_01")
    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key["l"] = True
                elif event.key == pygame.K_RIGHT:
                    key["r"] = True
                elif event.key == pygame.K_UP:
                    key["u"] = True
                elif event.key == pygame.K_DOWN:
                    key["d"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key["l"] = False
                elif event.key == pygame.K_RIGHT:
                    key["r"] = False
                elif event.key == pygame.K_UP:
                    key["u"] = False
                elif event.key == pygame.K_DOWN:
                    key["d"] = False

        if key["l"] and player_xvel > -2:
            player_xvel-=0.1
        if key["r"] and player_xvel < 2:
            player_xvel+=0.1
        if key["u"] and player_yvel > -2:
            player_yvel-=0.1
        if key["d"] and player_yvel < 2:
            player_yvel+=0.1

        if not key["l"] and not key["r"]:
            if player_xvel > 0:
                player_xvel -= 0.01
            elif player_xvel < 0:
                player_xvel += 0.01
        if not key["u"] and not key["d"]:
            if player_yvel > 0:
                player_yvel -= 0.01
            elif player_yvel < 0:
                player_yvel += 0.01

        player_x += player_xvel
        player_y += player_yvel

        screen.fill(COLOR_WHITE)
        pygame.draw.rect(screen, COLOR_BLACK, [player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT])

        pygame.display.flip()
        clock.tick(144)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()