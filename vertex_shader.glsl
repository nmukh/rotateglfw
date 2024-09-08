#version 410 core

layout(location = 0) in vec3 aVert;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform float uTheta;

out vec2 vTexCoord;

void main() {
  mat4 rot = mat4(
        vec4(1.0,  0.0,          0.0,         0.0),
        vec4(0.0,  cos(uTheta),  sin(uTheta), 0.0),
        vec4(0.0, -sin(uTheta),  cos(uTheta), 0.0),
        vec4(0.0,  0.0,          0.0,         1.0)
  );
  gl_Position = uPMatrix * uMVMatrix * rot * vec4(aVert, 1.0);
  vTexCoord = aVert.xy + vec2(0.5, 0.5);
}
