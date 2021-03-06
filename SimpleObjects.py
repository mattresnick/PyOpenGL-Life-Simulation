import OpenGL.GL as _gl

import math
import numpy as np
from ctypes import c_float

from global_vars import Cos, Sin, Polar


from copy import copy

class GenericObject:
    '''
    Base class for creating a simple, generic 3D object using VBOs. drawParts
    (called at draw-time) and getData (called at initilization-time) need to
    be overloaded. The former draws the individual pieces based on primitive
    type and index values, and getData obtains the vertex, texture, color, and
    normal data.
    '''
    
    
    def __init__(self,res=1,rep=[1,1]):
        self.res = res
        self.rep = rep
        self.color_len=3
        
        self.draw_metadata = []
        
        self.initBuffers()
    
    def draw(self,tex=None,s=None,r=None,t=None):
        _gl.glPushMatrix()
        
        if t is not None:
            _gl.glTranslatef(*t)
        
        if r is not None:
            _gl.glRotatef(*r)
        
        if s is not None:
            _gl.glScalef(*s)
        
        
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
    
    # Initialize buffers used to store the data for drawing.
    def initBuffers(self):
        
         # Calculate vertex/color lists from indices.
        #vdata, cdata, ndata, tdata = self.getData()
        self.getData()
        
        # Convert data to appropriate form for buffers.
        self.n_points = len(self.vdata)
        self.fsize = self.vdata.itemsize
        
        # Convert to c arrays.
        self.vert_data = (c_float*len(self.vdata))(*self.vdata)
        self.color_data = (c_float*len(self.cdata))(*self.cdata)
        self.norm_data = (c_float*len(self.ndata))(*self.ndata)
        self.tex_data = (c_float*len(self.tdata))(*self.tdata)
        
        # Initialize VBO for vertices.
        self.vbo_v = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_v)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points*self.fsize,
                         copy(self.vert_data),
                         _gl.GL_STATIC_DRAW)
        
        # Initialize VBO for colors.
        self.n_points_c = len(self.cdata)
        self.fsize_c = self.cdata.itemsize
        
        self.vbo_c = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_c)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points_c*self.fsize_c,
                         copy(self.color_data),
                         _gl.GL_STATIC_DRAW)
        
        # Initialize VBO for normals.
        self.vbo_n = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_n)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points*self.fsize,
                         copy(self.norm_data),
                         _gl.GL_STATIC_DRAW)
        
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,0)
        
    
    # Specify how to use the generated data to draw the components.
    def drawParts(self):
        pass
    
    # Draw individual pieces of the object.
    def drawPart(self,gtype,start,num):
        
        # Bind vertex VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_v)
        _gl.glEnableClientState(_gl.GL_VERTEX_ARRAY)
        _gl.glVertexPointer(3,_gl.GL_FLOAT,0,None)
        
        # Bind color VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_c)
        _gl.glEnableClientState(_gl.GL_COLOR_ARRAY)
        _gl.glColorPointer(self.color_len,_gl.GL_FLOAT,0,None)
        
        # Bind normal VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_n)
        _gl.glEnableClientState(_gl.GL_NORMAL_ARRAY)
        _gl.glNormalPointer(_gl.GL_FLOAT,0,None)
        
        
        
        # Reset.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,0)
        
        
        
        # Use DrawArrays to construct the individual pieces.
        _gl.glDrawArrays(gtype,start,num)
        
        
        # "Turn off" VBOs
        _gl.glDisableClientState(_gl.GL_VERTEX_ARRAY)
        _gl.glDisableClientState(_gl.GL_COLOR_ARRAY)
        _gl.glDisableClientState(_gl.GL_NORMAL_ARRAY)
        
        
        
    
    
    # Generate the data used to draw the pieces.
    def getData(self):
        pass











class GenericTexturedObject(GenericObject):
    
    
    def __init__(self,res=1,rep=[1,1]):
        super().__init__(res,rep)
    
    
    
    # Initialize buffers used to store the data for drawing.
    def initBuffers(self):
        
         # Calculate vertex/color lists from indices.
        #vdata, cdata, ndata, tdata = self.getData()
        self.getData()
        
        # Convert data to appropriate form for buffers.
        self.n_points = len(self.vdata)
        self.fsize = self.vdata.itemsize
        
        
        # Convert to c arrays.
        self.vert_data = (c_float*len(self.vdata))(*self.vdata)
        self.color_data = (c_float*len(self.cdata))(*self.cdata)
        self.norm_data = (c_float*len(self.ndata))(*self.ndata)
        self.tex_data = (c_float*len(self.tdata))(*self.tdata)
        
        # Initialize VBO for vertices.
        self.vbo_v = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_v)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points*self.fsize,
                         copy(self.vert_data),
                         _gl.GL_STATIC_DRAW)
        
        # Initialize VBO for colors.
        self.vbo_c = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_c)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points*self.fsize,
                         copy(self.color_data),
                         _gl.GL_STATIC_DRAW)
        
        # Initialize VBO for normals.
        self.vbo_n = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_n)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points*self.fsize,
                         copy(self.norm_data),
                         _gl.GL_STATIC_DRAW)
        
        
        self.n_points_t = len(self.tdata)
        self.fsize_t = self.tdata.itemsize
        
        # Initialize VBO for textures.
        self.vbo_t = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_t)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points_t*self.fsize_t,
                         copy(self.tex_data),
                         _gl.GL_STATIC_DRAW)
        
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,0)
        
    
   
    # Draw individual pieces of the object.
    def drawPart(self,gtype,start,num):
        
        # Bind vertex VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_v)
        _gl.glEnableClientState(_gl.GL_VERTEX_ARRAY)
        _gl.glVertexPointer(3,_gl.GL_FLOAT,0,None)
        
        # Bind color VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_c)
        _gl.glEnableClientState(_gl.GL_COLOR_ARRAY)
        _gl.glColorPointer(3,_gl.GL_FLOAT,0,None)
        
        # Bind normal VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_n)
        _gl.glEnableClientState(_gl.GL_NORMAL_ARRAY)
        _gl.glNormalPointer(_gl.GL_FLOAT,0,None)
        
        
        # Bind texture VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_t)
        _gl.glEnableClientState(_gl.GL_TEXTURE_COORD_ARRAY)
        _gl.glTexCoordPointer(2,_gl.GL_FLOAT,0,None)
        
        # Reset.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,0)
        
        
        
        # Use DrawArrays to construct the individual pieces.
        _gl.glDrawArrays(gtype,start,num)
        
        
        # "Turn off" VBOs
        _gl.glDisableClientState(_gl.GL_VERTEX_ARRAY)
        _gl.glDisableClientState(_gl.GL_COLOR_ARRAY)
        _gl.glDisableClientState(_gl.GL_NORMAL_ARRAY)
        _gl.glDisableClientState(_gl.GL_TEXTURE_COORD_ARRAY)
        











class WireFrameCyl(GenericObject):
    '''
    Draw a cylinder about a wireframe of points, using spheres for joints
    and faceculling.
    '''
    
    def __init__(self, wire_points, res, r, bigjoints=False, rep=[1,1], colors=[]):
        self.w_points = wire_points
        self.colors = colors
        self.r = r
        
        if bigjoints:
            self.SphereObj = Sphere(res=60,rep=rep,colors=colors)
            self.joint_scale = [self.r+(self.r*0.25) for i in range(3)]
        else:
            self.SphereObj = Sphere(res=30,rep=rep,colors=colors)
            #self.joint_scale = [self.r for i in range(3)]
            self.joint_scale = [self.r+(self.r*0.02) for i in range(3)]
        super().__init__(res,rep)
        
    
    
    def norm(self, v):
        len_ = np.linalg.norm(v)
        if np.mean(np.abs(len_))==0:
            return v
        else:
            return v/len_
        
    
    def rotateVec(self,V1,V2): 
        V1, V2 = np.array(V1), np.array(V2)
        V2 = self.norm(V2)
        
        angle = math.acos(np.dot(V1,V2))
        axis = self.norm(np.cross(V1,V2))
        
        _gl.glRotatef(angle*(180/math.pi), *axis)
        
    
    def drawParts(self):
        
        _gl.glEnable(_gl.GL_CULL_FACE)
        
        for i,point in enumerate(self.w_points[:-1]):
            n_ind = (i+1)%len(self.w_points)
            n_point = self.w_points[n_ind]
            
            delta_v = list(np.array(n_point) - np.array(point))
            length = np.linalg.norm(delta_v)
            
            _gl.glPushMatrix()
            
            _gl.glTranslatef(*point)
            self.rotateVec([0,1,0],delta_v)
            _gl.glScalef(self.r,length,self.r)
            
            self.drawPart(_gl.GL_QUAD_STRIP,0,int(self.n_points/3))
            _gl.glPopMatrix()
            
            # Draw joint.
            if i!=0:
                self.SphereObj.draw(t=point,s=self.joint_scale)
        
        self.SphereObj.draw(t=self.w_points[-1],s=self.joint_scale)
        
        _gl.glDisable(_gl.GL_CULL_FACE)
    
    
    def getData(self):
        vdata, cdata, ndata, tdata = [],[],[],[]
        
        
        for th in np.arange(360, -self.res, -self.res):
            vdata.extend([Cos(th),0,Sin(th)])
            ndata.extend([Cos(th),0,Sin(th)])
            
            vdata.extend([Cos(th),1,Sin(th)])
            ndata.extend([Cos(th),0,Sin(th)])
            
            
        
        vdata.extend(vdata[:6])
        ndata.extend(ndata[:6])
            
        # Handle the colors last.
        if len(self.colors)==0:
            cdata = [1 for i in range(len(vdata))]
        elif len(self.colors)==3:
            cdata = list(np.tile(self.colors,int(len(vdata)/3)))
        else:
            cdata = self.colors
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            np.array(vdata), np.array(cdata), np.array(ndata), np.array(tdata)
            
            
            










class Cylinder(GenericObject):
    '''
    Draw a basic cylinder.
    '''
    
    def __init__(self,res,colors=[1,1,1]):
        self.colors = colors
        super().__init__(res,None)
        
        
    def drawParts(self):
        self.drawPart(_gl.GL_QUAD_STRIP,0,int(self.n_points/3))
    
    
    def getData(self):
        vdata, cdata, ndata, tdata = [],[],[],[]
        
        
        # Bottom
        bottomv, bottomn = [], []
        for th in np.arange(360, -self.res, -self.res):
            bottomv.extend([0,0,0])
            bottomn.extend([0,-1,0])
            
            bottomv.extend([Cos(th),0,Sin(th)])
            bottomn.extend([0,-1,0])
        bottomv.extend(bottomv[:6])
        bottomn.extend(bottomn[:6])
        
        
        # Sides
        sidev, siden = [], []
        for th in np.arange(360, -self.res, -self.res):
            sidev.extend([Cos(th),1,Sin(th)])
            siden.extend([Cos(th),0,Sin(th)])
            
            sidev.extend([Cos(th),0,Sin(th)])
            siden.extend([Cos(th),0,Sin(th)])
            
        sidev.extend(sidev[:6])
        siden.extend(siden[:6])
        
        # Top
        topv, topn = [], []
        for th in np.arange(360, -self.res, -self.res):
            topv.extend([0,1,0])
            topn.extend([0,1,0])
            
            topv.extend([Cos(th),1,Sin(th)])
            topn.extend([0,1,0])
        topv.extend(topv[:6])
        topn.extend(topn[:6])
        
        
        vdata.extend(bottomv)
        vdata.extend(sidev)
        vdata.extend(topv)
        
        ndata.extend(bottomn)
        ndata.extend(siden)
        ndata.extend(topn)
        
        
        
        # Handle the colors last.
        if len(self.colors)==0:
            cdata = [1 for i in range(len(vdata))]
        elif len(self.colors)==3:
            cdata = list(np.tile(self.colors,int(len(vdata)/3)))
        else:
            cdata = self.colors
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            np.array(vdata), np.array(cdata), np.array(ndata), np.array(tdata)









class OpenCone(GenericObject):
    '''
    Draw a basic cone with an open face. Normals inverted.
    '''
    
    def __init__(self,res,colors=[1,1,1]):
        self.colors = colors
        super().__init__(res,None)
        
        
    def drawParts(self):
        self.drawPart(_gl.GL_QUAD_STRIP,0,int(self.n_points/3))
    
    
    def getData(self):
        vdata, cdata, ndata, tdata = [],[],[],[]
        
        c_points = list(range(360,-self.res,-self.res))
        self.c_pt = len(c_points)
        
        
        # Define data for cone.
        for i in c_points:
            vdata.extend([Cos(i),0,Sin(i)])
            cdata.extend([1,1,1])
            ndata.extend([-Cos(i),-Sin(45),-Sin(i)])
            
            # Define data for point of spike.
            vdata.extend([0,1,0])
            cdata.extend([1,1,1])
            ndata.extend([-Cos(i),-Sin(45),-Sin(i)])
        
        # The quad strip needs the first two points again.
        vdata.extend(vdata[:6])
        cdata.extend(cdata[:6])
        ndata.extend(ndata[:6])
        
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            np.array(vdata), np.array(cdata), np.array(ndata), np.array(tdata)



    






class Sphere(GenericObject):
    '''
    Draw a hollow sphere.
    '''
    
    def __init__(self, res, rep=[1,1], colors=[]):
        self.colors = colors
        super().__init__(res,rep)
        
    def drawParts(self):
        self.drawPart(_gl.GL_QUAD_STRIP,0,int(self.n_points/3))
    
    def getData(self):
        vdata, cdata, ndata, tdata = [],[],[],[]
        
        up_down = range(-90,90+self.res,self.res)
        around = range(360,0-self.res,-self.res)
        for m,i in enumerate(up_down):
            for n,j in enumerate(around):
                vdata.extend(Polar(j,i+self.res))
                ndata.extend(Polar(j,i+self.res))
                
                vdata.extend(Polar(j,i))
                ndata.extend(Polar(j,i))
                
        
        
        for i in range(0,len(vdata),3):
            u = self.rep[0]*((vdata[i]+1)/(2*math.pi))
            v = self.rep[1]*((vdata[i+2]+1)/(2*math.pi))
            tdata.extend([u,v])
            
        # Handle the colors last.
        if len(self.colors)==0:
            cdata = [1 for i in range(len(vdata))]
        elif len(self.colors)==3:
            cdata = list(np.tile(self.colors,int(len(vdata)/3)))
        else:
            cdata = self.colors
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            np.array(vdata), np.array(cdata), np.array(ndata), np.array(tdata)
    




class Box(GenericObject):
    '''
    Draw a hollow box.
    '''
    
    def __init__(self, delside=None, rep=[1,1], colors=[]):
        self.colors = colors
        self.delside = delside
        super().__init__(None,rep)
    
    
    def norm(self, v):
        len_ = np.linalg.norm(v)
        if np.mean(np.abs(len_))==0:
            return v
        else:
            return v/len_
    
    
    def drawParts(self):
        self.drawPart(_gl.GL_QUADS,0,int(self.n_points/3))
    
    def getData(self):
        vdata, cdata, ndata, tdata = [],[],[],[]
        
        # Cube with X left (-) and right (+), and z front (-) to back (+).
        vdata=[0.5, 0.5, 0.5,  -0.5, 0.5, 0.5,  -0.5,-0.5, 0.5,  0.5,-0.5, 0.5,      # Front
               0.5, 0.5, 0.5,   0.5,-0.5, 0.5,   0.5,-0.5,-0.5,  0.5, 0.5,-0.5,      # Right
               0.5, 0.5, 0.5,   0.5, 0.5,-0.5,  -0.5, 0.5,-0.5, -0.5, 0.5, 0.5,      # Top
               -0.5, 0.5, 0.5,  -0.5, 0.5,-0.5,  -0.5,-0.5,-0.5, -0.5,-0.5, 0.5,     # Left
               -0.5,-0.5,-0.5,   0.5,-0.5,-0.5,   0.5,-0.5, 0.5, -0.5,-0.5, 0.5,     # Bottom
               0.5,-0.5,-0.5,  -0.5,-0.5,-0.5,  -0.5, 0.5,-0.5,  0.5, 0.5,-0.5]      # Back
        
        # Remove a side's data, if needed.
        if self.delside is not None:
            i=self.delside
            new_vdata = []
            new_vdata = vdata[:i*12]
            new_vdata.extend(vdata[(i+1)*12:])
            vdata = new_vdata
        
        # Calculate normals.
        for i in range(0,len(vdata),4*3):
            v1 = np.array(vdata[i:i+3])
            v2 = np.array(vdata[i+3:i+6])
            v3 = np.array(vdata[i+9:i+12])
            
            face_normal = list(np.cross(v2-v1,v3-v1))
            for j in range(4):
                ndata.extend(face_normal)
        
        
        # Handle the colors last.
        if len(self.colors)==0:
            cdata = [1 for i in range(len(vdata))]
        elif len(self.colors)==3:
            cdata = list(np.tile(self.colors,int(len(vdata)/3)))
        elif len(self.colors)==4:
            cdata = list(np.tile(self.colors,int(len(vdata)/3)))
            self.color_len = 4
        else:
            cdata = self.colors
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            np.array(vdata), np.array(cdata), np.array(ndata), np.array(tdata)





def drawContainer(l,w,h1,h2):
    
    
    
    container = Box(delside=2,colors = [0.1,0.1,0.1])
    container.draw(s=[l,h1,w],t=[0,-h1/2,0])
    
    _gl.glEnable(_gl.GL_POLYGON_OFFSET_FILL)
    _gl.glPolygonOffset(1,1)
    _gl.glEnable(_gl.GL_CULL_FACE)
    _gl.glCullFace(_gl.GL_FRONT)
    
    _gl.glDepthMask(1)
    _gl.glEnable(_gl.GL_BLEND)
    _gl.glBlendFunc(_gl.GL_SRC_COLOR,_gl.GL_ONE_MINUS_SRC_ALPHA)
    glass = Box(delside=4, colors = [0,0,1,0.8])
    glass.draw(s=[l,h2,w],t=[0,h2/2,0])
    _gl.glDisable(_gl.GL_BLEND)
    
    
    
    _gl.glDisable(_gl.GL_CULL_FACE)
    _gl.glDisable(_gl.GL_POLYGON_OFFSET_FILL)
    
def drawContainerWalls(l,w,h1,h2):
    
    light_blue = np.array([0,191,255])/255
    _gl.glColor3f(*light_blue.tolist())
    
    _gl.glBegin(_gl.GL_LINES)
    
    _gl.glVertex3f(-l/2,0,-w/2)
    _gl.glVertex3f(-l/2,h2,-w/2)
    
    _gl.glVertex3f(-l/2,0,w/2)
    _gl.glVertex3f(-l/2,h2,w/2)
    
    _gl.glVertex3f(l/2,0,-w/2)
    _gl.glVertex3f(l/2,h2,-w/2)
    
    _gl.glVertex3f(l/2,0,w/2)
    _gl.glVertex3f(l/2,h2,w/2)
    
    
    _gl.glVertex3f(-l/2,h2,-w/2)
    _gl.glVertex3f(-l/2,h2,w/2)
    
    _gl.glVertex3f(-l/2,h2,w/2)
    _gl.glVertex3f(l/2,h2,w/2)
    
    _gl.glVertex3f(l/2,h2,w/2)
    _gl.glVertex3f(l/2,h2,-w/2)
    
    _gl.glVertex3f(l/2,h2,-w/2)
    _gl.glVertex3f(-l/2,h2,-w/2)
    
    _gl.glEnd()



