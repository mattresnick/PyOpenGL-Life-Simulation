import OpenGL.GL as _gl

import math
import numpy as np
from SimpleObjects import GenericObject, GenericTexturedObject, Sphere, Cylinder, OpenCone

from global_vars import Sin, Cos


class Terrain(GenericTexturedObject):
    '''
    Terrain creation class. Autogenerates varied terrain, though I may add the
    option of saving the terrain values to file and then loading them in,
    if that gives a significant enough performance boost.
    
    Also, as of now the terrain is generated only in a square shape.
    '''
    
    def __init__(self, max_height, width, color=[1,1,1], tex_scale=1, use_gouraud=False):
        
        self.colors = color
        self.mh = max_height
        self.n = width
        self.use_gouraud = use_gouraud
        
        # Scale value corresponds to 2^s appearances of the texture image.
        self.s = 1/tex_scale
        
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
    
    
    def genTriangles(self):
        '''
        Generates all of the triangles needed for terrain. The trouble is
        generating a flat grid of tesselating triangles, and then raising 
        the vertices to random heights. 
        
        The reason it's difficult is we must keep track of what traingles 
        share vertices, and then only raise those vertices by the same amount.
        
        The result is a list of vertices of the shape (n*n*2 X 3 X 3), where 
        there are n*n*2 triangles with 3 xyz vertices each.
        '''
        t_0 = [[0,0],[1,0],[1,1]]
        t_1 = [[0,0],[1,1],[0,1]]
        
        flat_triangles = []
        for i in range(self.n):
            for j in range(self.n):
                
                # At each grid point, make two triangles shifted by the
                # appropriate x and z values.
                for t_x in [t_0, t_1]:
                    t_2 = []
                    for p in range(3):
                        t_2.append([t_x[p][0]+i,t_x[p][1]+j])
                    flat_triangles.append(t_2)
        
        flat_triangles = np.array(flat_triangles)
        
        unique_pairs = np.unique(flat_triangles.reshape(-1,2),axis=0)
        
        xyz_verts = []
        for pair in unique_pairs:
            height = np.random.rand()*self.mh
            xyz_verts.append([pair[0],height,pair[1]])
        
        xyz_verts = np.array(xyz_verts)
        
        
        
        # Replace elements of flat traingles with elements of xyz_verts when the 
        # flat triangles element is equivalent to the same index in unique_pairs
        all_triangles = []
        for triangle in flat_triangles:
            new_triangle=[]
            for vert in triangle:
                new_vert_ind = self.arrIndInNestedArr(unique_pairs,vert.reshape((1,2)))[0]
                new_triangle.append(xyz_verts[new_vert_ind])
            
            all_triangles.append(new_triangle)
        
        return np.array(all_triangles), flat_triangles
    
    
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
        
        triangles, tex_grid = self.genTriangles()
        normals = self.genNormals(triangles)
        
        
        if self.use_gouraud:
            normals = self.avgNorms(triangles, normals)
                
                
        
        # Make data 1D for VBOs.
        vdata = triangles.ravel()
        ndata = normals.ravel()
        
        # Produce texture data and make 1D.
        texture_values = tex_grid/(self.n*self.s)
        tdata = texture_values.ravel()
        
        cdata = list(np.tile(self.colors,int(len(vdata)/3)))
        
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            vdata, np.array(cdata), ndata, tdata





class Box(GenericObject):
    '''
    Draw a hollow box.
    '''
    
    def __init__(self, rep=[1,1], colors=[]):
        self.colors = colors
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
        else:
            cdata = self.colors
        
        self.vdata, self.cdata, self.ndata, self.tdata = \
            np.array(vdata), np.array(cdata), np.array(ndata), np.array(tdata)




class Skybox:
    
    
    def __init__(self, size, textures):
        self.size = size
        self.textures = textures
    
    
    
    def drawWall(self,name):
        
        verts = self.getData(name)
        tex = self.textures[name]
        
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glBindTexture(_gl.GL_TEXTURE_2D, tex)
        
        _gl.glBegin(_gl.GL_QUADS)
        
        # Had to ham-fist this because I didn't want to think about
        # texture orientations.
        if name in ['right']:
            _gl.glTexCoord2f(0,0)
            _gl.glVertex3f(*verts[0])
            
            _gl.glTexCoord2f(0,1) 
            _gl.glVertex3f(*verts[1])
            
            _gl.glTexCoord2f(1,1) 
            _gl.glVertex3f(*verts[2])
            
            _gl.glTexCoord2f(1,0)
            _gl.glVertex3f(*verts[3])
        
        elif name in ['back']:
            _gl.glTexCoord2f(0,1)
            _gl.glVertex3f(*verts[0])
            
            _gl.glTexCoord2f(1,1) 
            _gl.glVertex3f(*verts[1])
            
            _gl.glTexCoord2f(1,0) 
            _gl.glVertex3f(*verts[2])
            
            _gl.glTexCoord2f(0,0)
            _gl.glVertex3f(*verts[3])
        
        elif name in ['bottom']:
            _gl.glTexCoord2f(0,1)
            _gl.glVertex3f(*verts[0])
            
            _gl.glTexCoord2f(1,1) 
            _gl.glVertex3f(*verts[1])
            
            _gl.glTexCoord2f(1,0) 
            _gl.glVertex3f(*verts[2])
            
            _gl.glTexCoord2f(0,0)
            _gl.glVertex3f(*verts[3])
        
        
        elif name in ['top']:
            _gl.glTexCoord2f(1,1)
            _gl.glVertex3f(*verts[0])
            
            _gl.glTexCoord2f(1,0) 
            _gl.glVertex3f(*verts[1])
            
            _gl.glTexCoord2f(0,0) 
            _gl.glVertex3f(*verts[2])
            
            _gl.glTexCoord2f(0,1)
            _gl.glVertex3f(*verts[3])
        
        else:
            _gl.glTexCoord2f(1,0)
            _gl.glVertex3f(*verts[0])
            
            _gl.glTexCoord2f(0,0) 
            _gl.glVertex3f(*verts[1])
            
            _gl.glTexCoord2f(0,1) 
            _gl.glVertex3f(*verts[2])
            
            _gl.glTexCoord2f(1,1)
            _gl.glVertex3f(*verts[3])
        
        _gl.glEnd()
        
        _gl.glDisable(_gl.GL_TEXTURE_GEN_S)
        _gl.glDisable(_gl.GL_TEXTURE_GEN_T)
        _gl.glDisable(_gl.GL_TEXTURE_2D)
        
        
    
    def draw(self):
        
        
        _gl.glPushMatrix()
        
        _gl.glScalef(*self.size)
        
        self.drawWall('front')
        self.drawWall('right')
        self.drawWall('top')
        self.drawWall('left')
        self.drawWall('bottom')
        self.drawWall('back')
        
        _gl.glPopMatrix()
        
    def getData(self,side):
        # Cube with X left (-) and right (+), and z front (-) to back (+).
        
        vdata = {'front':[[0.5, 0.5, 0.5],  [-0.5, 0.5, 0.5],  [-0.5,-0.5, 0.5],  [0.5,-0.5, 0.5]],
                 'right':[[0.5, 0.5, 0.5],   [0.5,-0.5, 0.5],   [0.5,-0.5,-0.5], [ 0.5, 0.5,-0.5]],
                 'top':[[0.5, 0.5, 0.5],   [0.5, 0.5,-0.5],  [-0.5, 0.5,-0.5], [-0.5, 0.5, 0.5]],
                 'left':[[-0.5, 0.5, 0.5],  [-0.5, 0.5,-0.5],  [-0.5,-0.5,-0.5], [-0.5,-0.5, 0.5]],
                 'bottom':[[-0.5,-0.5,-0.5],   [0.5,-0.5,-0.5],   [0.5,-0.5, 0.5], [-0.5,-0.5, 0.5]],
                 'back':[[0.5,-0.5,-0.5],  [-0.5,-0.5,-0.5],  [-0.5, 0.5,-0.5],  [0.5, 0.5,-0.5]]}
        
        return vdata[side]
        
        
        


class Table:
    
    def __init__(self, size, texture):
        self.size = size
        self.texture = texture
    
    
    
    def draw(self, rep=1):
        
        
        _gl.glPushMatrix()
        
        _gl.glTranslatef(0,-2.5,0)
        _gl.glScalef(*self.size)
        
        
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glBindTexture(_gl.GL_TEXTURE_2D, self.texture)
        
        _gl.glBegin(_gl.GL_QUADS)
        
        _gl.glTexCoord2f(0,0)
        _gl.glVertex3f(-0.5,0,-0.5)
        
        _gl.glTexCoord2f(0,rep) 
        _gl.glVertex3f(0.5,0,-0.5)
        
        _gl.glTexCoord2f(rep,rep) 
        _gl.glVertex3f(0.5,0, 0.5)
        
        _gl.glTexCoord2f(rep,0)
        _gl.glVertex3f(-0.5,0, 0.5)
        
        _gl.glEnd()
        
        _gl.glDisable(_gl.GL_TEXTURE_GEN_S)
        _gl.glDisable(_gl.GL_TEXTURE_GEN_T)
        _gl.glDisable(_gl.GL_TEXTURE_2D)
        
        _gl.glPopMatrix()



class Lamp:
    
    def __init__(self):
        self.base = Cylinder(res=15)
        
        self.arm = Cylinder(res=60)
        
        self.joint = Sphere(res=30)
        
        self.face = OpenCone(res=15)
        
        self.bulb = Sphere(res=30,colors=[0.25,0.25,0.25])
        
        self.knob = Cylinder(res=60,colors=[0.5,0.5,0.5])
        
        
        self.th = 50
        self.lstretch = 4
        self.joint2loc = [-2.8,5.5+3*Sin(90-self.th),0]
        
        self.lightpos = [(-2.1+(self.lstretch/2))-self.lstretch,
                         self.joint2loc[1]-0.4,
                         0]
    
    
    def draw(self,s=None,r=None,t=None):
        _gl.glPushMatrix()
        
        if t is not None:
            _gl.glTranslatef(*t)
        
        if r is not None:
            _gl.glRotatef(*r)
        
        if s is not None:
            _gl.glScalef(*s)
        
        
        # Base
        self.base.draw(s=[2.5,0.5,2.5])
        
        # Arm1
        self.arm.draw(t=[0,0.5,0],
                      s=[1.25/2,5,1.25/2])
        
        # Joint1
        self.joint.draw(t=[0,5.5,0],
                        s=[0.9,0.9,0.9])
        
        # Arm2
        self.arm.draw(t=[0,5.5,0],
                      r=[self.th,0,0,1],
                      s=[1.25/2,3,1.25/2])
        
        # Joint2
        self.joint.draw(t=self.joint2loc,
                        s=[1.1,1.1,1.1])
        
        # Face
        self.face.draw(t=[-1.6-self.lstretch,self.joint2loc[1]-0.9,0],
                       r=[-70,0,0,1],
                       s=[2,self.lstretch,2])
        
        
        # Knob
        self.knob.draw(t=[-2.2,self.joint2loc[1]+0.3,0],
                       r=[-70,0,0,1],
                       s=[1.25/3,1.5,1.25/3])
        
        # "Off" bulb
        self.bulb.draw(t=self.lightpos,
                       s=[0.95,0.95,0.95])
        
        _gl.glPopMatrix()
        
    
    

