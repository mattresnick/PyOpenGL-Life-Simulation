#version 120

varying float LightIntensity;
varying vec3  ModelPos;
varying vec3  vPos;

uniform float Zcenter;
uniform float Xcenter;
uniform float Ycenter;

//  Phong lighting intensity
float phong()
{
   
   vec3 P = vec3(gl_ModelViewMatrix * gl_Vertex);
   vec3 N = normalize(gl_NormalMatrix * gl_Normal);
   vec3 LightPos = vec3(gl_LightSource[0].position);
   vec3 L = normalize(LightPos - P);
   vec3 R = reflect(-L, N);
   vec3 V = normalize(-P);

   float Id = max(dot(L,N) , 0.0);
   float Is = (Id>0.0) ? pow(max(dot(R,V) , 0.0) , gl_FrontMaterial.shininess) : 0.0;

   vec3 color = gl_FrontLightProduct[0].ambient.rgb
           + Id*gl_FrontLightProduct[0].diffuse.rgb
           + Is*gl_FrontLightProduct[0].specular.rgb;

   return length(color);
}

void main()
{
   LightIntensity = phong();

   ModelPos = Zcenter*gl_Vertex.xyz - vec3(Xcenter,Ycenter,Zcenter);

   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
   
   vPos = vec3(gl_ProjectionMatrix * gl_Vertex);
   
   gl_FrontColor = gl_Color;
}