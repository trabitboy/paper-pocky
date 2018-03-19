import collutil

LEFT = 'left'
RIGHT = 'right'
DOWN ='down'
UP='up'

bulletSpeed=20
timeNoBullet=4
globStepWipe=40

class Player(object):
    def __init__(self,body_left_img,body_right_img,wipe_img,down_img,up_img,left_img,right_img,direction,lvl):
##        global L_POCK_IMG
        self.left_img=left_img
        self.right_img=right_img
        self.down_img=down_img
        self.up_img=up_img
        #default init 
        self.head_img=down_img
        
        self.x=400
        self.y=200
        self.l_img=body_left_img
        self.r_img=body_right_img
        self.surface=self.l_img
        self.facing= direction
        ##self.x': HALF_WINWIDTH,
        ##'y': HALF_WINHEIGHT,
        self.bounce=0
        self.moveDown=False
        self.moveUp=False
        self.moveLeft=False
        self.moveRight=False
        self.fire=False
        self.inhibFire=0 # to have smooth flow of cards like pocky roky
        self.wipe=False #defense flag,triggers wipe
        self.wipeFw=True #is the wipe going or going back
        self.wipe_img=wipe_img
        self.xWipe=0
        self.yWipe=0
        self.stepWipe=0#both init on wipe triger
        self.maxStepWipe=wipe_img.get_width()+body_left_img.get_width()
        self.currentlyWiping=False
        self.MOVERATE = 9         # how fast the player moves
        self.BOUNCERATE = 6       # how fast the player bounces (large is slower)
        self.BOUNCEHEIGHT = 30    # how high the player bounces
        self.cur_lvl=lvl
        self.bullets=[]
        #debug test
        self.fire_bullet()

    def get_bul_vx(self):
        if self.facing==LEFT:
            return -bulletSpeed
        elif self.facing==RIGHT:
            return bulletSpeed
        else:
            return 0

    def get_bul_vy(self):
        if self.facing==UP:
            return -bulletSpeed
        elif self.facing==DOWN:
            return bulletSpeed
        else:
            return 0


            
    def fire_bullet(self):
        #fire sound
        self.cur_lvl.firespell_snd.play()
        newbullet={'x':self.x,
                   'y':self.y,
                   'vx':self.get_bul_vx(),
                   'vy':self.get_bul_vy()}
        self.bullets.append(newbullet)
        self.inhibFire= timeNoBullet


    def notif_right(self):
        self.moveLeft = False
        self.moveRight = True
        if self.facing != RIGHT: # change player image
            self.surface = self.r_img
            self.head_img=self.right_img
        self.facing = RIGHT
     
    def notif_left(self):
        self.moveRight = False
        self.moveLeft = True

        if self.facing != LEFT: # change player image
            self.surface = self.l_img
            self.head_img=self.left_img
        self.facing = LEFT
        
    def notif_up(self):
        self.moveDown = False
        self.moveUp = True
        self.head_img=self.up_img
        self.facing = UP
     
    def notif_down(self):
        self.moveUp = False
        self.moveDown = True

        self.head_img=self.down_img
        self.facing = DOWN

    def set_other_ply(self,other):
        self.other_ply=other

    def update_bullets(self):
        for bul in list(self.bullets):
            bul['x']=bul['x']+bul['vx']
            bul['y']=bul['y']+bul['vy']
            if bul['x']<0 or bul['x']>640 or bul['y']<0 or bul['y']>480:
                self.bullets.remove(bul)

    def calculate_wipe_pos(self):
        self.xWipe=self.x
        self.yWipe=self.y
        if self.facing==UP:
            self.yWipe-=self.wipe_img.get_height()
            self.xWipe+=(-self.wipe_img.get_width()+self.stepWipe)
        elif self.facing==DOWN:
            self.yWipe+=64
            self.xWipe+=(-self.wipe_img.get_width()+self.stepWipe)
        elif self.facing==LEFT:
            self.xWipe-=self.wipe_img.get_width()
            self.yWipe+=(-self.wipe_img.get_width()+self.stepWipe)
        elif self.facing==RIGHT:
            self.xWipe+=64
            self.yWipe+=(-self.wipe_img.get_width()+self.stepWipe)
        


    def init_wipe(self):
        self.stepWipe=0
        self.calculate_wipe_pos()
        self.currentlyWiping=True
        self.wipeFw=True
        
    #TODO
    def update_wipe_if_necessary(self):
        #pass
        if self.currentlyWiping==True:
            if self.wipeFw:
                self.stepWipe+=globStepWipe
            else:
                self.stepWipe-=globStepWipe
            self.calculate_wipe_pos()

            
#            if self.stepWipe>=64:
            if self.wipeFw and self.stepWipe>=self.maxStepWipe:
                print("reversing wipe wipe ")
                #self.currentlyWiping=False
                self.wipeFw=False

            if self.wipeFw==False and self.stepWipe <=0 :
                self.currentlyWiping=False
                return

    def baddy_coll(self):
        #TODO do not forget bullets are "generic ennemies"
        for baddy in self.cur_lvl.currentEnnemies:
            #TODO refac with real w h
            if collutil.coll(self.x,self.y,64,64,baddy["x"],baddy["y"],64,64):
                if "exit" in baddy:
                    print("exit");
                    self.cur_lvl.triggerNextLevel=True
            
    
    def update_model(self):


            #object coll ( baddy and exit and shop etc )
            self.baddy_coll()

        
            self.update_bullets()
            #global yScreen,xScreen
            # actually move the player
            yback=self.y
            xback=self.x
            
            if self.moveLeft:
                self.x -= self.MOVERATE
            if self.moveRight:
                self.x += self.MOVERATE
            if self.moveUp:
                self.y -= self.MOVERATE
            if self.moveDown:
                self.y += self.MOVERATE

            if (self.moveLeft or self.moveRight or self.moveUp or self.moveDown) or self.bounce != 0:
                self.bounce += 1

            if self.inhibFire>0:
                self.inhibFire -= 1
                

            if self.fire and self.inhibFire==0:
                self.fire_bullet()

            if self.bounce > self.BOUNCERATE:
                self.bounce = 0 # reset bounce amount
          #  global yScreen,xScreen

            self.update_wipe_if_necessary()

            if self.wipe:
                self.init_wipe()
                self.wipe=False

#            print(self.y)
            if self.y<10:
                #we need to change screen if one is available
                if 'x'+str(self.cur_lvl.xScreen)+'y'+str(self.cur_lvl.yScreen+1) in self.cur_lvl.bgDict:
                    print('changing screen')
#                    #global yScreen
                    #self.cur_lvl.yScreen+=1
                    self.cur_lvl.offsetXYScreen(0,1)
                    self.y=400
                    self.other_ply.y=400
                else:
                    self.y=yback

            if self.y>440:
                #we need to change screen if one is available
                if 'x'+str(self.cur_lvl.xScreen)+'y'+str(self.cur_lvl.yScreen-1) in self.cur_lvl.bgDict:
                    print('changing screen')
#                    global yScreen
                    #self.cur_lvl.yScreen-=1
                    self.cur_lvl.offsetXYScreen(0,-1)
                    self.y=10
                    self.other_ply.y=10
                else:
                    self.y=yback

            if self.x<10:
                #we need to change screen if one is available
                if 'x'+str(self.cur_lvl.xScreen-1)+'y'+str(self.cur_lvl.yScreen) in self.cur_lvl.bgDict:
                    print('changing screen')
 #                   global xScreen
                    #self.cur_lvl.xScreen-=1
                    self.cur_lvl.offsetXYScreen(-1,0)
                    self.x=540
                    self.other_ply.x=540
                else:
                    self.x=xback

            if self.x>540:
                #we need to change screen if one is available
                if 'x'+str(self.cur_lvl.xScreen+1)+'y'+str(self.cur_lvl.yScreen) in self.cur_lvl.bgDict:
                    print('changing screen')
  #                  global xScreen
#                    self.cur_lvl.xScreen+=1
                    self.cur_lvl.offsetXYScreen(1,0)

                    
                    self.x=10
                    self.other_ply.x=10
                else:
                    self.x=xback
