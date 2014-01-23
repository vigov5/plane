from math import copysign
import os, sys
import pygame
from pygame.locals import *
import math

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

gravity = 0.05
acc = 0.05
MAX_VX = 3
MAX_VY = 3

class Plane(pygame.sprite.Sprite):

    step_angle = math.pi/72;

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/b0.png")
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.angle = math.pi/2
        self.key_states = {
            pygame.K_UP : False,
            pygame.K_DOWN : False,
            pygame.K_RIGHT : False,
            pygame.K_LEFT : False
        }

    def update(self):
        if abs(self.vx) > MAX_VX:
            self.vx = copysign(MAX_VX, self.vx)
        if abs(self.vy) > MAX_VY:
            self.vy = copysign(MAX_VY, self.vy)

        dy = self.vy
        dx = self.vx
        self.vy += gravity
        self.rect = self.rect.move(dx, dy)
        if self.rect.right > width or self.rect.left < 0:
            self.vx = -self.vx
        if self.rect.bottom > height:
            self.vy = -self.vy * 0.95
        #print self.key_states
        target_angle = self.angle
        if self.key_states[pygame.K_UP]:
            # pull to pi/2
            self.vy -= 0.1
            target_angle = -math.pi if self.angle < 0 else math.pi
        if self.key_states[pygame.K_DOWN]:
            self.vy += 0.1
            target_angle = 0

        if self.key_states[pygame.K_LEFT]:
            self.vx -= 0.1
            target_angle = -math.pi/2
        if self.key_states[pygame.K_RIGHT]:
            self.vx += 0.1
            target_angle = math.pi/2
        self.update_angle(target_angle)

        #

        images = {-8:4, -7:3, -6:2, -5:1, -4:0, -3:15, -2:14, -1:13, 0:12, 1:11, 2:10, 3:9, 4:8, 5:7, 6:6, 7:5, 8:4}
        #-8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8
        index = int(self.angle/(math.pi/8))
        # 4  3  2  1  0 15 14 13 12  11  10  9  8  7  6  5  4
        file_name= "imgs/b%d.png" % (images[index])
        self.image = pygame.image.load(file_name)


    def update_angle(self, target_angle):
        #print self.angle/math.pi, target_angle/math.pi

        if 0 <= self.angle < math.pi/2:
            print '1'
            if target_angle in [math.pi/2, math.pi]:
                self.angle += self.step_angle
            elif target_angle in [0, -math.pi/2]:
                self.angle -= self.step_angle

        elif math.pi/2 <= self.angle <= math.pi:
            print '2'
            if target_angle in [-math.pi/2, math.pi]:
                self.angle += self.step_angle
            elif target_angle in [0, math.pi/2]:
                self.angle -= self.step_angle

        elif -math.pi/2 <= self.angle < 0:
            print '3'
            if target_angle in [0, math.pi/2]:
                self.angle += self.step_angle
            elif target_angle in [-math.pi/2, -math.pi]:
                self.angle -= self.step_angle

        elif -math.pi <= self.angle < -math.pi/2:
            print '4'
            if target_angle in [0, -math.pi/2]:
                self.angle += self.step_angle
            elif target_angle in [math.pi/2, -math.pi]:
                self.angle -= self.step_angle

        if self.angle <= -math.pi:
            self.angle = math.pi
        elif self.angle >= math.pi:
            self.angle = -math.pi


    def draw(self, screen):
        cx, cy = self.rect.center
        #self.angle = math.atan(-self.vx/(self.vy + 0.001))
        end_point = (cx + 50 * math.sin(self.angle), cy + 50 * math.cos(self.angle))
        pygame.draw.line(screen, (255, 255, 255), self.rect.center, end_point)


    def handle(self, event):
        if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                if event.type == pygame.KEYDOWN:
                    self.key_states[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.key_states[event.key] = False



pygame.init()
size = width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

my_plane = Plane()

clock = pygame.time.Clock()
allsprites = pygame.sprite.RenderPlain(my_plane)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        for sprite in allsprites:
            sprite.handle(event)

    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Hello ", 1, (255, 0, 0))
        textpos = text.get_rect(centerx=width/2)

    screen.fill(black)
    allsprites.update()
    for sprite in allsprites:
        sprite.draw(screen)

    allsprites.draw(screen)
    screen.blit(text, textpos)
    pygame.display.flip()