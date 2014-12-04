from __future__ import print_function

import os
import sys
import math
import random
import pygame as pg

global target
target = 2
global test
test = True
bitmap = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
BACKGROUND_COLOR = (30, 40, 50)
SCREEN_SIZE = (700, 500)
RECT_SIZE = (50, 50)
CAPTION = "Self Organization"
ARR = []



#START_BLOCKS = [(pg.Color("blue"), (350,400)), (pg.Color("blue"), (300,350)),(pg.Color("blue"), (300,400)), (pg.Color("blue"), (240,450)), (pg.Color("blue"), (180,450)), (pg.Color("blue"), (35,450)), (pg.Color("blue"), (90,450))]
START_BLOCKS = [(pg.Color("yellow"), (100,350)),(pg.Color("yellow"), (400,50)), (pg.Color("yellow"), (250,400)),  (pg.Color("yellow"), (200,150)),(pg.Color("yellow"), (100,250)), (pg.Color("yellow"), (400,150))]
#START_BLOCKS2 = [(pg.Color("red"), (100,350))]
#START_BLOCKS3 = [(pg.Color("blue"), (100,350))]
#add bitmap to visual representation. change this for scalability... and so it isn't programmed like shit.


STATIC_BLOCKS = [(pg.Color("green"), (350,400)), (pg.Color("green"), (300,350)),(pg.Color("green"), (300,400))]

if bitmap[8] == 1:
    STATIC_BLOCKS.append((pg.Color("gray"), (350,300)))
if bitmap[7] == 1:
    STATIC_BLOCKS.append((pg.Color("gray"), (400,300)))
if bitmap[0] == 1:
    STATIC_BLOCKS.append((pg.Color("gray"), (300,300)))
if bitmap[2] == 1:
    STATIC_BLOCKS.append((pg.Color("gray"), (350,350)))
if bitmap[3] == 1:
    STATIC_BLOCKS.append((pg.Color("gray"), (400,350)))
if bitmap[6] == 1:
    STATIC_BLOCKS.append((pg.Color("gray"), (400,400)))


def collide_other(one, two):
    """
    Callback function for use with pg.sprite.collidesprite methods.
    It simply allows a sprite to test collision against its own group,
    without returning false positives with itself.
    """
    return one is not two and pg.sprite.collide_rect(one, two)


class Block(pg.sprite.Sprite):
    """Our basic bouncing block."""

    def __init__(self, color, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(RECT_SIZE).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.true_pos = list(self.rect.center)
        self.velocity = [random.randint(-5, 5), random.randint(-5, 5)]
        #self.velocity = [0,0]
        self.unit_vector = self.get_unit_vector(self.velocity)
        self.rbool = False
        self.lbool = False
        self.ubool = False
        self.dbool = False
        self.quitRunning = True
        self.keepRunning = False

    def get_unit_vector(self, vector):
        """Return the unit vector of vector."""
        magnitude = math.hypot(*vector)
        if magnitude:
            return float(vector[0])/magnitude, float(vector[1])/magnitude
        else:
            return (0, 0)

    def update(self, screen_rect, others):
        """
        Update position; check collision with other blocks; and check
        collision with screen boundaries.
        """
        global test

        if(test or self.keepRunning):
            test = False
            self.keepRunning = True
            global target
            self.before_move = self.rect.copy()
            self.before_vel = self.velocity[:]
            # self.true_pos[0] += self.velocity[0]
            # self.true_pos[1] += self.velocity[1]
            if(self.quitRunning):

                coordinates = [[299,351,401,349],[349,401,401,349],[400,400,400,350],[350,350,351,299],[400,400,400,350],[300,300,300,250],[350,350,400,350],[349, 401,350,300],[399,451,301,249]]

                if bitmap[target] == 1:
                    right = coordinates[target][0]
                    left = coordinates[target][1]
                    up = coordinates[target][2]
                    down = coordinates[target][3]
                    # right = 451
                # left = 400
                # up = 400
                # down = 351
                #print ("target not reached")

                #print (target)
                if (self.true_pos[0]>right):
                    self.true_pos[0] -= 1
                else:
                    #print ("rbool")
                    self.rbool = True
                if (self.true_pos[0]<left):
                    self.true_pos[0] += 1
                    #print (self.true_pos[0],"left",left)
                else:
                    #print ("lbool")
                    self.lbool = True
                if (self.true_pos[1]>up):
                    self.true_pos[1] -= 1
                else:
                    #print ("ubool")
                    self.ubool = True
                if (self.true_pos[1]<down):
                    self.true_pos[1] += 1
                else:
                    #print ("dbool")
                    self.dbool = True
                if (self.dbool and self.ubool and self.lbool and self.rbool and self.quitRunning):
                    #self.velocity= [0,0]
                    print ("target = ", target)
                    target += 1
                    self.quitRunning = False
                    #print ("target reached")
                    print (target)
                    test = True
                    #self.keepRunning = False

                #print ("function target",target)
                self.rect.center = self.true_pos
                self.collide_walls(screen_rect)
                self.collide(others)

    def collide_walls(self, screen_rect):
        """
        Reverse relevent velocity component if colliding with edge of screen.
        """
        out_left = self.rect.left < screen_rect.left
        out_right = self.rect.right > screen_rect.right
        out_top = self.rect.top < screen_rect.top
        out_bottom = self.rect.bottom > screen_rect.bottom
        if out_left or out_right:
            self.velocity[0] *= -1
        if out_top or out_bottom:
            self.velocity[1] *= -1
        if any([out_left, out_right, out_top, out_bottom]):
            self.constrain(screen_rect)
            self.unit_vector = self.get_unit_vector(self.velocity)


    def goPlaces(self, others):
        """
        Check collision with other and switch components if hit.
        If collision can not be rectified, block is auto-killed.
        """
        count = 0
        other = None
        hit = pg.sprite.spritecollideany(self, others, collide_other)
        while hit:
            other = hit
            self.step_back()
            hit = pg.sprite.spritecollideany(self, others, collide_other)
            count += 1
            if count > 1000:
                self.kill()
                template = "Velocity: {velocity}, Unit: {unit_vector}"
                break
        if other:
            on_bottom = self.rect.bottom <= other.rect.top
            on_top = self.rect.top >= other.rect.bottom
            self.switch_components(other,on_bottom or on_top)

    def collide(self, others):
        """
        Check collision with other and switch components if hit.
        If collision can not be rectified, block is auto-killed.
        """
        count = 0
        other = None
        hit = pg.sprite.spritecollideany(self, others, collide_other)
        while hit:
            other = hit
            self.step_back()
            hit = pg.sprite.spritecollideany(self, others, collide_other)
            count += 1
            if count > 1000:
                self.kill()
                template = "Velocity: {velocity}, Unit: {unit_vector}"
                print("Rect: {}, Other: {}".format(self.rect, other.rect))
                print(template.format(**vars(self)))
                print("Unjustly murdered in collide.\n")
                break
        if other:
            on_bottom = self.rect.bottom <= other.rect.top
            on_top = self.rect.top >= other.rect.bottom
            self.switch_components(other,on_bottom or on_top)

    def switch_components(self, other, i):
        """Exchange the i component of velocity with other."""
        self.velocity[i],other.velocity[i] = other.velocity[i],self.velocity[i]
        self.unit_vector = self.get_unit_vector(self.velocity)
        other.unit_vector = other.get_unit_vector(other.velocity)

    def constrain(self, screen_rect):
        """
        Step back one unit pixel until contained within screen_rect.
        If the block is not contained within the screen after a number of
        iterations, it will be automaticaly killed.
        """
        count = 0
        rect_before = self.rect.copy()
        while not screen_rect.contains(self.rect):
            self.step_back()
            if count > 1000:
                self.kill()
                previous_info = "Before movement: {}, Before velocity: {}"
                rect_info = "Rect before: {}, Rect after: {}"
                break
            count += 1

    def step_back(self):
        """Decrement block's position by one unit pixel."""

        self.true_pos[0] -= self.unit_vector[0]
        self.true_pos[1] -= self.unit_vector[1]
        self.rect.center = self.true_pos


class Block2(pg.sprite.Sprite):
    """Our basic bouncing block."""
    def __init__(self, color, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(RECT_SIZE).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.true_pos = list(self.rect.center)
        #self.velocity = [random.randint(-5, 5), random.randint(-5, 5)]
        self.velocity = [0,0]
        self.unit_vector = self.get_unit_vector(self.velocity)

    def get_unit_vector(self, vector):
        """Return the unit vector of vector."""
        magnitude = math.hypot(*vector)
        if magnitude:
            return float(vector[0])/magnitude, float(vector[1])/magnitude
        else:
            return (0, 0)


class Control(object):
    """The big boss."""
    def __init__(self):
        pg.init()
        os.environ["SDL_VIDEO_CENTERED"] = "True"
        pg.display.set_caption(CAPTION)
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.blocks = pg.sprite.Group(Block(*args) for args in START_BLOCKS)
        self.blocks2 = pg.sprite.Group(Block2(*args) for args in STATIC_BLOCKS)
        #self.blocks3 = pg.sprite.Group(Block(*args) for args in START_BLOCKS2)
        #self.blocks4 = pg.sprite.Group(Block(*args) for args in START_BLOCKS3)


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def draw(self):
        """Fill the screen and draw all blocks."""
        self.screen.fill(BACKGROUND_COLOR)
        self.blocks2.draw(self.screen)
        self.blocks.draw(self.screen)
        #self.blocks3.draw(self.screen)
        #self.blocks4.draw(self.screen)

    def main_loop(self):
        #print(ARR)
        #target = 2
        while not self.done:
            self.event_loop()
            #print ("main target", target)

            self.blocks.update(self.screen_rect, self.blocks)
            #if(target==3):
            #    self.blocks3.update(self.screen_rect, self.blocks)
            #if(target==4):
            #    self.blocks4.update(self.screen_rect, self.blocks)
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    Control().main_loop()
    pg.quit()
    sys.exit()

