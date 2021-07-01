import OpenGL.GL as _gl
import numpy as np




def activateShader(shaderprog,
                   A, D, P, 
                   R=None, pos=None,
                   colors=None):
    _gl.glUseProgram(shaderprog)
    
    # Set uniform variables.
    s_id = _gl.glGetUniformLocation(shaderprog,"Xcenter")
    if (s_id>=0): _gl.glUniform1f(s_id,0.5)
    
    s_id = _gl.glGetUniformLocation(shaderprog,"Ycenter")
    if (s_id>=0): _gl.glUniform1f(s_id,0.5)
    
    s_id = _gl.glGetUniformLocation(shaderprog,"Zcenter")
    if (s_id>=0): _gl.glUniform1f(s_id,0.5)
    
    if R is not None: 
        s_id = _gl.glGetUniformLocation(shaderprog,"R")
        if (s_id>=0): _gl.glUniform1f(s_id,R)
    
    if pos is not None:
        for i,p in enumerate(pos):
            s_id = _gl.glGetUniformLocation(shaderprog,"pos"+str(i+1))
            if (s_id>=0): _gl.glUniform3f(s_id,*p)
    
    
    if colors is not None:
        s_id = _gl.glGetUniformLocation(shaderprog,"color1")
        if (s_id>=0): _gl.glUniform3f(s_id,*colors[0])
        
        s_id = _gl.glGetUniformLocation(shaderprog,"color2")
        if (s_id>=0): _gl.glUniform3f(s_id,*colors[1])
    
    else:
        s_id = _gl.glGetUniformLocation(shaderprog,"color1")
        if (s_id>=0): _gl.glUniform3f(s_id,1,1,1)
        
        s_id = _gl.glGetUniformLocation(shaderprog,"color2")
        if (s_id>=0): _gl.glUniform3f(s_id,1,1,1)
    
    # Steal the modelview and projection matrixes from OpenGL
    ViewMatrix, ModelViewMatrix, ProjectionMatrix, NormalMatrix = \
    np.zeros(16),np.zeros(16),np.zeros(16),np.zeros(9)
    _gl.glGetFloatv(_gl.GL_PROJECTION_MATRIX,ProjectionMatrix)
    _gl.glGetFloatv(_gl.GL_MODELVIEW_MATRIX,ViewMatrix)
    _gl.glGetFloatv(_gl.GL_MODELVIEW_MATRIX,ModelViewMatrix)
    
    
    NormalMatrix[0] = ModelViewMatrix[0];   NormalMatrix[3] = ModelViewMatrix[4];   NormalMatrix[6] = ModelViewMatrix[8];
    NormalMatrix[1] = ModelViewMatrix[1];   NormalMatrix[4] = ModelViewMatrix[5];   NormalMatrix[7] = ModelViewMatrix[9];
    NormalMatrix[2] = ModelViewMatrix[2];   NormalMatrix[5] = ModelViewMatrix[6];   NormalMatrix[8] = ModelViewMatrix[10];
    
    
    # Set matrices.
    s_id = _gl.glGetUniformLocation(shaderprog,"ModelViewMatrix")
    if (s_id>=0): _gl.glUniformMatrix4fv(s_id,1,0,ModelViewMatrix)
        
    s_id = _gl.glGetUniformLocation(shaderprog,"ViewMatrix")
    if (s_id>=0): _gl.glUniformMatrix4fv(s_id,1,0,ViewMatrix)
        
    s_id = _gl.glGetUniformLocation(shaderprog,"ProjectionMatrix")
    if (s_id>=0): _gl.glUniformMatrix4fv(s_id,1,0,ProjectionMatrix)
        
    s_id = _gl.glGetUniformLocation(shaderprog,"NormalMatrix")
    if (s_id>=0): _gl.glUniformMatrix3fv(s_id,1,0,NormalMatrix)
        
    #  Set lighting parameters
    s_id = _gl.glGetUniformLocation(shaderprog,"Position")
    if (s_id>=0): _gl.glUniform4fv(s_id,1,P[:-1])
        
    s_id = _gl.glGetUniformLocation(shaderprog,"Ambient")
    if (s_id>=0): _gl.glUniform4fv(s_id,1,A[:-1])
        
    s_id = _gl.glGetUniformLocation(shaderprog,"Diffuse")
    if (s_id>=0): _gl.glUniform4fv(s_id,1,D[:-1])
    
    s_id = _gl.glGetUniformLocation(shaderprog,"Specular")
    if (s_id>=0): _gl.glUniform4fv(s_id,1,[0,0,0,1])
        
    #  Set material properties
    s_id = _gl.glGetUniformLocation(shaderprog,"Ks")
    if (s_id>=0): _gl.glUniform4fv(s_id,1,[0,0,0,1])
        
    s_id = _gl.glGetUniformLocation(shaderprog,"Ke")
    if (s_id>=0): _gl.glUniform4fv(s_id,1,[0,0,0,1])
        
    s_id = _gl.glGetUniformLocation(shaderprog,"Shinyness")
    if (s_id>=0): _gl.glUniform1f(s_id,16)


