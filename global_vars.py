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



