import pygame as pg
import sys
from math import sqrt,sin,cos,pi,factorial
import numpy as np
import copy

winsize = 800
display = pg.display.set_mode((winsize,winsize))
clock = pg.time.Clock()

idl = 0
collisions = 0

def initmasses():
    for x in objects:
        for y in objects:
            if x == y:
                continue
            x.masses[y.id] = np.array([(x.mass-y.mass)/(x.mass+y.mass),2*y.mass/(x.mass+y.mass)])
            x.collided[y.id] = False

class Object:

    def __init__(self,pos,mass,size):
        global idl
        self.id = str(idl)
        idl += 1
        self.pos = np.array(pos)
        self.mass = mass
        self.size = size
        self.vel = np.array([0.0,0.0])
        self.masses = {}
        self.collided = {}

    def collide(self,other):
        global collisions
        collisions += 1

        xvel = np.array([self.vel[0],other.vel[0]])

        self.vel[0] = np.dot(self.masses[other.id],xvel)
        other.vel[0] = np.dot(other.masses[self.id],np.flip(xvel))

        self.collided[other.id] = True
        other.collided[self.id] = True

    def main(self,objects):
        self.pos += self.vel

        pg.draw.circle(display,"white",self.pos + winsize/2,self.size)

        for x in objects:
            if x == self:
                continue
            if not(self.collided[x.id]) and (abs(self.pos[0]-x.pos[0]) <= self.size + x.size):
                self.collide(x)

        if abs(self.pos[0])+self.size >= winsize/2:
            global collisions
            collisions += 1
            self.vel[0] *= -1
        
objects = []
obj1 = Object([100.0,0.0],1,20)
obj1.vel[0] = 0.0
objects.append(obj1)

obj2 = Object([-100.0,0.0],100,20)
obj2.vel[0] = 1.0
objects.append(obj2)


initmasses()

while True:
    display.fill((0,0,0))


    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()

    for object in objects:
        object.main(objects)

    for object in objects:
        for x in object.collided:
            object.collided[x] = False

    print(collisions)

    clock.tick(60)
    pg.display.update()