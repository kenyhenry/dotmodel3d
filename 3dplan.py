from OpenGL.GL import *
from OpenGL.GL import shaders
# import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
import serial
import time
import sys

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
    view = Point(0,0,0)
    point = Point(0,0,0)
    time = time.time()
    clearTime = 5
    hold_mouse = False
    display = (1080, 1080)
    move_x = 0
    move_y = 0
    move_z = 0
    test = False

    def usage(self):
        print("usage : [-t = test_cube] [-c = clear periode in seconde]")
        print("full usage : [--test] [--clear]")

    def __init__(self):
        if(len(sys.argv) > 4):
            print("3dplan : wrong number of argument")
            self.usage()
            sys.exit()
        for i in range(1, len(sys.argv)):
            if(sys.argv[i] == "--test" or sys.argv[i] == "-t"):
                self.test = True
            elif(sys.argv[i] == "--clear" or sys.argv[i] == "-c"):
                i+=1
                self.clearTime=float(sys.argv[i])

        self.ser = serial.Serial('/dev/tty.usbserial-1422240',115200,timeout = 1)
        self.ser.write(0x42)
        self.ser.write(0x57)
        self.ser.write(0x02)
        self.ser.write(0x00)
        self.ser.write(0x00)
        self.ser.write(0x00)
        self.ser.write(0x01)
        self.ser.write(0x06)

        # window init
        glutInitWindowSize(self.display[0], self.display[1])
        glutInitWindowPosition(0, 0)
        glutInitDisplayMode(GLUT_RGB)
        glutInit()
        glutCreateWindow("3d Plan")
        glEnable(GL_DEPTH_TEST)

        # openGL calllback
        glutIdleFunc(self.process)
        glutDisplayFunc(self.plot_points)
        glutMotionFunc(self.mouseMotion)
        glutMouseFunc(self.mouseEvent)
        glutKeyboardFunc(self.keyboardEvent)
        # for some reason mouse wheel not implemented use 'z' 'x' keyboard
        # glutMouseWheelFunc(self.mouseWhl)

        glLoadIdentity()

        glutMainLoop()

    # clear screen
    def clearScreen(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        gluOrtho2D(-1.0, 1.0,-1.0,1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    # callbacks
    def plot_points(self):
        glColor3f(0.0,1.0,0.0)
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glVertex3d(0, self.point.x/1000, 0)
        glEnd()
        glFlush()

    def mouseMotion(self, x, y):
        if(self.hold_mouse == True):
            self.view.x = -1 * ((x - self.move_x)/10)
            self.view.y = -1 * ((y - self.move_y)/10)
            glRotatef(self.view.x, 1, 0, 0)
            glRotatef(self.view.y, 0, 1, 0)
            self.clearScreen()

    def mouseEvent(self, button, state, x, y):
        if(state == 0 and button == 0):
            self.move_x = x
            self.move_y = y
            self.hold_mouse = True
        # if(state == 1 and button == 0):
        #     glRotatef(self.view.x, 1, 0, 0)
        #     glRotatef(self.view.y, 0, 1, 0)
        #     glRotatef(self.view.z, 0, 0, 1)
        #     self.clearScreen()

    def mouseWhl(self, wheel, direction, x, y):
        print(wheel)
        print(direction)
        print(x)
        print(y)

    def keyboardEvent(self, key, x, y):
        if(key == b'q'):
             glutLeaveMainLoop()
        if(key == b' '):
            self.clearScreen()

        # move x by keyboard
        if(key == b'z'):
            self.view.x = self.move_x + 10
            glRotatef(self.view.x, 1, 0, 0)
            self.clearScreen()
        if(key == b'x'):
            self.view.x = self.move_x - 10
            glRotatef(self.view.x, 1, 0, 0)
            self.clearScreen()
        # move y by keyboard
        if(key == b'c'):
            self.view.y = self.move_y + 10
            glRotatef(self.view.y, 0, 1, 0)
            self.clearScreen()
        if(key == b'v'):
            self.view.y = self.move_y - 10
            glRotatef(self.view.y, 0, 1, 0)
            self.clearScreen()
        # move z by keyboard
        if(key == b'b'):
            self.view.z = self.move_z + 10
            glRotatef(self.view.z, 0, 0, 1)
            self.clearScreen()
        if(key == b'n'):
            self.view.z = self.move_z - 10
            glRotatef(self.view.z, 0, 0, 1)
            self.clearScreen()

    # get point
    def process(self):
        # get point of tfmini-s sensor
        while(self.ser.in_waiting >= 9):
            if(('Y' == self.ser.read().decode("utf-8")) and ('Y' == self.ser.read().decode("utf-8"))):
                Dist_L = self.ser.read()
                Dist_H = self.ser.read()
                Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                self.point.x = Dist_Total
                for i in range (0,5):
                   self.ser.read()
                glutPostRedisplay()
                # print("dist L= ", ord(Dist_L), " dist H= ", ord(Dist_H), " dist total= ",Dist_Total)
            time.sleep(0.005)

        if(self.test):
            self.DrawCube()

        # clear screen every self.clearTime "secondes
        if(time.time() > (self.time+self.clearTime)):
            self.time = time.time()
            self.clearScreen()

    def DrawCube(self):
        # Cube
        # White side - BACK
        glBegin(GL_POLYGON)
        glColor3f(   1.0,  1.0, 1.0 )
        glVertex3f(  0.5, -0.5, 0.5 )
        glVertex3f(  0.5,  0.5, 0.5 )
        glVertex3f( -0.5,  0.5, 0.5 )
        glVertex3f( -0.5, -0.5, 0.5 )
        glEnd()

        # Purple side - RIGHT
        glBegin(GL_POLYGON)
        glColor3f(  1.0,  0.0,  1.0 )
        glVertex3f( 0.5, -0.5, -0.5 )
        glVertex3f( 0.5,  0.5, -0.5 )
        glVertex3f( 0.5,  0.5,  0.5 )
        glVertex3f( 0.5, -0.5,  0.5 )
        glEnd()

        # Green side - LEFT
        glBegin(GL_POLYGON)
        glColor3f(   0.0,  1.0,  0.0 )
        glVertex3f( -0.5, -0.5,  0.5 )
        glVertex3f( -0.5,  0.5,  0.5 )
        glVertex3f( -0.5,  0.5, -0.5 )
        glVertex3f( -0.5, -0.5, -0.5 )
        glEnd()

        # Blue side - TOP
        glBegin(GL_POLYGON)
        glColor3f(   0.0,  0.0,  1.0 )
        glVertex3f(  0.5,  0.5,  0.5 )
        glVertex3f(  0.5,  0.5, -0.5 )
        glVertex3f( -0.5,  0.5, -0.5 )
        glVertex3f( -0.5,  0.5,  0.5 )
        glEnd()

        # Red side - BOTTOM
        glBegin(GL_POLYGON)
        glColor3f(   1.0,  0.0,  0.0 )
        glVertex3f(  0.5, -0.5, -0.5 )
        glVertex3f(  0.5, -0.5,  0.5 )
        glVertex3f( -0.5, -0.5,  0.5 )
        glVertex3f( -0.5, -0.5, -0.5 )
        glEnd()

        #TODO: Front side missing
        # Yellow side - FRONT
        # glBegin(GL_POLYGON)
        # glColor3f(   1.0,  1.0,  0.0 )
        # glVertex3f(  0.5, -0.5, 0.5 )
        # glVertex3f(  0.5, -0.5,  0.5 )
        # glVertex3f( -0.5, -0.5,  0.5 )
        # glVertex3f( -0.5, -0.5, -0.5 )
        # glEnd()

def main():
    plan = plan3d()
    glutMainLoopEvent()

if __name__ == '__main__':
    sys.exit(main())
