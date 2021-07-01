import OpenGL.GL as _gl
import OpenGL.GLUT as _glut

import math
import numpy as np
from ctypes import c_float

from global_vars import Cos, Sin
import SimpleObjects as so
from shader_functions import activateShader











class Crawler:
    '''
    Crawlers are striped creatures with round bodies and several legs.
    
    DNA
    ---
    The colors of the stripes are determined by their DNA, which is a pair
    of integers in the range [0,9]. One color of stripes is determined by one
    integer, and the other color by the other integer. The number of legs is 
    determined by the sum of the integers divided by two (and placed radially
    around their bodies). There are a minimum of two legs, and if the DNA is
    odd, an extra leg is added. The number of legs also determines the speed
    of the crawler.
    
    The parents send half of their DNA to the child, with random order. The 
    first integer determines the sex of the child. Females have a loop which
    protrudes from their tops while the males do not. 
    
    
    Behavior
    --------
    The food they eat is near the floor of the aquarium, so they only move
    horizontally. They move forward always, unless they hit a wall, when
    they turn a random wide angle, or when encountering another crawler.
    
    If they encounter an opposite sex crawler, there's a 50% chance of mating 
    and producing a single offspring nearby, and turn completely around.
    When two same sex crawlers collide the one with the higher DNA sum survives 
    and the other dies (equal DNA causes both to survive). They can also die of 
    old age or starvation. 
    
    '''
    def __init__(self, dna=None):
        
        if dna is None:
            self.dna = np.random.randint(0,9,2)
        else:
            self.dna = dna
        
        self.ctype = 'crawler'
        self.skincolors = self.getSkinColors()
        
        
        
        self.DOB = 0.001*_glut.glutGet(_glut.GLUT_ELAPSED_TIME)
        self.center_location = [0,0,0]
        self.facing = [0,0,1,0]
        
        self.hitbox = 0.5
        self.size = [self.hitbox for i in range(3)]
        
        self.last_collision = self.DOB
        
        self.age = 1
        self.lifespan=20
        self.egg_time = 3
        self.hunger = 0
        
        self.sex = bool((self.dna[0])%2)
        
        self.body = so.Sphere(res=15)
        #self.headtube = so.Cylinder(res=15)
        self.antenna = so.WireFrameCyl(wire_points=self.antennaWirePoints(), 
                                                res=30, r=0.1)
        self.mouth = Mouth(colors=[1,1,1])
        self.tail = Tail(colors=[1,1,1])
        #self.tail = Tail(colors=[i/255 for i in [111,119,85]])
        
        self.numlegs = int(np.sum(self.dna)/2) + 2
        if bool(self.numlegs%2):
            self.numlegs+=1
            
        self.legs = []
        self.initLegs()
        self.initLoop()
        
        # Movement step size/speeds. Array-like for alternate speeds.
        speed_mult = self.numlegs/4
        self.speeds = [0.1*speed_mult, 0]
        self.movestep = self.speeds[0]
        
        
        self.hatched=False
        self.notmated=True
        
        self.stasis = False
        
        
        ''' Shader attributes '''
        self.timevars= {'f':True,
                        's':0,
                        'el':0}
        self.notburning = True
        self.burn = False
        self.spawn=False
        self.spawntime = 2.1
        self.kill = False
        
        
        rlocs = np.random.rand(6)*2*self.hitbox - self.hitbox
        self.randpositions = [[rlocs[0],-self.hitbox,rlocs[1]],
                              [rlocs[2],0.0,rlocs[3]],
                              [rlocs[4],self.hitbox,rlocs[5]]]
        
        
        
        zrands = np.random.rand(3)*15
        xrands = np.random.rand(3)*4 - 2
        yrands = np.random.rand(3)*2 - 1
        self.tailrand = [[xrands[i],yrands[i],zrands[i]] for i in range(3)]
        
    
    
    
    def sizeUpdate(self,s):
        self.hitbox = s
        self.size = [self.hitbox for i in range(3)]
    
    def getSkinColors(self):
        
        dna1 = self.dna[0]
        dna2 = self.dna[1]
        
        color_dict = {'astronaut_blue':[33, 69, 89],
                      'blue_charcoal ':[38, 43, 47],
                      'dark_navy_blue ':[0, 51, 102],
                      'dark_green ':[1, 50, 32],
                      'dill ':[111,119,85],
                      'very_dark_green ':[6, 46, 3],
                      'brick_orange ':[193, 74, 9],
                      'burgundy ':[128, 0, 32],
                      'maroon ':[128, 0, 0],
                      'alice_blue ':[240, 248, 255],
                      'light_azure ':[139, 185, 231],
                      'sea_mist ':[194, 213, 196],
                      'lima_bean ':[179, 223, 112],
                      'oyster ':[163, 146, 116],
                      'pink_linen ':[210, 191, 196],
                      'sand_yellow ':[207, 174, 117],
                      'peach_orange ':[255, 204, 153],
                      'tainted_gold ':[234, 215, 149]}
        
        color_list1 = list(color_dict.keys())[:9]
        color_list2 = list(color_dict.keys())[9:]
    
        color1 = color_dict[color_list1[dna1]]
        color2 = color_dict[color_list2[dna2]]
        
        color1 = np.array(color1)/255
        color2 = np.array(color2)/255
        
        color1 = color1.tolist()
        color2 = color2.tolist()
        
        return [color1, color2]
    
    
    

    
    def BurnSpawnShaders(self, burnprog, spawnprog, baseprog,
                         A,D,P,
                         c=None,rnd=None,rmult=1):
        
        if c is None:
            skincolors = self.skincolors
        else:
            skincolors = c
        
        if rnd is None:
            randpositions = self.randpositions
        else:
            randpositions = rnd
        
        
        
        if self.burn:
            
            time = 0.001*_glut.glutGet(_glut.GLUT_ELAPSED_TIME)
            
            # Record the start time and turn this part off.
            if self.timevars['f']:
                self.timevars['f']=False
                self.timevars['s']=time
            
            # Only increase elapsed time if below 20 seconds.
            if self.timevars['el']<5:
                self.timevars['el'] = time - self.timevars['s']
            else:
                #self.burn=False
                self.kill=True
            
            activateShader(shaderprog = burnprog,
                           A=A, D=D, P=P, 
                           R=self.timevars['el']*0.4*rmult, 
                           pos=randpositions,
                           colors = skincolors)
            
            if not self.burn:
                self.timevars= {'f':True,
                                's':0,
                                'el':0}
            
        elif self.spawn:
            
            time = 0.001*_glut.glutGet(_glut.GLUT_ELAPSED_TIME)
            
            # Record the start time and turn this part off.
            if self.timevars['f']:
                self.timevars['f']=False
                self.timevars['s']=time
            
            # Only increase elapsed time if below 20 seconds.
            if self.timevars['el']<self.spawntime+0.5:
                self.timevars['el'] = time - self.timevars['s']
            else:
                self.spawn=False
                
            
            
        
        
            activateShader(shaderprog = spawnprog,
                               A=A, D=D, P=P, 
                               R=self.timevars['el']*1.6-1,
                               colors = skincolors)
            
            if not self.spawn:
                self.timevars= {'f':True,
                                's':0,
                                'el':0}
        
        else:
            activateShader(shaderprog = baseprog, A=A, D=D, P=P,
                           colors = skincolors)
            
        
    
    
    def draw(self,tex=None, ADP=None, shaderprogs=None):
        
        self.ADP = ADP
        self.shaderprogs = shaderprogs
        
        _gl.glPushMatrix()
        
        
        _gl.glTranslatef(*self.center_location)
        _gl.glRotatef(*self.facing)
        _gl.glScalef(*self.size)
        
        
        if tex is not None:
            _gl.glEnable(_gl.GL_TEXTURE_2D)
            _gl.glBindTexture(_gl.GL_TEXTURE_2D, tex)
            
            self.drawParts()
            
            _gl.glDisable(_gl.GL_TEXTURE_GEN_S)
            _gl.glDisable(_gl.GL_TEXTURE_GEN_T)
            _gl.glDisable(_gl.GL_TEXTURE_2D)
            
        else:
            self.drawParts()
        
        _gl.glPopMatrix()
    
    
    def burnUpdate(self):
        self.burn = True
        self.notburning = False
        
        self.spawn=False
        self.timevars= {'f':True,
                        's':0,
                        'el':0}
    
    def update(self,t):
        
        if not self.stasis:
            
            if self.kill:
                return False, self.center_location, self.hitbox
            
            # Update age and kill if too old.
            self.age = t-self.DOB
            
            if self.age>self.egg_time and self.age<self.egg_time+self.spawntime:
                self.hatched = True
                self.spawn=True
                
            if self.hatched:
                
                if self.age>self.lifespan and self.notburning:
                    self.burnUpdate()
                
                if self.notburning and not self.spawn:
                    # Move.
                    th = self.facing[0]
                    self.center_location[0]+=self.movestep*Sin(th)
                    self.center_location[2]+=self.movestep*Cos(th)
                    
                elif not self.notburning:
                    self.center_location[1]+=self.movestep*(1/2)
                    
                    self.facing[1]=1
                    self.facing[3]=1
                    self.facing[0] += 2 
                
        
        return True, self.center_location, self.hitbox
    
    
    def drawParts(self):
        
        
        if self.hatched:
            
            red = [i/255 for i in [128, 0, 32]]
            self.BurnSpawnShaders(*self.shaderprogs,*self.ADP, c=[red,red],rmult=12)
            #self.headtube.draw(r=[90,1,0,0],s=[0.1,2,0.1])
            self.drawMouth()
            
            
            self.BurnSpawnShaders(*self.shaderprogs,*self.ADP, 
                                  c=[self.skincolors[0],self.skincolors[0]],
                                  rnd = self.tailrand, rmult=15)
            self.drawTail()
            
            
            self.BurnSpawnShaders(*self.shaderprogs,*self.ADP, 
                                  c=[self.skincolors[0],self.skincolors[0]])
            self.drawAntennae()
            
            
            self.BurnSpawnShaders(*self.shaderprogs,*self.ADP)
            self.drawLegs()
            self.drawBody()
            
            
            
            
            if self.sex:
                self.drawLoop()
        else:
            self.BurnSpawnShaders(*self.shaderprogs,*self.ADP)
            self.body.draw(s=[0.4*self.hitbox for i in range(3)])
    
    
    
    def antennaWirePoints(self):
        points=[]
        
        start=235
        step=15
        stop = start-360
        
        R_vals = np.linspace(1,0,num=int((start-stop)/step))
        
        for i,th in enumerate(range(start,stop,-step)):
            r = R_vals[i]
            points.append([r*Cos(th),r*Sin(th),0])
        
        
        return points
    
    
    def drawAntennae(self):
        self.antenna.draw(t=[0.9*Cos(105),0.3,0.9*Sin(105)],
                          r=[-90,0,1,0],
                          s=[0.3,0.3,0.3])
        
        self.antenna.draw(t=[0.9*Cos(75),0.3,0.9*Sin(75)],
                          r=[-90,0,1,0],
                          s=[0.3,0.3,0.3])
    
    
    
    def initLoop(self):
        pts = [[0,0.025,0],
               [0,0.4,0]]
        
        for i in range(270,270+360+30,30):
            pts.append([0,0.1*Sin(i)+0.5,0.1*Cos(i)])
        
        self.loop = so.WireFrameCyl(wire_points=pts, 
                                    res=15, r=.04)
    
    def initLegs(self):
        
        leg_angles = [[180],
                      [165,195],
                      [150,180,210],
                      [150,165,195,210],
                      [120,150,180,210,240]]
        
        angle_list = leg_angles[int(self.numlegs/2)-1]
        for lpoint in angle_list:
            
            # Leg on one side.
            pos1 = [0.95*Cos(lpoint),0.025,0.95*Sin(lpoint)]
            pos2 = [1.5*Cos(lpoint),0.3,1.5*Sin(lpoint)]
            pos3 = [1.7*Cos(lpoint),0,1.7*Sin(lpoint)]
            pos4 = [1.8*Cos(lpoint),0,1.8*Sin(lpoint)]
            
            pos5 = [1.8*Cos(lpoint+5),0,1.8*Sin(lpoint+5)]
            pos6 = [1.8*Cos(lpoint-5),0,1.8*Sin(lpoint-5)]
            
            leg1 = so.WireFrameCyl(wire_points=[pos1,pos2,pos3,pos4], 
                               res=30, r=.04, bigjoints=True)
            
            toe1 = so.WireFrameCyl(wire_points=[pos3,pos5], 
                               res=30, r=.04, bigjoints=True)
            toe2 = so.WireFrameCyl(wire_points=[pos3,pos6], 
                               res=30, r=.04, bigjoints=True)
            
            self.legs.append(leg1)
            self.legs.append(toe1)
            self.legs.append(toe2)
            
            # Leg on opposite side.
            pos1 = [0.95*Cos(lpoint+180),0.025,0.95*Sin(lpoint+180)]
            pos2 = [1.5*Cos(lpoint+180),0.3,1.5*Sin(lpoint+180)]
            pos3 = [1.7*Cos(lpoint+180),0,1.7*Sin(lpoint+180)]
            pos4 = [1.8*Cos(lpoint+180),0,1.8*Sin(lpoint+180)]
            
            pos5 = [1.8*Cos(lpoint+185),0,1.8*Sin(lpoint+185)]
            pos6 = [1.8*Cos(lpoint+175),0,1.8*Sin(lpoint+175)]
            
            leg2 = so.WireFrameCyl(wire_points=[pos1,pos2,pos3,pos4], 
                               res=30, r=.04, bigjoints=True)
            
            toe3 = so.WireFrameCyl(wire_points=[pos3,pos5], 
                               res=30, r=.04, bigjoints=True)
            toe4 = so.WireFrameCyl(wire_points=[pos3,pos6], 
                               res=30, r=.04, bigjoints=True)
            
            self.legs.append(leg2)
            self.legs.append(toe3)
            self.legs.append(toe4)
    
    
    def drawLegs(self):
        for leg in self.legs:
            leg.draw()
            
    
    def drawBody(self):
        self.body.draw(s=[1,0.3,1])
    
    
    
    def drawMouth(self):
        _gl.glPushMatrix()
        
        _gl.glTranslatef(*[0,0.025,1])
        
        _gl.glRotatef(*[90,1,0,0])
        _gl.glRotatef(*[180,0,1,0])
        
        sc = 0.3/14
        _gl.glScalef(*[sc*2,sc*1.3,sc])
        
        _gl.glTranslatef(*[-7,0,-2])
        
        self.mouth.draw()
            
        _gl.glPopMatrix()
    
    
    def drawTail(self):
        _gl.glPushMatrix()
        
        _gl.glTranslatef(*[0,0.025,-1.25])
        
        
        sc = 1.5/15
        _gl.glScalef(*[sc,sc,sc])
        
        _gl.glTranslatef(*[0,0,-7.5])
        
        self.tail.draw()
            
        _gl.glPopMatrix()
    
    
    def drawLoop(self):
        self.loop.draw()
            







class BodyPart(so.GenericObject):
    '''
    Draw body part out of triangles.
    
    Only the function genTriangles needs to be overwritten to return a
    Nx3x3 array of triangle vertices for N triangles.
    '''
    
    def __init__(self,colors=[1,1,1]):
        self.colors = colors
        super().__init__(None,None)
        
        
    def drawParts(self):
        self.drawPart(_gl.GL_TRIANGLES,0,int(self.n_points/3))
    
    # Get an index of a 1D array within a nD array.
    def arrIndInNestedArr(self,A,B):
        nrows, ncols = A.shape
        dtype={'names':['f{}'.format(i) for i in range(ncols)],
               'formats':ncols * [A.dtype]}
        inds, = np.where(np.in1d(A.view(dtype), B.view(dtype)))
        return inds
    
    # Given a list of traingle vertices, generate corresponding normals.
    def genNormals(self,triangles):
        normals = []
        for triangle in triangles:
            v1 = triangle[1]
            v2 = triangle[0]
            v3 = triangle[2]
            
            face_normal = np.cross(v2-v1,v3-v1)
            for j in range(3):
                normals.append(face_normal)
            
        return np.array(normals)
    
    
    # Averaging normals for shared vertices, for Gouraud shading.
    def avgNorms(self, triangles, normals):
        avgd_normals=np.zeros(normals.shape)
        found_inds=[]
        
        vertlist = triangles.reshape((-1,3))
        for i, norm in enumerate(normals):
            if i not in found_inds:
                
                # Associated vertex.
                vert = vertlist[i]
                
                # Shared vertices.
                inds = self.arrIndInNestedArr(vertlist, vert).tolist()
                
                # Normals for all of these vertices.
                s_norms = normals[inds]
                a_norm = np.mean(s_norms,axis=0)
                
                # Set new norm list to have average.
                for j in inds:
                    avgd_normals[j] = a_norm
                
                # Don't recalculate for these vertices.
                found_inds.extend(inds)
        
        return avgd_normals
    
    
    def getData(self):
        vdata, cdata, ndata, tdata = [],[],[],[]
        
        # Specify triangle points.
        triangles = self.genTriangles()
        
        
        normals = self.genNormals(triangles)
        
        normals = self.avgNorms(triangles, normals)
                
        
        # Make data 1D for VBOs.
        vdata = triangles.ravel()
        ndata = normals.ravel()
        
        
        cdata = list(np.tile(self.colors,int(len(vdata)/3)))
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            np.array(vdata), np.array(cdata), np.array(ndata), np.array(tdata)
    
    def genTriangles(self):
        pass








class Mouth(BodyPart):
    
    
    def __init__(self,colors=[1,1,1]):
        super().__init__(colors)
    
    
    
    def genTriangles(self):
        triangles = []
        
        hval = 1
        
        # Top of mouth
        vlist = [[0,0,2],
                 [5,0,2],
                 [5,hval,3],
                 [5,0,5],
                 [7,0,0],
                 [7,hval,1],
                 [7,hval,3],
                 [9,0,2],
                 [9,hval,3],
                 [9,0,5],
                 [14,0,2],
                 [7,0,4.5]]
        
        triangles.append([vlist[0],vlist[2],vlist[3]])
        triangles.append([vlist[0],vlist[1],vlist[2]])
        triangles.append([vlist[0],vlist[5],vlist[10]])
        triangles.append([vlist[0],vlist[4],vlist[5]])
        triangles.append([vlist[4],vlist[10],vlist[5]])
        triangles.append([vlist[3],vlist[2],vlist[6]])
        triangles.append([vlist[2],vlist[1],vlist[7]])
        triangles.append([vlist[2],vlist[7],vlist[8]])
        triangles.append([vlist[6],vlist[8],vlist[9]])
        triangles.append([vlist[9],vlist[8],vlist[10]])
        triangles.append([vlist[8],vlist[7],vlist[10]])
        triangles.append([vlist[3],vlist[6],vlist[11]])
        triangles.append([vlist[6],vlist[9],vlist[11]])
        
        # Bottom.
        lower = lambda l_: [l_[0], -3, l_[2]]
        
        wall1 = lambda l,r: triangles.append([vlist[l],lower(vlist[l]),vlist[r]])
        wall2 = lambda l,r: triangles.append([lower(vlist[l]),lower(vlist[r]),vlist[r]])
        
        #triangles.append([vlist[0],lower(vlist[0]),vlist[4]])
        #triangles.append([lower(vlist[0]),lower(vlist[4]),vlist[0]])
        
        wall1(0,4)
        wall2(0,4)
        
        wall1(4,10)
        wall2(4,10)
        
        wall1(9,10)
        wall2(9,10)
        
        wall1(11,9)
        wall2(11,9)
        
        wall1(3,11)
        wall2(3,11)
        
        wall1(0,3)
        wall2(0,3)
        
        
        
        
        
        return np.array(triangles)
    



class Tail(BodyPart):
    
    
    def __init__(self,colors=[1,1,1]):
        super().__init__(colors)
    
    
    
    def genTriangles(self):
        triangles = []
        
        hval=1
        lower = lambda l_: [l_[0], -hval, l_[2]]
        
        
        vlist = [[-2,0,14],
                 [0,hval,14],
                 [2,0,14],
                 [-2,0,10],
                 [0,hval,10],
                 [2,0,10],
                 [0,0,7],
                 [1.5,hval,7],
                 [3,0,7],
                 [-1,0,4],
                 [0,hval,4],
                 [1,0,4],
                 [1,0,2],
                 [1.5,hval,2],
                 [2,0,2],
                 [0,0,0]]
        # 1 4 7 10 13
        for i in range(0,10,3):
            
            # Upper quad 1.
            triangles.append([vlist[i],vlist[i+3],vlist[i+4]])
            triangles.append([vlist[i],vlist[i+4],vlist[i+1]])
            
            # Upper quad 2.
            triangles.append([vlist[i+1],vlist[i+4],vlist[i+5]])
            triangles.append([vlist[i+1],vlist[i+5],vlist[i+2]])
            
            # Lower quad 1.
            triangles.append([vlist[i],vlist[i+3],lower(vlist[i+4])])
            triangles.append([vlist[i],lower(vlist[i+4]),lower(vlist[i+1])])
            
            # Lower quad 2.
            triangles.append([lower(vlist[i+1]),lower(vlist[i+4]),vlist[i+5]])
            triangles.append([lower(vlist[i+1]),vlist[i+5],vlist[i+2]])
            
        
        
        # Upper tail tip.
        triangles.append([vlist[12],vlist[15],vlist[13]])
        triangles.append([vlist[13],vlist[15],vlist[14]])
        
        
        # Lower tail tip.
        # Upper tail tip.
        triangles.append([vlist[12],vlist[15],lower(vlist[13])])
        triangles.append([lower(vlist[13]),vlist[15],vlist[14]])
        
        
        return np.array(triangles)










        