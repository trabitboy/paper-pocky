import pygame
import player
import json
import collutil
from HomingBullet import *
from pprint import pprint

class LvlRun(object):
    def __init__(self,lvlFolder):

        #message passing flag to load next level
        self.triggerNextLevel=False

        self.lvlFolder=lvlFolder;
        self.test='tutu'        
        self.bgDict={}
        self.screenDataDict={}
        self.players=[]
        for j in range(0,6):
            for i in range(0,3):
                print('trying to load pic ' +str(i)+' '+str(j))
                prefix =lvlFolder+'/'
                #'source/'
                key='x'+str(i)+'y'+str(j)
                try:
                    tmp=pygame.image.load(prefix+key+'.png')
                    tmp2=pygame.transform.scale(tmp,(480,640))
                    angle=270
                    bg=pygame.transform.rotate(tmp2,angle)
                    self.bgDict[key]=bg
                except pygame.error as message:
#            if bg is None:
                    print('not found '+key)
#           else:
#               bgDict[key]=bg


        self.currentEnnemies=None
        #ennemies
        print('loading screen datas ')
        for j in range(0,6):
            for i in range(0,3):
                print('trying to load data ' +str(i)+' '+str(j))
                prefix =lvlFolder+"/"
                #'source/'
                key='x'+str(i)+'y'+str(j)
                potfile=prefix+key+'.json'
                try:
                    with open(potfile) as data_file:    
                        data = json.load(data_file)
                        pprint(data)
                        data['step']=0 #to quantify where the ennemy is in his anim
                        self.screenDataDict[key]=data
                except FileNotFoundError:
                    print("Wrong file or file path")
#        self.xScreen=1
#        self.yScreen=0
        self.setXYScreen(1,0)
        #preparing firing fx
        self.firespell_snd=pygame.mixer.Sound(lvlFolder+'/firespell.wav')
        #preparing ennemy destroyed fx
        self.ennemydestroyed_snd=pygame.mixer.Sound(lvlFolder+'/ennemydestroyed.wav')
        #writing second kind of ennemies that are proper classes
        # ( they have code in them )( normal ennemies should be migrated to that at one point )
        self.genericEnnemies=[]

    #TODO : check if possible 
    def offsetXYScreen(self,ox,oy):
        self.setXYScreen(self.xScreen +ox,self.yScreen+oy)

    #wip : to maintain "current" ennemy list and "current" bg
    def setXYScreen(self,nxs,nys):
        self.xScreen=nxs
        self.yScreen=nys
        ennemies=[]

        try:
            tmpScrDat = self.screenDataDict['x'+str(self.xScreen)+'y'+str(self.yScreen)]
            ennemies=tmpScrDat['ennemies']
        except KeyError:
            print("key error")
        self.currentEnnemies=ennemies
        #TODO TOWIRE
        #pass
        self.genericEnnemies=[]
        
    ##for some reason throws error called from main loop, wip merge to hello_monsters
    def update_model(self):

        for ply in self.players:
            #pass
#            print("updating player")
            ply.update_model()
#        ply1.update_model()
#        ply2.update_model()

        #update ennemies
        self.hello_monsters()

##    def coll(self,x1,y1,w1,h1,x2,y2,w2,h2):
##        #x check
##        if x1+w1 <x2 or x2+w2 <x1:
##            #no coll x
##            return False
##        if y1+h1 <y2 or y2+h2 <y1:
##            #no coll y
##            return False
##        #if we are so far both are coll
##        return True
##
##        #pass

    def ennemy_to_bullet_coll(self,ennemy,bullet):
        
        #TODO coll code TODO put real coords
#        return self.coll(ennemy["x"],ennemy["y"],64,64,bullet["x"],bullet["y"],32,32)
        return collutil.coll(ennemy["x"],ennemy["y"],64,64,bullet["x"],bullet["y"],32,32)
        #TODO inactivate ennemy / remove bullet
        #pass

    def ennemy_to_bullets_coll(self,en):
        for ply in self.players:
            bull_ply=ply.bullets
            for bullet in list(bull_ply): #we might remove bullet, so we iterate on copy
                if self.ennemy_to_bullet_coll(en,bullet):
                    bull_ply.remove(bullet)
                    self.currentEnnemies.remove(en)
                    self.ennemydestroyed_snd.play()
                    return
                    
            
                    

    def fireHomingBullet(self,en):
        #WIP by default let us target player 1 :)
        tgtply=self.players[0]
        spawned = HomingBullet(en["x"],en["y"],tgtply.x,tgtply.y)
        self.genericEnnemies.append(spawned)

    def update_ennemy(self,en):
        #en['x']

        #only one default behavior so far        
        step=en['step']
        if step <30:
            
            en['x']=en['x']+en['vx']
            en['y']=en['y']+en['vy']
            step=step+1
            en['step']=step
        else:
            en['vx']=-en['vx']
            en['vy']=-en['vy']
            en['step']=0
            self.fireHomingBullet(en)
        
        #we do check coll between bullets of both players and the ennemies
        self.ennemy_to_bullets_coll(en)
        


    def hello_monsters(self):

                for ennemy in list(self.currentEnnemies):#we might remove some
                    #default loaded ennemy behavior
                    if 'exit' in ennemy:
                        pass
                    else:
                        self.update_ennemy(ennemy)
                
                for gen in list(self.genericEnnemies):
                    gen.update(self)

    
