#version 410 core

in vec2 vTexCoord;
out vec4 fragColor;

uniform sampler2D tex2D;
uniform float uTheta;          // Rotation angle
uniform float uTilingFactor;   // Number of tiles (n)

// Rotation matrices for different planes
mat4 rotationXY(float angle) {
    return mat4(
        cos(angle), -sin(angle), 0.0, 0.0,
        sin(angle), cos(angle),  0.0, 0.0,
        0.0,        0.0,        1.0, 0.0,
        0.0,        0.0,        0.0, 1.0
    );
}

mat4 rotationYZ(float angle) {
    return mat4(
        1.0, 0.0,        0.0,        0.0,
        0.0, cos(angle), -sin(angle), 0.0,
        0.0, sin(angle), cos(angle),  0.0,
        0.0, 0.0,        0.0,        1.0
    );
}

mat4 rotationXZ(float angle) {
    return mat4(
        cos(angle),  0.0, sin(angle), 0.0,
        0.0,         1.0, 0.0,        0.0,
        -sin(angle), 0.0, cos(angle), 0.0,
        0.0,         0.0, 0.0,        1.0
    );
}

void main() {
    // Scale texture coordinates by tiling factor for the entire surface
    vec2 tileCoord = vTexCoord * uTilingFactor;

    // Get the integer part of tileCoord to determine the current tile position
    vec2 tileIndex = floor(tileCoord);

    // Use the tileIndex to determine which rotation to apply
    mat4 rotationMatrix;
    if (mod(tileIndex.x + tileIndex.y, 3.0) == 0.0) {
        rotationMatrix = rotationXY(uTheta);  // Rotate in xy-plane
    }
    else if (mod(tileIndex.x + tileIndex.y, 3.0) == 1.0) {
        rotationMatrix = rotationYZ(uTheta);  // Rotate in yz-plane
    }
    else {
        rotationMatrix = rotationXZ(uTheta);  // Rotate in xz-plane
    }

    // Calculate the local texture coordinates within each tile
    vec2 localCoord = fract(tileCoord);  // Fractional part for the local position within each tile

    // Apply rotation to the local tile coordinates
    vec4 rotatedCoord = rotationMatrix * vec4(localCoord - vec2(0.5, 0.5), 0.0, 1.0);
    vec2 finalCoord = rotatedCoord.xy + vec2(0.5, 0.5);  // Translate back to the original position

    // Sample the texture using the modified texture coordinates
    vec4 texColor = texture(tex2D, finalCoord);

    // Output the final color
    fragColor = texColor;
}
