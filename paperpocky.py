#ennemy fire
#TODO dynamic state to append to ennemy dicts loaded ( pic height width for instance)
#TODO player energy bar
#TODO clean up title ( come back from game )
#TODO refactor with game states ( first cleanup )
#WIP joystick support / refactor input polling 

#TODO player colls
#TODO parameterize ennemy pics
#TODO boss!
#WIP level transition works, but for some reason it waits for fire press

#TODO victory screen !
#put some bounce in ennemy moves
#TODO ennemy state transitions ( to spawn explosion after destroy , or boss states )

#TODO victory screen
import random, sys, time, math, pygame
from pygame.locals import *
from lvlrun import * 
from player import *
from inputpoller import *

FPS = 30 # frames per second to update the screen
#not used yet, should be
WINWIDTH = 640 # width of the program's window, in pixels
WINHEIGHT = 480 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

WHITE = (255, 255, 255)
RED = (255, 0, 0)

#wrapper to pass global around without the dreaded "glob"
class RdrContext(object):
    def __init__(self):
        self.FPSCLOCK=None        
        self.DISPLAYSURF=None        
        self.BASICFONT=None        


def titleScreen(ctx):
    titlepic=pygame.image.load("title.png")
    ctx.DISPLAYSURF.blit(titlepic,
                        pygame.Rect( (0 ,
                                       0,
                                        WINWIDTH,
                                        WINHEIGHT ))    
                         )
    pygame.display.update()

    waitForPlayer=True
    while waitForPlayer :
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYDOWN:
                if event.key == ( K_j):
                    waitForPlayer=False                
            elif event.type == JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    waitForPlayer=False                
            elif event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")


def main():
    
    pygame.init()
    # Initialize the joysticks
    pygame.joystick.init()
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    potJoy1=None
    potJoy2=None

    print("Number of joysticks: "+str(joystick_count) )
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        if i==0:
            potJoy1=joystick
        elif i==1:
            potJoy2=joystick

    poller = InputPoller(potJoy1,potJoy2)
    ctx=RdrContext()
#    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT),pygame.FULLSCREEN)
    ctx.DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    ctx.BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
    #lvlFolder="level2"
    #lvlFolder="level1"

    stageList=["level1","level2"]
    current=-1
    #not to refactor too many things, let's return an outcome for the level
    # VICTORY , or GAME OVER )
    # VICTORY goes to next level
    outcome="next"
#    while True:
    while outcome!="quit":
        if outcome =="next":
            #TODO check if current in range, otherwise victory screen
            current+=1
            if current <= ( len(stageList)-1 ): 
                outcome=runGame(ctx,poller,stageList[current])
            else:
                print(' last level finished, game won ')
                outcome = "quit"



def runGame(ctx,poller,lvlFolder):

    ctx.FPSCLOCK = pygame.time.Clock()
    
    pygame.display.set_icon(pygame.image.load('gameicon.png'))
    pygame.display.set_caption('PAPER POCKY')

    # load the image files
    L_POCK_IMG = pygame.image.load('pocky.png')
    R_POCK_IMG = pygame.transform.flip(L_POCK_IMG, True, False)
    L_ROCK_IMG = pygame.image.load('rocky.png')
    R_ROCK_IMG = pygame.transform.flip(L_ROCK_IMG, True, False)
    two_p_folder='kids/'
    one_p_folder='kids/'
#    two_p_folder='./'
    one_p_down_img = pygame.image.load(one_p_folder+'1pdown.png')
    two_p_down_img = pygame.image.load(two_p_folder+'2pdown.png')
    one_p_left_img = pygame.image.load(one_p_folder+'1pleft.png')
    two_p_left_img = pygame.image.load(two_p_folder+'2pleft.png')
    one_p_right_img = pygame.image.load(one_p_folder+'1pright.png')
    two_p_right_img = pygame.image.load(two_p_folder+'2pright.png')
    one_p_up_img = pygame.image.load(one_p_folder+'1pup.png')
    two_p_up_img = pygame.image.load(two_p_folder+'2pup.png')

    BULLET_IMG= pygame.image.load('bullet.png')
    BADDYBULLET_IMG = pygame.image.load('baddybullet.png')
    RACKET_IMG= pygame.image.load('racket.png')

    img_bd_pool={}

    #wip refactor
    tstImgName='redknight.png'
    img_bd_pool[tstImgName]=pygame.image.load(tstImgName)
    tstImgName='funkyspider.png'
    img_bd_pool[tstImgName]=pygame.image.load(tstImgName)
    tstImgName='straxus.png'
    img_bd_pool[tstImgName]=pygame.image.load(tstImgName)
    tstImgName='miniskel.png'
    img_bd_pool[tstImgName]=pygame.image.load(tstImgName)
    tstImgName='exit.png'
    img_bd_pool[tstImgName]=pygame.image.load(tstImgName)
    #TST_ENNEMY_IMG=pygame.image.load(tstImgName)
    

    #after pygame init, pygame stuff inside


    bgRect=pygame.Rect(0,0,640,480);


    # create the surfaces to hold game text
#    gameOverSurf = BASICFONT.render('Game Over', True, WHITE)
#    gameOverRect = gameOverSurf.get_rect()
#    gameOverRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)


    #firstLvlFolder="level1"

    # stores the player object:
    
    lvl = LvlRun(lvlFolder)
##    lvl.hello()


    ply1=Player(L_POCK_IMG,R_POCK_IMG,RACKET_IMG,one_p_down_img,one_p_up_img,one_p_left_img,one_p_right_img,LEFT,lvl)    
    ply2=Player(L_ROCK_IMG,R_ROCK_IMG,RACKET_IMG,two_p_down_img,two_p_up_img,two_p_left_img,two_p_right_img,LEFT,lvl)    
    ply1.set_other_ply(ply2)
    ply2.set_other_ply(ply1)

    lvl.players.append(ply1)
    lvl.players.append(ply2)
    
    
    pygame.mixer.music.load(lvlFolder+'/bgmusic.wav')
    pygame.mixer.music.play(-1)


    titleScreen(ctx)

#    poller = InputPoller()

    
    while True: # main game loop
        # draw the green background
        ctx.DISPLAYSURF.fill(WHITE)

        ctx.DISPLAYSURF.blit(lvl.bgDict[ 'x'+str(lvl.xScreen)+'y'+str(lvl.yScreen) ],bgRect)


        # draw the player squirrel
        #if True :
        ply1.rect = pygame.Rect( (ply1.x ,
                                              ply1.y  - getBounceAmount(ply1.bounce, ply1.BOUNCERATE, ply1.BOUNCEHEIGHT),
                                              ply1.surface.get_width(),
                                              ply1.surface.get_height()) )
        ctx.DISPLAYSURF.blit(ply1.surface, ply1.rect)

        #TODO blit head
        ply1.rect = pygame.Rect( (ply1.x ,
                                              ply1.y  - getBounceAmount(ply1.bounce, ply1.BOUNCERATE, ply1.BOUNCEHEIGHT)-32,
                                              ply1.surface.get_width(),
                                              ply1.surface.get_height()) )
        ctx.DISPLAYSURF.blit(ply1.head_img, ply1.rect)

            #display wipe if active
        if ply1.currentlyWiping:
                #get x y then blit
                ply1.wipeRect = pygame.Rect( (ply1.xWipe ,
                                              ply1.yWipe,
                                              ply1.wipe_img.get_width(),
                                              ply1.wipe_img.get_height() ))
                ctx.DISPLAYSURF.blit(ply1.wipe_img, ply1.wipeRect)


        ply2.rect = pygame.Rect( (ply2.x ,
                                              ply2.y  - getBounceAmount(ply2.bounce, ply2.BOUNCERATE, ply2.BOUNCEHEIGHT),
                                              ply2.surface.get_width(),
                                              ply2.surface.get_height()) )
        ctx.DISPLAYSURF.blit(ply2.surface, ply2.rect)
        #TODO blit head
        ply2.rect = pygame.Rect( (ply2.x ,
                                              ply2.y  - getBounceAmount(ply2.bounce, ply2.BOUNCERATE, ply2.BOUNCEHEIGHT)-32,
                                              ply2.surface.get_width(),
                                              ply2.surface.get_height()) )
        ctx.DISPLAYSURF.blit(ply2.head_img, ply2.rect)

            #draw the bullets of the players
        for bul in ply1.bullets:
                ctx.DISPLAYSURF.blit(BULLET_IMG,pygame.Rect(bul['x'],bul['y'],BULLET_IMG.get_width(),BULLET_IMG.get_height()))

        for bul in ply2.bullets:
                ctx.DISPLAYSURF.blit(BULLET_IMG,pygame.Rect(bul['x'],bul['y'],BULLET_IMG.get_width(),BULLET_IMG.get_height()))

        try:
#TODO replace with "current" maintained list in lvlrun
                tmpScrDat = lvl.screenDataDict['x'+str(lvl.xScreen)+'y'+str(lvl.yScreen)]
                #displaying ennemies
                ennemies=tmpScrDat['ennemies']
                for ennemy in ennemies:
                    tmpic=img_bd_pool[ennemy['pic']]
#                    ctx.DISPLAYSURF.blit(TST_ENNEMY_IMG,pygame.Rect(ennemy['x'],ennemy['y'],TST_ENNEMY_IMG.get_width(),TST_ENNEMY_IMG.get_height()))
                    ctx.DISPLAYSURF.blit(tmpic,pygame.Rect(ennemy['x'],ennemy['y'],tmpic.get_width(),tmpic.get_height()))
        except KeyError:
                pass
        for gen in lvl.genericEnnemies:
                ctx.DISPLAYSURF.blit(BADDYBULLET_IMG,pygame.Rect(gen.x,gen.y,BADDYBULLET_IMG.get_width(),BADDYBULLET_IMG.get_height()))

        poller.consumeEvents()


        #ply1
        if poller.p1Left:
            ply1.notif_left()
        else:
            ply1.moveLeft=False
        
        if poller.p1Right:
            ply1.notif_right()
        else:
            ply1.moveRight=False
        
        if poller.p1Down:
            ply1.notif_down()
        else:
            ply1.moveDown=False
        
        if poller.p1Up:
            ply1.notif_up()
        else:
            ply1.moveUp=False
        
        if poller.p1Fire:
            ply1.fire=True
        else:
            ply1.fire=False

        if poller.p1Swipe:
            ply1.wipe=True        

        #ply2
        if poller.p2Left:
            ply2.notif_left()
        else:
            ply2.moveLeft=False
        
        if poller.p2Right:
            ply2.notif_right()
        else:
            ply2.moveRight=False
        
        if poller.p2Down:
            ply2.notif_down()
        else:
            ply2.moveDown=False
        
        if poller.p2Up:
            ply2.notif_up()
        else:
            ply2.moveUp=False
        
        if poller.p2Fire:
            ply2.fire=True
        else:
            ply2.fire=False

        if poller.p2Swipe:
            ply2.wipe=True        

        #next level check



        lvl.update_model()
        if lvl.triggerNextLevel:
            return "next"
        if poller.quit:
            terminate()

        pygame.display.update()
        ctx.FPSCLOCK.tick(FPS)






def terminate():
    pygame.quit()
    sys.exit()


def getBounceAmount(currentBounce, bounceRate, bounceHeight):
    # Returns the number of pixels to offset based on the bounce.
    # Larger bounceRate means a slower bounce.
    # Larger bounceHeight means a higher bounce.
    # currentBounce will always be less than bounceRate
    return int(math.sin( (math.pi / float(bounceRate)) * currentBounce ) * bounceHeight)






if __name__ == '__main__':
    main()
