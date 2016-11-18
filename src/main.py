
import math
from OpenGL.GL import *
from OpenGL.GLUT import *

from point import *
from hole import *
from ball import *



eps = 1e-4

hole_coner = { Hole(-218,  218, 12), 
               Hole(   0, -218, 12),
               Hole(   0,  218, 12),
               Hole(-218, -218, 12) }
hole_edge  = { Hole(   0,    0, 13),
               Hole(-220,    0, 13) }

balls = {
    Ball(-110, -180, math.pi / 2.0 + 0.3, 13, 1, 1, 1, 10),
    Ball(-110,  80, 0, 0, 251/ 256.0, 236 / 256.0,  49 / 256.0, 10),
    Ball(-130, 130, 0, 0,   0/ 256.0,   0 / 256.0, 256 / 256.0, 10),
    Ball(-130,  50, 0, 0, 256/ 256.0,   0 / 256.0,   0 / 256.0, 10),
    Ball(-120, -70, 0, 0,   0/ 256.0,   0 / 256.0,   0 / 256.0, 10)
}

def euclid_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 +  (y2 - y1)**2)

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
        if u.speed < 0.3:
            u.speed = 0
            continue
        vx = u.speed * math.cos(u.rad)
        vy = u.speed * math.sin(u.rad)

        u.x += vx
        u.y += vy

        u.speed = 0.98 * u.speed

        # bump between two balls
        e = 0.7 #restitution
        for b in [b for b in balls if b.enable and u.id != b.id]:
            if euclid_distance(u.x, u.y, b.x, b.y) < u.radius + b.radius:
                vx2 = b.speed * math.cos(b.rad)
                vy2 = b.speed * math.sin(b.rad)
                nvx = ((1 - e) * vx + (1 + e) * vx2) * 0.5
                nvy = ((1 - e) * vy + (1 + e) * vy2) * 0.5
                nvx2 = ((1 + e) * vx + (1 - e) * vx2) * 0.5
                nvy2 = ((1 + e) * vy + (1 - e) * vy2) * 0.5

                u.speed = math.sqrt(nvx**2 + nvy**2)
                b.speed = math.sqrt(nvx2**2 + nvy2**2)

                if nvx2 == 0:
                    b.rad = 0
                else:
                    b.rad = math.atan2(nvy2,  nvx2)

                if nvx == 0:
                    u.rad = 0
                else:
                    u.rad = math.atan2(nvy, nvx)
               
                b.x += nvx
                b.y += nvy


            


        # if the balls drop, the balls are no longer enable.
        for h in hole_coner:
            if math.fabs(u.x - h.x) + math.fabs(u.y - h.y) < (u.radius + h.radius) * 0.9:
                u.enable = False
        for h in hole_edge:    
            if math.fabs(u.x - h.x) + math.fabs(u.y - h.y) < (u.radius + h.radius) * 0.9:
                u.enable = False

        # if the points exceeds the constraints,
        # recalculate the points.
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

    # draw the table
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
    # Note that balls' points are given in the way of absolute coordinate where
    # the origin is (0, 0) which is the centre of the window, so the North-West corner is (-240, 240) and
    # the South-East corner is (240, -240).

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