import pygame as pg
import sys
from math import sin,cos,atan2,pi,sqrt
import numpy as np
import copy
from random import randint

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

def collisions_calc(v1,v2,t1,t2,phi,m1,m2):
    com = (v1*cos(t1-phi)*(m1-m2) + 2*m2*v2*cos(t2-phi)) / (m1+m2)
    vx = com * cos(phi) + v1*sin(t1-phi)*cos(phi+pi/2)
    vy = com * sin(phi) +v1*sin(t1-phi)*sin(phi+pi/2)
    return np.array([vx,vy])

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
    
    def collide2D(self,other):
        global collisions
        collisions += 1

        """
        v1 = np.linalg.norm(self.vel)
        v2 = np.linalg.norm(other.vel)
        t1 = atan2(self.vel[1],self.vel[0])
        t2 = atan2(other.vel[1],other.vel[0])
        phi = atan2(abs(other.vel[1]-self.vel[1]), abs(other.vel[0]-self.vel[0]))
        print(phi, t1, t2)

        velx = collisions_calc(v1,v2,t1,t2,phi,self.mass,other.mass)
        print(velx)

        self.vel = velx
        other.vel = collisions_calc(v2,v1,t2,t1,phi,other.mass,self.mass)"""

        v1 = (2*other.mass)/(self.mass+other.mass) * np.dot(self.vel-other.vel,self.pos-other.pos)/(np.linalg.norm(self.pos-other.pos)**2) * (self.pos-other.pos)
        v2 = (2*self.mass)/(other.mass+self.mass) * np.dot(other.vel-self.vel,other.pos-self.pos)/(np.linalg.norm(other.pos-self.pos)**2) * (other.pos-self.pos)

        self.vel -= v1
        other.vel -= v2

        self.collided[other.id] = True
        other.collided[self.id] = True        

    def main(self,objects):
        self.pos += self.vel

        pg.draw.circle(display,[255,0,0],self.pos + winsize/2,self.size)

        for x in objects:
            if x == self:
                continue
            if not(self.collided[x.id]) and (np.linalg.norm(self.pos-x.pos) <= self.size + x.size):
                self.collide2D(x)

        global collisions

        if abs(self.pos[0])+self.size >= winsize/2:
            collisions += 1
            self.vel[0] *= -1
        
        if abs(self.pos[1])+self.size >= winsize/2:
            collisions += 1
            self.vel[1] *= -1
        
objects = []
"""obj1 = Object([0.0,0.0],1,20)
obj1.vel[0] = 0.0
objects.append(obj1)

obj2 = Object([-100.0,-80.0],1,20)
obj2.vel[0] = 5.0
obj2.vel[1] = 5.0
objects.append(obj2)"""

for j in range(5):
    for i in range(14):
        obj = Object([-350.0+50.0*i,-200+j*100],1,5)
        obj.vel[0] = randint(-5,5)
        obj.vel[1] = randint(-5,5)
        objects.append(copy.copy(obj))

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

    #print(collisions)

    clock.tick(60)
    pg.display.update()