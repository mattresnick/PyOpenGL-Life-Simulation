burnvshader = \
'''
// Vertex shader for brick and mandelbrot shaders
// Derived from Orange Book Chapter 6
#version 120

//  Light intensity and model position required by fragment shader
varying float LightIntensity;
varying vec3  ModelPos;
varying vec3  vPos;

uniform float Zcenter;
uniform float Xcenter;
uniform float Ycenter;

//  Phong lighting intensity only
float phong()
{
   //  P is the vertex coordinate on body
   vec3 P = vec3(gl_ModelViewMatrix * gl_Vertex);
   //  N is the object normal at P
   vec3 N = normalize(gl_NormalMatrix * gl_Normal);
   //  Light Position for light 0
   vec3 LightPos = vec3(gl_LightSource[0].position);
   //  L is the light vector
   vec3 L = normalize(LightPos - P);
   //  R is the reflected light vector R = 2(L.N)N - L
   vec3 R = reflect(-L, N);
   //  V is the view vector (eye at the origin)
   vec3 V = normalize(-P);

   //  Diffuse light intensity is cosine of light and normal vectors
   float Id = max(dot(L,N) , 0.0);
   //  Shininess intensity is cosine of light and reflection vectors to a power
   float Is = (Id>0.0) ? pow(max(dot(R,V) , 0.0) , gl_FrontMaterial.shininess) : 0.0;

   //  Vertex color
   vec3 color = gl_FrontLightProduct[0].ambient.rgb
           + Id*gl_FrontLightProduct[0].diffuse.rgb
           + Is*gl_FrontLightProduct[0].specular.rgb;

   //  Vertex intensity
   return length(color);
}

void main()
{
   //  Scalar light intensity (for fragment shader)
   LightIntensity = phong();

   //  Save model coordinates (for fragment shader)
   ModelPos = Zcenter*gl_Vertex.xyz - vec3(Xcenter,Ycenter,Zcenter);

   //  Return fixed transform coordinates for this vertex
   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
   
   vPos = vec3(gl_ProjectionMatrix * gl_Vertex);
   
   gl_FrontColor = gl_Color;
}
'''



burnfshader = \
'''
#version 120


const vec4 BurnColor1 = vec4(1.0,0.647,0.0,1.0);
const vec4 BurnColor2 = vec4(1.0,1.0,0.0,1.0);
const vec4 BurnColor3 = vec4(1.0,1.0,1.0,1.0);
const float BurnWidth = 0.03;

//  Model coordinates and light from vertex shader
varying float LightIntensity;
varying vec3  ModelPos;
varying vec3  vPos;

uniform float R;

uniform vec3 pos1;
uniform vec3 pos2;
uniform vec3 pos3;

const float width = 0.05;
uniform vec3 color1;
uniform vec3 color2;



// Noise function thanks to:
// https://thebookofshaders.com/10/
float random (in vec2 _st) {
    return fract(sin(dot(_st.xy,vec2(12.9898,78.233)))*43758.5453123);
}

void main()
{
    float Rn = R;
    
    vec3 position = vPos;
    
    float dist1 = distance(position,pos1);
    float dist2 = distance(position,pos2);
    float dist3 = distance(position,pos3);
    
    // Hole in the object.
    if ((dist1<Rn) || (dist2<Rn) || (dist3<Rn))
    {
            discard;
    } else {
        
        // Burn around the hole.
        if ((dist1<Rn+BurnWidth) || (dist2<Rn+BurnWidth) || (dist3<Rn+BurnWidth)) {
                
                vec2 in_r = vec2(Rn, position.xy + position.yz);
                float value = random(in_r);
                
                // Primary burn color.
                if (fract(value)>0.5) {
                        gl_FragColor = BurnColor1;
                        }
                
                else {
                    // Tertiary burn color.
                    if ((fract(value)<0.5) && (fract(value)>=0.1)) {
                            gl_FragColor = BurnColor2;
                            }
                    
                    // Secondary burn color.
                    else {
                        gl_FragColor = BurnColor3;
                        }
                    }
                
                
                    
                }
        
        // The rest of the object.
        else {
            if ((fract(position.z)<fract(position.x)+width) && (fract(position.z)>fract(position.x)-width)) {
           vec3 color = gl_Color.xyz*LightIntensity;
           vec3 newcolor = mix(color, color1, 0.5);
           gl_FragColor = vec4(newcolor,1.0);
           } else {
               vec3 color = gl_Color.xyz*LightIntensity;
               vec3 newcolor = mix(color, color2, 0.5);
               gl_FragColor = vec4(newcolor,1.0);
               }
            //vec3 color = gl_Color.xyz*LightIntensity;
            //gl_FragColor = vec4(color,1.0);
            }
    }
       
   
}
'''




spawnvshader = \
'''
// Vertex shader for brick and mandelbrot shaders
// Derived from Orange Book Chapter 6
#version 120

//  Light intensity and model position required by fragment shader
varying float LightIntensity;
varying vec3  ModelPos;
varying vec3  vPos;

uniform float Zcenter;
uniform float Xcenter;
uniform float Ycenter;

//  Phong lighting intensity only
float phong()
{
   //  P is the vertex coordinate on body
   vec3 P = vec3(gl_ModelViewMatrix * gl_Vertex);
   //  N is the object normal at P
   vec3 N = normalize(gl_NormalMatrix * gl_Normal);
   //  Light Position for light 0
   vec3 LightPos = vec3(gl_LightSource[0].position);
   //  L is the light vector
   vec3 L = normalize(LightPos - P);
   //  R is the reflected light vector R = 2(L.N)N - L
   vec3 R = reflect(-L, N);
   //  V is the view vector (eye at the origin)
   vec3 V = normalize(-P);

   //  Diffuse light intensity is cosine of light and normal vectors
   float Id = max(dot(L,N) , 0.0);
   //  Shininess intensity is cosine of light and reflection vectors to a power
   float Is = (Id>0.0) ? pow(max(dot(R,V) , 0.0) , gl_FrontMaterial.shininess) : 0.0;

   //  Vertex color
   vec3 color = gl_FrontLightProduct[0].ambient.rgb
           + Id*gl_FrontLightProduct[0].diffuse.rgb
           + Is*gl_FrontLightProduct[0].specular.rgb;

   //  Vertex intensity
   return length(color);
}

void main()
{
   //  Scalar light intensity (for fragment shader)
   LightIntensity = phong();

   //  Save model coordinates (for fragment shader)
   ModelPos = gl_Vertex.xyz - vec3(Xcenter,Ycenter,Zcenter);

   //  Return fixed transform coordinates for this vertex
   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
   
   vPos = vec3(gl_ProjectionMatrix * gl_Vertex);
   //vPos = vec3(gl_Vertex * gl_ProjectionMatrix);
   //vPos = vec3(vec3(gl_ModelViewMatrix * gl_Vertex)+gl_Vertex.xyz);
   
   //vPos = vec3(gl_Position[2] + Ycenter);
   
   gl_FrontColor = gl_Color;
}
'''



spawnfshader = \
'''
#version 120


const vec4 SpawnColor = vec4(1.0,1.0,1.0,1.0);
const float BorderWidth = 0.1;

//  Model coordinates and light from vertex shader
varying float LightIntensity;
varying vec3  ModelPos;
varying vec3  vPos;

uniform float R;

const float width = 0.05;
uniform vec3 color1;
uniform vec3 color2;

void main()
{
   
   vec3 position = vPos;
   if (position.y>R) {
           discard;
   } else {
       
       if (position.y>R-BorderWidth){
               gl_FragColor = SpawnColor;
               
               }
       
       else {
           if ((fract(position.z)<fract(position.x)+width) && (fract(position.z)>fract(position.x)-width)) {
           vec3 color = gl_Color.xyz*LightIntensity;
           vec3 newcolor = mix(color, color1, 0.5);
           gl_FragColor = vec4(newcolor,1.0);
           } else {
               vec3 color = gl_Color.xyz*LightIntensity;
               vec3 newcolor = mix(color, color2, 0.5);
               gl_FragColor = vec4(newcolor,1.0);
               }
           //vec3 color = gl_Color.xyz*LightIntensity;
           //gl_FragColor = vec4(color,1.0);
           }
       }
}
'''




basevshader = \
'''
// Vertex shader for brick and mandelbrot shaders
// Derived from Orange Book Chapter 6
#version 120

//  Light intensity and model position required by fragment shader
varying float LightIntensity;
varying vec3  vPos;

uniform float Zcenter;
uniform float Xcenter;
uniform float Ycenter;

//  Phong lighting intensity only
float phong()
{
   //  P is the vertex coordinate on body
   vec3 P = vec3(gl_ModelViewMatrix * gl_Vertex);
   //  N is the object normal at P
   vec3 N = normalize(gl_NormalMatrix * gl_Normal);
   //  Light Position for light 0
   vec3 LightPos = vec3(gl_LightSource[0].position);
   //  L is the light vector
   vec3 L = normalize(LightPos - P);
   //  R is the reflected light vector R = 2(L.N)N - L
   vec3 R = reflect(-L, N);
   //  V is the view vector (eye at the origin)
   vec3 V = normalize(-P);

   //  Diffuse light intensity is cosine of light and normal vectors
   float Id = max(dot(L,N) , 0.0);
   //  Shininess intensity is cosine of light and reflection vectors to a power
   float Is = (Id>0.0) ? pow(max(dot(R,V) , 0.0) , gl_FrontMaterial.shininess) : 0.0;

   //  Vertex color
   vec3 color = gl_FrontLightProduct[0].ambient.rgb
           + Id*gl_FrontLightProduct[0].diffuse.rgb
           + Is*gl_FrontLightProduct[0].specular.rgb;

   //  Vertex intensity
   return length(color);
}

void main()
{
     
   //  Scalar light intensity (for fragment shader)
   LightIntensity = phong();

   //  Return fixed transform coordinates for this vertex
   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
   
   vPos = vec3(gl_ProjectionMatrix * gl_Vertex);
   
   gl_FrontColor = gl_Color;
}
'''



basefshader = \
'''
#version 120

//  Model coordinates and light from vertex shader
varying float LightIntensity;
varying vec3  vPos;

uniform float R;

const float width = 0.05;
uniform vec3 color1;
uniform vec3 color2;



void main()
{
     vec3 position = vPos;
 
     if ((fract(position.z)<fract(position.x)+width) && (fract(position.z)>fract(position.x)-width)) {
           vec3 color = gl_Color.xyz*LightIntensity;
           vec3 newcolor = mix(color, color1, 0.5);
           gl_FragColor = vec4(newcolor,1.0);
   } else {
       vec3 color = gl_Color.xyz*LightIntensity;
       vec3 newcolor = mix(color, color2, 0.5);
       gl_FragColor = vec4(newcolor,1.0);
       }
    //vec3 color = gl_Color.xyz*LightIntensity;
    //gl_FragColor = vec4(color,1.0);
}

'''








skinfshader = \
'''
#version 120

const float width = 0.05;

//  Model coordinates and light from vertex shader
varying float LightIntensity;
varying vec3  ModelPos;
varying vec3  vPos;


uniform vec3 color1;
uniform vec3 color2;
uniform float S;

void main()
{
   
   vec3 position = vPos;
   
   // females = dotted.
   if (S==1){
          
           
           float dist1 = distance(position,pos1);
           
           // Inside of dot color.
           
           X = fract(position.x)
           Z = fract(position.z)
           
           
           if (fract(position.z)==fract(position.x)+width) {
           vec3 color = gl_Color.xyz*LightIntensity;
           vec3 newcolor = mix(color, color1, 0.5);
           gl_FragColor = vec4(newcolor,1.0);
          
           
          // Outside of dot color
            } else {
               vec3 color = gl_Color.xyz*LightIntensity;
               vec3 newcolor = mix(color, color2, 0.5);
               gl_FragColor = vec4(newcolor,1.0);
               }
           
           
           }
   
   // Males = striped.
   else {
       // Inner stripe color.
   if ((fract(position.z)<fract(position.x)+width) && (fract(position.z)>fract(position.x)-width)) {
           vec3 color = gl_Color.xyz*LightIntensity;
           vec3 newcolor = mix(color, color1, 0.5);
           gl_FragColor = vec4(newcolor,1.0);
    
    // Outer stripe color.
   } else {
       vec3 color = gl_Color.xyz*LightIntensity;
       vec3 newcolor = mix(color, color2, 0.5);
       gl_FragColor = vec4(newcolor,1.0);
       }
}
}
'''








shader_strings = {'burnv':burnvshader,
                  'burnf':burnfshader,
                  'spawnv':spawnvshader,
                  'spawnf':spawnfshader,
                  'basev':basevshader,
                  'basef':basefshader}



