import math

Cos = lambda x: math.cos((x)*math.pi/180)
Sin = lambda x: math.sin((x)*math.pi/180) 

Polar = lambda t,p: [Sin(t)*Cos(p), Sin(p), Cos(t)*Cos(p)]

r2in = 1/math.sqrt(2)

glight = {'on':True,
         'd':5,            # Distance of light.
         'res':10,
         'smooth':True,
         'local':False,
         'emission':0,
         'ambient':10,
         'diffuse':50,
         'specular':0,
         's':0,            # Shininess (not currently in use)
         'zh':90,          # Rotation angle of the light.
         'y':4,            # Height of the light.
         'm':False}        # Auto movement of light.



init_cam_pos={'E_x': -17.53789311061423, 'E_y': 8.712873029298844, 'E_z': 8.41809892267677, 
              'C_x': -16.671867706829794, 'C_y': 8.539224851631914, 'C_z': 7.918098922676769, 
              'U_x': 0, 'U_y': 1, 'U_z': 0}

inspect_cam_pos={'E_x': -4.0, 'E_y': 2.2860619515673033, 'E_z': 0.0, 
                 'C_x': -3.0, 'C_y': 1.7860619515673033, 'C_z': 0.0, 
                 'U_x': 0, 'U_y': 1, 'U_z': 0}

standard_cam_pos = {'E_x':-8,
                     'E_y':5,
                     'E_z':0,
                     'C_x':0,
                     'C_y':0,
                     'C_z':0,
                     'U_x':0,
                     'U_y':1,
                     'U_z':0}