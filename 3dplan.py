from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
import serial
import time
import numpy
import glm
def IdentityMat44(): return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')

class View:
    x=0
    y=0
    z=0

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    x=0
    y=0
    z=0

class plan3d:
    ser=""
    x=0
    y=0
    running=True
    view = View()
    viewMatrix = ""
    hold_mouse = False

    points = [Point(0.0, 0.0, 0.0)]

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
        self.ser.write(0x42)
        self.ser.write(0x57)
        self.ser.write(0x02)
        self.ser.write(0x00)
        self.ser.write(0x00)
        self.ser.write(0x00)
        self.ser.write(0x01)
        self.ser.write(0x06)

        # window init
        glutInitWindowSize(1080, 1080)
        glutInitWindowPosition(0, 0)
        glutInitDisplayMode(GLUT_RGB)
        glutInit()
        glutCreateWindow("3d Plan")

        # openGL calllback
        glutIdleFunc(self.process)
        glutDisplayFunc(self.plot_points)
        glutMotionFunc(self.mouseMotion)
        glutMouseFunc(self.mouseEvent)
        
        # openGl perspective
        self.viewMatrix = IdentityMat44()
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, 0, 0.5, 0, 0, 0, 0, 1, 0)
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        glutMainLoop()

    def redraw(self):
        for point in self.points:
            glColor3f(0.0,1.0,0.0)
            glPointSize(2.0)
            glBegin(GL_POINTS)
            glVertex3d(point.x, point.y, point.z)
            glEnd()
            glFlush()

    # draw utils
    def clearScreen(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        gluOrtho2D(-1.0, 1.0,-1.0,1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    # point callback
    def plot_points(self):
        glColor3f(0.0,1.0,0.0)
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glVertex3d(0, self.x/1000, 0)
        glEnd()
        glFlush()

    def mouseMotion(self, x, y):
        if(self.hold_mouse == True):
            print("x=", x)
            print("y=", y)
            self.view.x = self.view.x + x/1000
            self.view.y = self.view.y + y/1000
            
    def mouseEvent(self, button, state, x, y):
        if(state == 0 and button == 0):
            self.hold_mouse = True
        if(state == 1 and button == 0):
            gluLookAt(0, self.view.x, 0.5, 0, 0, 0, 0, 1, 0)
            glm.lookAt(glm.vec3(self.view.y,0,0), glm.vec3(self.view.x,0,0), glm.vec3(0,0,0))
            glLoadIdentity()
            # gluLookAt(0, 0, 0.5, self.view.x/1000, self.view.x/1000, 0, 0, 1, 0)
            glRotatef(self.view.x, 0, 0, 1)
            glRotatef(self.view.y, 0, 0, 1)
            glPushMatrix()
            glLoadIdentity()
            glRotatef(self.view.x, 0, 0, 1)
            glPopMatrix()
            glMultMatrixf(self.viewMatrix)
            viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.redraw()
            gluLookAt(0,0,0, 0,0,0, 0,0,0);


    # sensor callback
    def process(self):
        while(self.ser.in_waiting >= 9):
            if(('Y' == self.ser.read().decode("utf-8")) and ('Y' == self.ser.read().decode("utf-8"))):
                Dist_L = self.ser.read()
                Dist_H = self.ser.read()
                Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                self.x = Dist_Total
                self.points.append(Point(0,Dist_Total/1000,0))
                for i in range (0,5):
                   self.ser.read()
               
                # clear screen delete all dot already draw
                # self.clearScreen()

                glutPostRedisplay()

                # print("dist L= ", ord(Dist_L), " dist H= ", ord(Dist_H), " dist total= ",Dist_Total)
            time.sleep(0.005)

def main():
    plan = plan3d()
    glutMainLoop()

if __name__ == '__main__':
    sys.exit(main())
