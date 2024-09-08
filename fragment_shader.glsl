#version 410 core

in vec2 vTexCoord;

uniform sampler2D tex2D;
uniform bool showCircle;

out vec4 fragColor;

void main() {
  if (showCircle) {
    if (distance(vTexCoord, vec2(0.5, 0.5)) > 0.5) {
      discard;
    } else {
      fragColor = texture(tex2D, vTexCoord);
    }
  } else {
    fragColor = texture(tex2D, vTexCoord);
  }
}