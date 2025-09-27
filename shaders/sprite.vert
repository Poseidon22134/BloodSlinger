#version 460 core

layout(location = 0) in vec2 vertexPosition;
layout(location = 1) in vec2 vertexUV;
// att textureIndex

uniform vec2 position; // default at 0 fine
uniform vec2 scale = vec2(1.0); // sets default to 1 rather than 0
uniform bool flipped; // default false.

out vec2 UV;

void main() {
    UV = vec2(flipped ? 1.0 - vertexUV.x : vertexUV.x, vertexUV.y);
    gl_Position = vec4((vertexPosition + position * 2.0) * scale, 0.0, 1.0);
}
