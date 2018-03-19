import pygame
from pygame.locals import *


class InputPoller(object):
    def __init__(self,potJoy1,potJoy2):
        self.joy1=potJoy1
        self.joy2=potJoy2
        self.p1Left=False
        self.p2Left=False
        self.p1Right=False
        self.p2Right=False
        self.p1Down=False
        self.p2Down=False
        self.p1Up=False
        self.p2Up=False
        self.p1Fire=False
        self.p2Fire=False
        self.p1Swipe=False
        self.p2Swipe=False
        self.quit=False
    
    def consumeEvents(self):

        #joystick dpad polling not an event
        if self.joy1 != None:

            buttons = self.joy1.get_numbuttons()
           # textPrint.print(screen, "Number of buttons: {}".format(buttons) )
            #textPrint.indent()

            for i in range( buttons ):
                button = self.joy1.get_button( i )
 #               print("b "+str(i)+" v "+str(button))
                if i==0:
                    if button==1:
                        self.p1Fire=True
                    else:
                        self.p1Fire=False
                if i==1:
                    if button==1:
                        self.p1Swipe=True
                    else:
                        self.p1Swipe=False
                

            axes = self.joy1.get_numaxes()
        
            for i in range( axes ):
                axis = self.joy1.get_axis( i )
  #              print("axis "+str(axis)) 
                #MAGIC 0 seems to be x
                if i==0:
                    if axis >0.8:
#                        print("jright")
                        self.p1Right=True
                        self.p1Left=False
                    elif axis<-0.8:
 #                       print("jleft")
                        self.p1Left=True
                        self.p1Right=False
                    else : #left nor right pressed
  #                      print("jnone")
                        self.p1Left=False
                        self.p1Right=False
                if i==1:
                    if axis >0.8:
                        self.p1Down=True
                        self.p1Up=False
                    elif axis<-0.8:
                        self.p1Down=False
                        self.p1Up=True
                    else : #left nor right pressed
                        self.p1Down=False
                        self.p1Up=False

        #joystick dpad polling not an event
        if self.joy2 != None:

            buttons = self.joy2.get_numbuttons()
           # textPrint.print(screen, "Number of buttons: {}".format(buttons) )
            #textPrint.indent()

            for i in range( buttons ):
                button = self.joy2.get_button( i )
 #               print("b "+str(i)+" v "+str(button))
                if i==0:
                    if button==1:
                        self.p2Fire=True
                    else:
                        self.p2Fire=False
                if i==1:
                    if button==1:
                        self.p2Swipe=True
                    else:
                        self.p2Swipe=False
                

            axes = self.joy2.get_numaxes()
        
            for i in range( axes ):
                axis = self.joy2.get_axis( i )
  #              print("axis "+str(axis)) 
                #MAGIC 0 seems to be x
                if i==0:
                    if axis >0.8:
#                        print("jright")
                        self.p2Right=True
                        self.p2Left=False
                    elif axis<-0.8:
 #                       print("jleft")
                        self.p2Left=True
                        self.p2Right=False
                    else : #left nor right pressed
  #                      print("jnone")
                        self.p2Left=False
                        self.p2Right=False
                if i==1:
                    if axis >0.8:
                        self.p2Down=True
                        self.p2Up=False
                    elif axis<-0.8:
                        self.p2Down=False
                        self.p2Up=True
                    else : #left nor right pressed
                        self.p2Down=False
                        self.p2Up=False

        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                self.quit=True
                #terminate()
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
#            elif event.type == JOYBUTTONDOWN:
                #print("Joystick button pressed.")
 #           elif event.type == pygame.JOYBUTTONUP:
                #print("Joystick button released.")

            elif event.type == KEYDOWN:
                if event.key == ( K_e):
                    self.p1Up=True
                elif event.key == (K_j):
                    self.p1Fire=True
                elif event.key == (K_k):
                    self.p1Swipe=True
                elif event.key == (K_d):
                    self.p1Down=True
                elif event.key == (K_s):
                    self.p1Left=True
                elif event.key == (K_f):
                    self.p1Right=True
                #now player 2
                elif event.key == (K_UP):
                    self.p2Up=True
                elif event.key == (K_DOWN):
                    self.p2Down=True                    
                elif event.key == (K_LEFT):
                    self.p2Left=True
                elif event.key == (K_RIGHT):
                    self.p2Right=True
                elif event.key == (K_KP0):
                    self.p2Fire=True
            elif event.type == KEYUP:
                if event.key == K_s:
                    self.p1Left=False
                elif event.key == (K_j):
                    self.p1Fire=False
                elif event.key == (K_k):
                    self.p1Swipe=False
                elif event.key == K_f:
                    self.p1Right=False
                elif event.key == K_e:
                    self.p1Up=False
                elif event.key == K_d:
                    self.p1Down=False
                    
                #ply2
                if event.key ==K_LEFT:
                    self.p2Left=False
                elif event.key == (K_RIGHT):
                    self.p2Right=False
                elif event.key == (K_KP0):
                    self.p2Fire=False
                elif event.key == (K_UP):
                    self.p2Up=False
                elif event.key == (K_DOWN):
                    self.p2Down=False
                elif event.key == K_ESCAPE:
                    self.quit=True
        
