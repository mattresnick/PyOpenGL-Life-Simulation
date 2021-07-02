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
           }
       }
}