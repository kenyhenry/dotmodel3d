from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from pygame import gfxdraw
import serial
import time


class plan3d:
    ser=""
    x=0
    y=0
    running=True
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

        # screen manager
        # pygame.display.set_mode((1030, 1030), pygame.OPENGL | pygame.DOUBLEBUF)
        glutInitWindowSize(1080, 1080)
        glutInitWindowPosition(0, 0)
        glutInitDisplayMode(GLUT_RGB)
        glutInit()
        glutCreateWindow("3d Plan")
        glutIdleFunc(self.process)
        glutDisplayFunc(self.plot_points)
        glutMainLoop()

    # draw utils
    def clearScreen(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        gluOrtho2D(-1.0, 1.0,-1.0,1.0)

    # point callback
    def plot_points(self):
        #no need to clear 
        # glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0,1.0,0.0)
        glPointSize(2.0)
        glBegin(GL_POINTS)
        print("x= ", self.x)
        glVertex3d(0, 0, self.x/1000)       # Added another Vertex specifying end coordinates of line
        glEnd()
        glFlush()

    # sensor callback
    def process(self):
        while(self.ser.in_waiting >= 9):
            if(('Y' == self.ser.read().decode("utf-8")) and ('Y' == self.ser.read().decode("utf-8"))):
                Dist_L = self.ser.read()
                Dist_H = self.ser.read()
                Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                self.x = Dist_Total
                for i in range (0,5):
                   self.ser.read()
               
                glutPostRedisplay()
                # clearScreen()

                print("dist L= ", ord(Dist_L), " dist H= ", ord(Dist_H), " dist total= ",Dist_Total)
            time.sleep(0.005)

def main():
    plan = plan3d()
    glutMainLoop()

if __name__ == '__main__':
    sys.exit(main())
