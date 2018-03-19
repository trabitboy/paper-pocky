

def coll(x1,y1,w1,h1,x2,y2,w2,h2):
        #x check
        if x1+w1 <x2 or x2+w2 <x1:
            #no coll x
            return False
        if y1+h1 <y2 or y2+h2 <y1:
            #no coll y
            return False
        #if we are so far both are coll
        return True
