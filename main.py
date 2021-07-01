#!/usr/bin/env python3

import OpenGL.GL as _gl
import OpenGL.GLU as _glu
import OpenGL.GLUT as _glut

import sys
import os
import numpy as np
from copy import copy

from DrawLight import Light
from help_funcs import PrintText, printText, importTexture, ErrCheck

from SimpleObjects import drawContainer, drawContainerWalls
from BaseSpecies import Crawler
from world_objects import Terrain, Skybox, Lamp, Table

from shaders import shader_strings
from shader_functions import activateShader


''' -------- Global Variables -------- '''

from global_vars import glight, Cos, Sin, init_cam_pos, inspect_cam_pos
light = glight.copy()

lightpos = None
lamp_move = [0,-2.5,-20]
lamp_rot = [90,0,1,0]

obs = {}
obs_init={}
creatures={}
shaders = {}
skybox_textures={}
table_texture= None
on=True
scale_size=0.5


free_sim_mode = True

world_bounds = {'x':[-10,10],
                'y':[-10,10],
                'z':[-10,10]}
creature_locs = {}
creature_boxes = {}
total_count=0


tvars={'f':0,'g':0,'h':1}

# Camera variable dictionaries.

cam_p = init_cam_pos.copy()
cam_vars = {'th_h': -25, 'phi_v': -15}
'''
cam_vars = {'th_h':0,
            'phi_v':-30}
'''

# Window dimensions (width, height).
w, h = 1000, 1000

''' ---------------------------------- '''

















def setLight(P=None):
    global lightpos
    
    A = [0.01*light['ambient'], 0.01*light['ambient'], 0.01*light['ambient'], 1]
    D = [0.01*light['diffuse'], 0.01*light['diffuse'], 0.01*light['diffuse'], 1]
    
    if lightpos is None or not free_sim_mode:
        P = [light['d']*Cos(light['zh']),
             light['y'],
             light['d']*Sin(light['zh']),
             1]
        scale = [0.1,0.1,0.1]
    
    else:
        P = copy(lightpos)
        P = np.array(P)+ np.array(lamp_move)
        
        P = P + np.array([-lightpos[0],0,-lightpos[0]])
        
        P = P.tolist()
        P.append(1)
        scale = [1,1,1]
    
    obs['light'].draw(s=scale,t=P[:-1])
    
    
    _gl.glEnable(_gl.GL_LIGHTING)
    
    _gl.glLightModeli(_gl.GL_LIGHT_MODEL_LOCAL_VIEWER, light['local'])
    
    _gl.glColorMaterial(_gl.GL_FRONT_AND_BACK, _gl.GL_AMBIENT_AND_DIFFUSE)
    _gl.glEnable(_gl.GL_COLOR_MATERIAL)
    
    _gl.glEnable(_gl.GL_LIGHT0)
    
    _gl.glLightfv(_gl.GL_LIGHT0, _gl.GL_AMBIENT, A)
    _gl.glLightfv(_gl.GL_LIGHT0, _gl.GL_DIFFUSE, D)
    _gl.glLightfv(_gl.GL_LIGHT0, _gl.GL_POSITION, P)
    _gl.glLightfv(_gl.GL_LIGHT0,_gl.GL_SPECULAR,[1,1,1,1])
    
    _gl.glMaterialfv(_gl.GL_FRONT_AND_BACK,_gl.GL_SHININESS,[16]);
    _gl.glMaterialfv(_gl.GL_FRONT_AND_BACK,_gl.GL_SPECULAR,[0,0,0,1]);
    _gl.glMaterialfv(_gl.GL_FRONT_AND_BACK,_gl.GL_EMISSION,[0,0,0,1])
    
    return A,D,P



def display():
    
    
    # Clear screen.
    _gl.glClear(_gl.GL_COLOR_BUFFER_BIT|_gl.GL_DEPTH_BUFFER_BIT)
    _gl.glLoadIdentity()
    
    tex=importTexture('dirt3.bmp',1, 1)
    
    
    
    
    # First person camera.
    _glu.gluLookAt(*list(cam_p.values()))
    
    _gl.glEnable(_gl.GL_NORMALIZE)
    
    if light['smooth']:
         _gl.glShadeModel( _gl.GL_SMOOTH)
    else:
         _gl.glShadeModel(_gl.GL_FLAT)
    
    
    
    
    
    if light['on']:
        A,D,P = setLight()
    else:
      _gl.glDisable(_gl.GL_LIGHTING)
    
    
    try:
        prog_list = [shaders['burn'],shaders['spawn'],shaders['base']]
        for name in list(creatures.keys()):
            creatures[name].draw(ADP=[A,D,P],
                                 shaderprogs=prog_list)
    
    except Exception as e:
        print ('here',e)
    
    
    '''
    try:
        #pipe = Pipe3([0,1,0],res=15,r=0.1,phi=tvars['f'],alpha=tvars['g'])
        #pipe.draw()
        obs['pipe'].draw()
    except Exception as e:
        print ('draw',e)
    
    
    '''
    _gl.glUseProgram(0)
    
    
    # Draw the terrain in the container.
    obs['terrain'].draw(tex=tex,s=[0.5,0.5,0.5],t=[-10,-1,-10])
    
    
    
    # Draw the lamp.
    obs['lamp'].draw(t=lamp_move, r=lamp_rot)
    
    
    # Draw the table/floor.
    _gl.glEnable(_gl.GL_POLYGON_OFFSET_FILL)
    _gl.glPolygonOffset(1,1)
    obs['table'].draw()
    _gl.glDisable(_gl.GL_POLYGON_OFFSET_FILL)
    
    
    
    
    
    _gl.glDisable(_gl.GL_LIGHTING)
    
    # Draw skybox.
    obs['skybox'].draw()
    
    
    
    
    # Draw the crawler container.
    if light['on']:
        A,D,P = setLight()
    else:
      _gl.glDisable(_gl.GL_LIGHTING)
    drawContainer(l=20,w=20,h1=5,h2=15)
    
    _gl.glDisable(_gl.GL_LIGHTING)
    
    
    # Draw container outline.
    drawContainerWalls(l=20,w=20,h1=5,h2=15)
    
    
    _gl.glColor3f(1,1,1)
    _gl.glBegin(_gl.GL_LINE_STRIP)
    _gl.glVertex3f(-10,0,-10)
    _gl.glVertex3f(-10,0,10)
    _gl.glVertex3f(10,0,10)
    _gl.glVertex3f(10,0,-10)
    _gl.glVertex3f(-10,0,-10)
    _gl.glEnd()
    
    
    
    #  Display parameter values at bottom left of window.
    alive = len(list(creatures.keys()))
    prt_str1, prt_str2 = printText(on=on,n_alive=alive,n_total=total_count,
                                   light=light,freeview=free_sim_mode,
                                   spawnsize=scale_size)
    
    _gl.glWindowPos2i(5,24)
    PrintText(prt_str1+'\n')
    
    _gl.glWindowPos2i(5,5)
    PrintText(prt_str2+'\n')
    
    ErrCheck('display')
    
    # Make screen visible
    _gl.glFlush()
    _glut.glutSwapBuffers()
    
    












def killAll():
    global creatures
    
    for name in list(creatures.keys()):
        creatures[name].stasis=False
        creatures[name].burn=True
        creatures[name].notburning=False


    



def startStopCreatures():
    global creatures
    
    for name in list(creatures.keys()):
        current_speed = creatures[name].movestep
        current_ind = bool(creatures[name].speeds.index(current_speed))
        creatures[name].movestep = creatures[name].speeds[int(not current_ind)]




def spawnCreature(location=None, facing_th=None, stasis=None):
    global creatures, creature_locs, creature_boxes, total_count
    
    name = 'crawler'+str(total_count).zfill(3)
    
    # Generate random locations, but ensure no overlapping hitboxes.
    if location is None:
        attempt = 0
        flag=True
        
        # The first creature needs no location check.
        if len(list(creatures.keys()))==0:
            location = list(np.random.randint(-7,8,3))
            location[1] = 0
            flag=False
        
        
        # Allow 100 location generation attempts before giving up.
        while attempt<100 and flag:
            location = list(np.random.randint(-7,8,3))
            location[1] = 0
            
            loc1 = np.array([location])[:, None, :]
            loc2 = np.array(list(creature_locs.values()))[None, :, :]
            hitboxes = np.array(list(creature_boxes.values()))
            
            distances = np.linalg.norm(loc1 - loc2, axis=-1)
            overlap_check = distances - hitboxes*2
            overlap_check = overlap_check>0
            
            if overlap_check.all():
                flag=False
            
            attempt+=1
        else:
            if attempt>=500:
                return False
    
    
    # Generate random direction of movement.
    if facing_th is None:
        facing_th = np.random.randint(low=0, high=360)
    
    success=False
    tries=0
    
    while not success and tries<10:
        tries+=1
        try:
            creatures[name] = Crawler()
            success = True
        except Exception as e:
            print (f'Creature intitialization exception. Attempt #{tries}/10.')
    
    if not success:
        return False
    
    creatures[name].sizeUpdate(scale_size)
    creatures[name].center_location = location
    creature_locs[name] = location
    creature_boxes[name] = creatures[name].hitbox
    creatures[name].facing[0] = facing_th
    
    
    total_count+=1
    
    if stasis is not None:
        creatures[name].stasis = True
        creatures[name].hatched = True
        creatures[name].size = [1,1,1]
    
    return True












def camUpdate():
    global cam_p
    
    cam_p['C_x'] = Cos(cam_vars['th_h'])+cam_p['E_x']
    cam_p['C_y'] = Sin(cam_vars['phi_v'])+cam_p['E_y']
    cam_p['C_z'] = Sin(cam_vars['th_h'])+cam_p['E_z']
    
    


def camSpecial(key, x, y):
    global cam_vars, on, light, free_sim_mode
    
    # Arrow keys look around.
    if key == _glut.GLUT_KEY_UP and cam_vars['phi_v']<90:
        cam_vars['phi_v'] += 5
        camUpdate()
    elif key == _glut.GLUT_KEY_DOWN and cam_vars['phi_v']>-90:
        cam_vars['phi_v'] -= 5
        camUpdate()
    elif key == _glut.GLUT_KEY_RIGHT:
        cam_vars['th_h'] += 5
        camUpdate()
    elif key == _glut.GLUT_KEY_LEFT:
        cam_vars['th_h'] -= 5
        camUpdate()
    
    
    # F1 toggles creature movement.
    elif key == _glut.GLUT_KEY_F1:
        startStopCreatures()
        on = (not on)
    
    # F2 toggles light movement.
    elif key == _glut.GLUT_KEY_F2:
        light['m'] = (not light['m'])
        
        
    # F3 spawns in a new crawler.
    elif key == _glut.GLUT_KEY_F3:
        
        if free_sim_mode:
            try:
                attempt = spawnCreature()
                if not attempt:
                    print ('There may not be enough room for the requested number of creatures.')
                    print ('Stopping creature generation.')
            except Exception as e:
                print ('spawn',e)
        else:
            try:
                if len(list(creatures.keys()))<1:
                    attempt = spawnCreature(location=[0,0,0],facing_th=0,stasis=True)
                if not attempt:
                    print ('Creature creation failed due to memory exception.')
            except Exception as e:
                print ('spawn2',e)
    
    
    _glut.glutPostRedisplay()



def camKey(ch, x, y):
    global cam_p, cam_vars, free_sim_mode, scale_size
    
    if ch==b'\x1b':
        os._exit(1)
        
    elif ch==b'w':
        cam_p['E_x'] += Cos(cam_vars['th_h'])
        cam_p['E_y'] += Sin(cam_vars['phi_v'])
        cam_p['E_z'] += Sin(cam_vars['th_h'])
        camUpdate()
        
    elif ch==b's':
        cam_p['E_x'] -= Cos(cam_vars['th_h'])
        cam_p['E_y'] -= Sin(cam_vars['phi_v'])
        cam_p['E_z'] -= Sin(cam_vars['th_h'])
        camUpdate()
    
    elif ch==b'd':
        cam_p['E_x'] += Cos(cam_vars['th_h']+90)
        cam_p['E_z'] += Sin(cam_vars['th_h']+90)
        camUpdate()
    
    elif ch==b'a':
        cam_p['E_x'] -= Cos(cam_vars['th_h']+90)
        cam_p['E_z'] -= Sin(cam_vars['th_h']+90)
        camUpdate()
    
    
    
        
    
    # Increase/decrease light distance.
    elif ch==b'-' and light['d']>0:
        light['d']-=1
    elif ch==b'+' or ch==b'=':
        light['d']+=1
    
    # Increase/decrease light height.
    elif ch==b'[' and light['y']>0:
        light['y']-=1
    elif ch==b']':
        light['y']+=1
        
    # Move light sideways.
    elif ch==b',' or ch==b'<':
        light['zh']-=5
    elif ch==b'.' or ch==b'>':
        light['zh']+=5
    
    
    
    
    elif ch==b'f' or ch==b'F':
        if free_sim_mode:
            free_sim_mode = False
            light['d'] = 1
            light['m'] = True
            cam_p = inspect_cam_pos.copy()
            cam_vars = {'th_h':0,'phi_v':-30}
            camUpdate()
            killAll()
        else:
            free_sim_mode = True
            killAll()
            cam_p = init_cam_pos.copy()
            cam_vars = {'th_h': -25, 'phi_v': -15}
            camUpdate()
    
    
    
    elif ch==b'j' or ch==b'J':
        crtrs = list(creatures.keys())
        if not free_sim_mode and len(crtrs)>0:
            name = crtrs[0]
            creatures[name].burn = False
            creatures[name].timevars= {'f':True,'s':0,'el':0}
            creatures[name].spawn = (not creatures[name].spawn)
        
        else:
            if ch==b'j' and scale_size<2:
                scale_size=round(scale_size + 0.05,2)
            elif ch==b'J' and scale_size>0.05:
                scale_size=round(scale_size - 0.05,2)
    
    elif ch==b'k' or ch==b'K':
        crtrs = list(creatures.keys())
        if not free_sim_mode and len(crtrs)>0:
            name = crtrs[0]
            creatures[name].spawn = False
            creatures[name].timevars= {'f':True,'s':0,'el':0}
            creatures[name].burn = (not creatures[name].burn)
        
        else:
            killAll()
    
    
    
    
    
    elif ch==b'Y':
        tvars['f']-=5
    elif ch==b'y':
        tvars['f']+=5
    
    
    elif ch==b'U':
        tvars['g']-=5
    elif ch==b'u':
        tvars['g']+=5
    
    
    _glut.glutPostRedisplay()







# Handle window resizing.
def reshape(width, height):
    w2h = width
    if height>0: w2h = width/height
    
    # Set viewport as whole window.
    _gl.glViewport(0,0,width,height)
    
    # Select projection matrix and set projection to identity
    _gl.glMatrixMode(_gl.GL_PROJECTION)
    _gl.glLoadIdentity()
    
    # Set perspective to 90 deg FOV, res aspect ratio, and near/far boundaries.
    _glu.gluPerspective(90.0, w2h, 0.1, 500.0)
    
    # Select model view matrix and set model view to identity
    _gl.glMatrixMode(_gl.GL_MODELVIEW)
    _gl.glLoadIdentity()
    








def boundCheck(loc,hit):
    tests = [loc[0]+hit>world_bounds['x'][1],
             loc[0]-hit<world_bounds['x'][0],
             loc[2]+hit>world_bounds['z'][1],
             loc[2]-hit<world_bounds['z'][0]]
    
    return any(tests)

# Turn a creature some amount.
# If given a string "shallow" or "wide," pick a random degree.
def turnDeg(name, deg):
    
    t = _glut.glutGet(_glut.GLUT_ELAPSED_TIME)/1000
    
    if t-creatures[name].last_collision>0.5:
    
        if not isinstance(deg,int):
            
            if deg=='shallow':
                deg = np.random.randint(-15,15)
            
            else:
                #deg = 180
                deg = np.random.randint(165,195)
        
        creatures[name].last_collision=t
        look = creatures[name].facing[0]
        creatures[name].facing[0] = (look+deg)%360


def collisionHandler(n1,n2):
    global total_count, creatures, creature_locs, creature_boxes
    
    hetero_check = creatures[n1].sex==creatures[n2].sex                # True if same sex.
    hatch_check = creatures[n1].hatched and creatures[n2].hatched      # True if hatched.
    burn_check = creatures[n1].notburning and creatures[n2].notburning # True if not burning.
    mate_check = creatures[n1].notmated and creatures[n2].notmated     # True if not mated.
    
    # Fight.
    if hetero_check and burn_check:
        if hatch_check:
            dna1 = sum(creatures[n1].dna)
            dna2 = sum(creatures[n2].dna)
            if dna1>dna2:
                return n2
            elif dna1<dna2:
                return n1
            else:
                turnDeg(n1,180)
                turnDeg(n2,180)
    
    # Mate.
    else:
        if mate_check and burn_check:
            
            creatures[n1].notmated = False
            creatures[n2].notmated = False
            
            # Generate 0 or 1 at random.
            r_ind = lambda : np.random.randint(0,2)
            
            # Who is male and who is female.
            if creatures[n1].sex: 
                fname=n1
                mname=n2
            else:
                fname=n2
                mname=n1
            
            # Baby name e.g. crawler005
            total_count+=1
            bname = fname[:-2]+str(total_count).zfill(3)
            newdna = [0,0]
            
            # Determine which dna component the parents send from and to.
            male_ind = r_ind()
            female_ind = int(not bool(male_ind))
            
            
            newdna[male_ind] = creatures[mname].dna[r_ind()]
            newdna[female_ind] = creatures[mname].dna[r_ind()]
            
            # Childbirth.
            success=False
            tries=0
            while not success and tries<10:
                tries+=1
                try:
                    creatures[bname] = Crawler(dna=newdna)
                    success = True
                except Exception as e:
                    print (f'Creature intitialization exception. Attempt #{tries}/10.')
            
            
            creatures[bname].sizeUpdate(scale_size)
            
            mid = list((np.array(creatures[n2].center_location) +\
                        np.array(creatures[n1].center_location))/2)
            creatures[bname].center_location = mid
            creature_locs[bname] = mid
            creature_boxes[bname] = creatures[bname].hitbox
            
            # Everyone goes their separate ways.
            turnDeg(bname,-90)
            turnDeg(n1,180)
            turnDeg(n2,180)
        
        # Still turn away if they've mated once.
        elif not mate_check and burn_check:
            turnDeg(n1,'wide')
            turnDeg(n2,'wide')
        
            
    
    return None
        
    

def worldUpdate(t):
    global creatures, creature_locs, creature_boxes
    
    klist, blist = [], []
    
    for name in list(creatures.keys()):
        alive, loc, hit = creatures[name].update(t)
        
        # Burn list.
        if not alive:
            klist.append(name)
        else:
            creature_locs[name] = loc
            creature_boxes[name] = hit
            
            
            if boundCheck(loc,hit):
                turnDeg(name,'wide')
    
    
    for name1, loc1 in list(creature_locs.items()):
        for name2, loc2 in list(creature_locs.items()):
            if name1!=name2 and creatures[name1].hatched and creatures[name2].hatched:
                dist = np.linalg.norm(np.array(loc2)-np.array(loc1))
                hit_d = creature_boxes[name1]+creature_boxes[name2]
                
                if hit_d>dist:
                    rname = collisionHandler(name1, name2)
                    
                    # KOS list.
                    if rname is not None:
                        blist.append(rname)
               
                    
    # Burn creatures on burn list.
    blist = list(set(blist))
    for name in blist:
        creatures[name].burnUpdate()
    
    
    # Kill creatures on KOS list.
    klist = list(set(klist))
    for name in klist:
        del creatures[name]
        del creature_locs[name]
        del creature_boxes[name]
    
            
            
            
        
                


















# Move light around when idle if this feature is turned on.
def idle():
    
    # Time in seconds.
    t = _glut.glutGet(_glut.GLUT_ELAPSED_TIME)/1000
    
    if light['m']:
        light['zh'] = (90*t)%360
    
    try:
        worldUpdate(t)
    except Exception as e:
        print ('update',e)
    
    _glut.glutPostRedisplay()




# Logging code reference:
# http://www.hivestream.de/opengl-logging-and-debugging.html
def CreateShader(stype,string):
    shader = _gl.glCreateShader(stype)
    _gl.glShaderSource(shader,string)
    #_gl.glShaderSource(shader,1,string,len(string))
    _gl.glCompileShader(shader)
    compilestatus = _gl.glGetShaderiv(shader, _gl.GL_COMPILE_STATUS)
    if compilestatus != _gl.GL_TRUE:
        raise RuntimeError(_gl.glGetShaderInfoLog(shader)
                           .decode('ASCII'))
    
    return shader

def initShaderProg(vshader, fshader):
    prog = _gl.glCreateProgram()
    vert = CreateShader(_gl.GL_VERTEX_SHADER, vshader)
    frag = CreateShader(_gl.GL_FRAGMENT_SHADER, fshader)
    
    _gl.glAttachShader(prog,vert)
    _gl.glAttachShader(prog,frag)
    
    _gl.glLinkProgram(prog)
    linkstatus = _gl.glGetProgramiv(prog, _gl.GL_LINK_STATUS)
    if linkstatus != _gl.GL_TRUE:
        raise RuntimeError(_gl.glGetProgramInfoLog(prog)
                           .decode('ASCII'))
    # validate program
    _gl.glValidateProgram(prog)
    validatestatus = _gl.glGetProgramiv(prog, _gl.GL_VALIDATE_STATUS)
    if validatestatus != _gl.GL_TRUE:
        raise RuntimeError(_gl.glGetProgramInfoLog(prog)
                           .decode('ASCII'))
    
    return prog
















# Initialize objects to be drawn from later.
def initObjects():
    global obs,obs_init,total_count, lightpos
    
    
    obs_init['terrain']=False
    obs_init['skybox']=False
    obs_init['table']=False
    obs_init['lamp']=False
    obs_init['light']=False
    
    check=0
    while not np.array(list(obs_init.values())).all() and check<10:
        check+=1
        try:
            obs['terrain'] = Terrain(max_height=1,width=40,tex_scale=2,use_gouraud=True)
            obs_init['terrain']=True
            
            obs['skybox'] = Skybox(size=[500,500,500], textures = skybox_textures)
            obs_init['skybox']=True
            
            obs['table'] = Table(size=[100,1,100], texture = table_texture)
            obs_init['table']=True
            
            obs['lamp'] = Lamp()
            obs_init['lamp']=True
            lightpos = obs['lamp'].lightpos
            
            obs['light'] = Light(res=15,color=[1,1,1])
            obs_init['light']=True
            
            
        except Exception as e:
            c = str(check)
            print (f'Initialization exception. Attempt #{c}/10.')
    
    
    for i in range(5):
        attempt = spawnCreature()
        if not attempt:
            print ('Creature creation failed due to memory exception.')
    


def initShaders():
    global shader_strings
    shaders['burn'] = initShaderProg(shader_strings['burnv'], shader_strings['burnf'])
    shaders['spawn'] = initShaderProg(shader_strings['spawnv'], shader_strings['spawnf'])
    shaders['base'] = initShaderProg(shader_strings['basev'], shader_strings['basef'])


def main():
    global w, h, skybox_textures, table_texture
    
    # Initialize glut.
    if _glut.glutInit:
        _glut.glutInit(sys.argv)
    
    # Init as single buffer, true color.
    _glut.glutInitDisplayMode(_glut.GLUT_RGB | _glut.GLUT_DOUBLE | _glut.GLUT_DEPTH)
    
    # Initialize window dimensions and location.
    _glut.glutInitWindowSize(w, h)
    _glut.glutInitWindowPosition(50,50)
    
    # Create window and name.
    _glut.glutCreateWindow("Project - Matthew Resnick")
    
    # Register functions that render display/handle events.
    _glut.glutDisplayFunc(display)
    _glut.glutReshapeFunc(reshape)
    _glut.glutSpecialFunc(camSpecial)
    _glut.glutKeyboardFunc(camKey)
    _glut.glutIdleFunc(idle)
    
    
    # Enable Z-buffer depth test
    _gl.glEnable(_gl.GL_DEPTH_TEST)
    _gl.glDepthMask(1)
    
    # Face culling.
    #_gl.glEnable(_gl.GL_CULL_FACE)
    
    # Initialize objects and cam positions.
    camUpdate()
    initShaders()
    
    
    skybox_textures = {'front':importTexture('posz.bmp',1, 1),
                       'right':importTexture('posx.bmp',1, 1),
                       'top':importTexture('posy.bmp',1, 1),
                       'left':importTexture('negx.bmp',1, 1),
                       'bottom':importTexture('negy.bmp',1, 1),
                       'back':importTexture('negz.bmp',1, 1)}
    
    table_texture = importTexture('wood.bmp',1, 1)
    
    initObjects()
    
    # Pass control to glut
    _glut.glutMainLoop()

main()
