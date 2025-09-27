#version 460 core

layout(location=0) uniform sampler2D tilemap;
uniform float tileSize;
uniform vec2 tilemapDimensions;

uniform vec2 screenResolution;

layout(location=1) uniform isampler2D tilemapLayout;
uniform ivec2 offset;

uniform vec2 mapScale = vec2(1.0);

in vec2 UV;
out vec4 color;

void main() {
    ivec2 texCoord = ivec2((gl_FragCoord.xy * mapScale - (screenResolution / 2) + offset) / tileSize + 1) - 1;

    int tileIndex = texelFetch(tilemapLayout, texCoord, 0).r;

    vec2 uv = UV + vec2(offset) / screenResolution / mapScale;
    vec2 tileLocalUV = vec2(mod((uv * screenResolution - screenResolution / 2) / tileSize, 1));

    if (tileIndex == 0 || tileIndex == -1) {
        discard;
    //     color = vec4(max(max(tileLocalUV.x, tileLocalUV.y), floor((tileLocalUV.x + tileLocalUV.y) * 0.5)));
    } else {
        vec2 tileUV = vec2(
            (float(tileIndex - 1) + tileLocalUV.x) / tilemapDimensions.x,
            (floor(float(tileIndex - 1) / tilemapDimensions.x) - tileLocalUV.y + 1) / tilemapDimensions.y
        );

        color = texture(tilemap, tileUV);
        if (color.a < 0.01) {
            discard;
        }
    }
}
