
import math
from OpenGL.GL import *
from OpenGL.GLUT import *

from point import *
from hole import *
from unit import *


hole_coner = { Hole(-0.89,  0.87, 0.06), 
               Hole(-0.89, -0.87, 0.06),
               Hole(-0.01,  0.87, 0.06),
               Hole(-0.01, -0.87, 0.06) }
hole_edge  = { Hole( 0.00,  0.00, 0.07),
               Hole(-0.91,  0.00, 0.07) }

unit = {
    Unit(-110, -180, math.pi / 2.0, 1, 1, 1, 1, 0.04)
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
    for u in unit:
        vx = u.speed * math.cos(u.rad)
        vy = u.speed * math.sin(u.rad)
        u.x += vx
        u.y += vy


def draw():                
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw the billiards' table
    glColor3f(0.675, 0.285, 0.117)
    glRectf(-0.98, 0.98, 0.08, -0.98)
    glColor3f(0.0, 0.0, 0.0)
    for h in hole_edge:
        draw_circle(h.x, h.y, h.radius)
    glColor3f(0.0, 0.332, 0.179)
    glRectf(-0.9, 0.9, 0.0, -0.9)
    glColor3f(0.0, 0.0, 0.0)
    for h in hole_coner:
        draw_circle(h.x, h.y, h.radius)

    # draw units
    # note that balls' point is given in absolute coordinate where
    # origin is (0, 0), so upper-left corner is (-240, 240), 
    # lower-right corner is (240, -240)

    for u in unit:
        glColor3f(u.red, u.green, u.blue)
        draw_circle(u.x / 240.0, u.y / 240.0, u.radius)

    glFlush()
    glutSwapBuffers()

def timer(value):
    calc()
    glutPostRedisplay()
    glutTimerFunc(10, timer, 0)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(480, 480)
glutCreateWindow("billiard with GA")
glutDisplayFunc(draw)
glutTimerFunc(10, timer, 0)
glutMainLoop()