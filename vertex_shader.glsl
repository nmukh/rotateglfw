#version 410 core

layout(location = 0) in vec3 aVert;
layout(location = 1) in vec2 aTexCoord;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform float uTheta;

out vec2 vTexCoord;

void main() {
    // Rotation matrix for the Y-axis
    mat4 rot = mat4(
          vec4(cos(uTheta),  0.0, -sin(uTheta), 0.0),
          vec4(0.0,         -1.0,  0.0,         0.0),
          vec4(sin(uTheta),  0.0,  cos(uTheta), 0.0),
          vec4(0.0,          0.0,  0.0,         1.0)
    );
    gl_Position = uPMatrix * uMVMatrix * rot * vec4(aVert, 1.0);

    // Pass the texture coordinates to the fragment shader
    vTexCoord = aTexCoord;
}
