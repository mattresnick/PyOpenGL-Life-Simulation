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
            }
    }
       
   
}