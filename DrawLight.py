import OpenGL.GL as _gl

import numpy as np
from ctypes import c_float

from global_vars import Polar



class Light:
    
    def __init__(self, res, color):
        self.res = res
        self.color = color
        self.initializeData()
        
    def initializeData(self):
        
        # Calculate vertices.
        vcoords = []
        for i in range(-90,90+self.res,self.res):
            for j in range(360,0-self.res,-self.res):
                vcoords.extend(Polar(j,i))
                vcoords.extend(Polar(j,i+self.res))
        
        n_points = int(len(vcoords)/3)
        
        # Calculate colors.
        vcolors = np.tile(np.array(self.color),n_points).tolist()
        
        # Calculate vertex/color lists from indices.
        inds = list(range(n_points))
        vdata, cdata = [], []
        for val in inds:
            vdata.extend(vcoords[val*3:val*3+3])
            cdata.extend(vcolors[val*3:val*3+3])
        vdata = np.array(vdata)
        cdata = np.array(cdata)
        
        # Convert data to appropriate form for buffers.
        self.n_points = len(vdata)
        self.fsize = vdata.itemsize
        
        self.vert_data = (c_float*len(vdata))(*vdata)
        self.color_data = (c_float*len(cdata))(*cdata)
        
        # Initialize VBO for vertices.
        self.vbo_v = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_v)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points*self.fsize,
                         self.vert_data,
                         _gl.GL_STATIC_DRAW)
        
        # Initialize VBO for colors.
        self.vbo_c = _gl.glGenBuffers(1)
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER, self.vbo_c)
        _gl.glBufferData(_gl.GL_ARRAY_BUFFER,
                         self.n_points*self.fsize,
                         self.color_data,
                         _gl.GL_STATIC_DRAW)
        
    
        
    def draw(self, s=None, r=None, t=None):
        
        _gl.glPushMatrix()
        if t is not None:
            _gl.glTranslatef(*t)
        
        if r is not None:
            _gl.glRotatef(*r)
            
        if s is not None:
            _gl.glScalef(*s)
        
        _gl.glMaterialfv(_gl.GL_FRONT,_gl.GL_EMISSION,[0.0,0.0,0.0,1])
        self.drawParts()
        
        _gl.glPopMatrix()
        
        

        
        
        
    def drawParts(self):
        
        # "Turn on" VBOs.
        _gl.glEnableClientState(_gl.GL_VERTEX_ARRAY)
        _gl.glEnableClientState(_gl.GL_COLOR_ARRAY)
        #_gl.glEnableClientState(_gl.GL_NORMAL_ARRAY)
        
        # Bind vertex VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_v)
        _gl.glVertexPointer(3,_gl.GL_FLOAT,0,None)
        
        # Bind color VBO with pointer.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,self.vbo_c)
        _gl.glColorPointer(3,_gl.GL_FLOAT,0,None)
        
        # Reset.
        _gl.glBindBuffer(_gl.GL_ARRAY_BUFFER,0)
        
        
        # Draw polygons.
        _gl.glDrawArrays(_gl.GL_QUAD_STRIP,0,int(self.n_points/3))
        
        
        # "Turn off" VBOs
        _gl.glDisableClientState(_gl.GL_VERTEX_ARRAY)
        _gl.glDisableClientState(_gl.GL_COLOR_ARRAY)








