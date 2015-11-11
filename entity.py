from math import atan2, degrees, pi
import pygame
import constants

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite):
        self.sprite = pygame.image.load(sprite)
        self.sprite_height = self.sprite.get_height()
        self.sprite_width = self.sprite.get_width()
        self.resetAttributes()

    def resetAttributes(self):
        self.keys = [False, False, False, False, False]

        self.x = constants.SCREEN_WIDTH/2
        self.y = constants.SCREEN_HEIGHT/2
        self.x_vel = 0.0
        self.y_vel = 0.0

        self.speed_run = 1.5
        self.speed_default = 0.7
        self.speed = self.speed_default
        self.acceleration = 0.1
        self.drag = 0.05

        self.stamina_max = 100
        self.stamina = self.stamina_max
        self.stamina_loss = 0.25
        self.stamina_regen = 0.1

        self.health_max = 100
        self.health = self.health_max

    def setKeys(self, w, a, s, d, ls):
        self.keys[0] = w
        self.keys[1] = a
        self.keys[2] = s
        self.keys[3] = d
        self.keys[4] = ls

    def move(self):
        if self.keys[4] and self.stamina > 1:
            self.speed = self.speed_run
            self.stamina -= self.stamina_loss
        elif not self.keys[4] and self.stamina < self.stamina_max:
            self.stamina += self.stamina_regen
            if self.stamina > self.stamina_max:
                self.stamina = self.stamina_max
            self.speed = self.speed_default
        else:
            self.speed = self.speed_default
        if self.stamina < 1:
            self.stamina = 1

        if self.keys[0] and self.y_vel > -self.speed:
            self.y_vel -= self.acceleration
        if self.keys[1] and self.x_vel > -self.speed:
            self.x_vel -= self.acceleration
        if self.keys[2] and self.y_vel < self.speed:
            self.y_vel += self.acceleration
        if self.keys[3] and self.x_vel < self.speed:
            self.x_vel += self.acceleration

        if not self.keys[0] and not self.keys[2] or self.y_vel > self.speed or -self.y_vel > self.speed:
            if self.y_vel > 0:
                self.y_vel -= self.drag
            elif self.y_vel < 0:
                self.y_vel += self.drag

        if not self.keys[1] and not self.keys[3] or self.x_vel > self.speed or -self.x_vel > self.speed:
            if self.x_vel > 0:
                self.x_vel -= self.drag
            elif self.x_vel < 0:
                self.x_vel += self.drag

        if self.x_vel > -self.drag and self.x_vel < self.drag:
            self.x_vel = 0
        if self.y_vel > -self.drag and self.y_vel < self.drag:
            self.y_vel = 0

        self.x += self.x_vel
        self.y += self.y_vel

    def getAngle(self, mx, my):
        self.delta_x = mx - self.x
        self.delta_y = my - self.y
        self.radians = atan2(-self.delta_y,self.delta_x)
        self.radians %= 2*pi
        return degrees(self.radians)-90

    def rotated(self, angle):
        self.orig_rect = self.sprite.get_rect()
        self.rot_image = pygame.transform.rotate(self.sprite, angle)
        self.rot_rect = self.orig_rect.copy()
        self.rot_rect.center = self.rot_image.get_rect().center
        self.rot_image = self.rot_image.subsurface(self.rot_rect).copy()
        return self.rot_image

    def displayX(self):
        self.real_x = self.x - (self.sprite_width/2)
        return self.real_x

    def displayY(self):
        self.real_y = self.y - (self.sprite_height/2)
        return self.real_y

    def draw(self, screen, mx, my):
        screen.blit(self.rotated(self.getAngle(mx,my)), (self.displayX(), self.displayY()))
