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
}