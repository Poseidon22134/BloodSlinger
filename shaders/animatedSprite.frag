#version 460 core

uniform sampler2D sprite;
uniform vec2 dimensions;

uniform float frame;

in vec2 UV;
out vec4 color;

void main() {
    vec2 xy = vec2(mod(frame, dimensions.x), floor(frame / dimensions.x));
    color = texture(sprite, UV / dimensions + xy * 1.0 / dimensions);
    if (color.a == 0) {discard;}
}