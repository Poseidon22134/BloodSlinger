#version 460 core

uniform sampler2D sprite;

in vec2 UV;
out vec4 color;

void main() {
    color = texture(sprite, UV);
    if (color.a == 0) {discard;}
}