import OpenGL.GL as _gl
import OpenGL.GLU as _glu
import OpenGL.GLUT as _glut

import ctypes
import numpy as np
from PIL import Image


# Makes prinited text suitable to be represented graphically.
def PrintText(text):
    for ch in text:
        _glut.glutBitmapCharacter(_glut.GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(ch)))



# Generates text to be displayed in the bottom left of the window.
def printText(on, n_alive, n_total, light, freeview, spawnsize):
    
    if light['m']: m='on'
    else: m='off'
    
    y = light['y']
    d = light['d']
    
    
    prt_str1=f'Number alive: {n_alive} | Total all-time: {n_total}. | '
    
    if freeview:
        prt_str1 = prt_str1 + 'View mode: free view.'
        prt_str2=f'Creature movement on: {on} | Spawn size: {spawnsize}.'
        
    else:
        prt_str1 = prt_str1 + 'View mode: inspect view.'
        
        prt_str2 = f'Light height: {y} | Light distance {d} | '
        prt_str2 = prt_str2 + f'Light movement: {m}.'
        
    
    return prt_str1, prt_str2




def importTexture(filename, f, g):
    tex_path = './textures/'
    im = Image.open(tex_path+filename)
    im_arr = np.array(list(im.getdata()))
    
    # Generate texture ID and bind.
    textID = _gl.glGenTextures(1)
    _gl.glBindTexture(_gl.GL_TEXTURE_2D,textID)
    _gl.glPixelStorei(_gl.GL_UNPACK_ALIGNMENT, 1)
    
    # Set texture parameters.
    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_S, _gl.GL_CLAMP)
    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_T, _gl.GL_CLAMP)
    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_S, _gl.GL_MIRRORED_REPEAT)
    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_T, _gl.GL_MIRRORED_REPEAT)
    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_MAG_FILTER, _gl.GL_LINEAR)
    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_MIN_FILTER, _gl.GL_LINEAR)
    
    # Set texture environment parameters.
    _gl.glTexEnvf(_gl.GL_TEXTURE_ENV, _gl.GL_TEXTURE_ENV_MODE, _gl.GL_MODULATE)
    
    if im.mode=='RGB': c_mode = _gl.GL_RGB 
    else: c_mode = _gl.GL_RGBA
    
    _gl.glTexImage2D(_gl.GL_TEXTURE_2D, 0, _gl.GL_RGB, im.size[0], im.size[1], 0, c_mode, _gl.GL_UNSIGNED_BYTE, im_arr)
    
    
    _gl.glMatrixMode(_gl.GL_TEXTURE)
    _gl.glLoadIdentity()
    
    _gl.glScalef(f, g, 1)
    
    _gl.glMatrixMode(_gl.GL_MODELVIEW)
    _gl.glLoadIdentity()
    
    return textID



def ErrCheck(where):
    err = _gl.glGetError()
    if err: 
        err_name = _glu.gluErrorString(err)
        print (f'{err_name}: {where}. (---)')