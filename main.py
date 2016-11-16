
import math
from OpenGL.GL import *
from OpenGL.GLUT import *

from point import *
from hole import *
from ball import *


hole_coner = { Hole(-218,  218, 12), 
               Hole(   0, -218, 12),
               Hole(   0,  218, 12),
               Hole(-218, -218, 12) }
hole_edge  = { Hole(   0,    0, 13),
               Hole(-220,    0, 13) }

balls = {
    Ball(-110, -180, 0.24 / 2.0, 10, 1, 1, 1, 10)
}


# draw a circle whose centre is (x, y) and radius is r
def draw_circle(x, y, r):
    glBegin(GL_POLYGON)
    n = 200
    for i in range(n):
        tx = r * math.cos(2.0 * math.pi * i / n) + x
        ty = r * math.sin(2.0 * math.pi * i / n) + y
        glVertex2f(tx, ty)
    glEnd()


def calc():
    for u in [b for b in balls if b.enable]:
        vx = u.speed * math.cos(u.rad)
        vy = u.speed * math.sin(u.rad)
        u.x += vx
        u.y += vy

        u.speed = 0.995 * u.speed

        # if the ball drops, the ball is no longer enable
        for h in hole_coner:
            if math.fabs(u.x - h.x) + math.fabs(u.y - h.y) < (u.radius + h.radius) * 0.6:
                u.enable = False
        for h in hole_edge:    
            if math.fabs(u.x - h.x) + math.fabs(u.y - h.y) < (u.radius + h.radius) * 0.6:
                u.enable = False

        # if the coordinate exceeds the constraints,
        # recalculate the coordinate
        if (u.y + u.radius > 220):
            u.rad = 2 * math.pi - u.rad
            diff = u.y + u.radius - 220
            u.y -= diff
        elif (u.y - u.radius < -220):
            u.rad = 2 * math.pi - u.rad  
            diff = -(u.y - u.radius) - 220
            u.y += diff
        if (u.x + u.radius > 0):
            u.rad = math.pi - u.rad
            diff = u.x + u.radius
            u.x -= diff
        elif (u.x - u.radius < -220):
            u.rad = math.pi - u.rad  
            diff = -(u.x - u.radius) - 220
            u.x += diff


def draw():                
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw the billiards' table
    glColor3f(0.675, 0.285, 0.117)
    glRectf(-235/240.0, 235/240.0, 15/240.0, -235/24.0)
    glColor3f(0.0, 0.0, 0.0)
    for h in hole_edge:
        draw_circle(h.x / 240.0, h.y / 240.0, h.radius / 240.0)
    glColor3f(0.0, 0.332, 0.179)
    glRectf(-220/240.0, 220/240.0, 0.0, -220/240.0)
    glColor3f(0.0, 0.0, 0.0)
    for h in hole_coner:
        draw_circle(h.x / 240.0, h.y / 240.0, h.radius / 240.0)

    # draw balls
    # note that balls' point is given in absolute coordinate where
    # origin is (0, 0), so North-West corner is (-240, 240), 
    # South-East corner is (240, -240)

    for u in [b for b in balls if b.enable]:
        glColor3f(u.red, u.green, u.blue)
        draw_circle(u.x / 240.0, u.y / 240.0, u.radius / 240.0)

    glFlush()
    glutSwapBuffers()

def timer(value):
    calc()
    glutPostRedisplay()
    glutTimerFunc(20, timer, 0)


def fixsize(width, height):
    glutReshapeWindow(480, 480)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(480, 480)
glutCreateWindow("billiard with GA")
glutDisplayFunc(draw)
glutReshapeFunc(fixsize)
glutTimerFunc(20, timer, 0)
glutMainLoop()