import collutil


class HomingBullet(object):
    #this object can be added to ennemies pool, should be removed
    #when it gets off screen
    #lvl run binding to eventually impact players, sfx
    def __init__(self,x,y,tx,ty):
        self.x=x
        self.y=y
        self.tx=tx
        self.ty=ty
        #computing steps on x and y
        #TODO magic number of bullet speed
        distance2 = (x-tx)*(x-tx) +( y-ty)*(y-ty)
        #TODO the pixel speed is magic for now
        pixspeed=30
        self.nbsteps= (distance2 )/(pixspeed*pixspeed) 
        #we calculate a base step to follow even after target reached
        self.xstp=(tx-x)/self.nbsteps
        self.ystp=(ty-y)/self.nbsteps


    def update(self,lvl):
        self.x=self.x+self.xstp
        self.y=self.y+self.ystp
        #if outside of screen we remove them
        if self.x<0 or self.x>640 or self.y<0 or self.y>480:
            print("removing homing bullet " )
            lvl.genericEnnemies.remove(self)
            #TODO collision between wipe and bullet

        for ply in lvl.players:
            if ply.currentlyWiping==True:
                 if collutil.coll(self.x,self.y,64,64,ply.xWipe,ply.yWipe,32,32):
                       print("wipe coll")
                       #TODO check if we are iterating on a copy
                       lvl.genericEnnemies.remove(self)
                       lvl.ennemydestroyed_snd.play()
