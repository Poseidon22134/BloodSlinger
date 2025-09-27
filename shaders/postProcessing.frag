#version 460 core

uniform sampler2D layer1;

in vec2 UV;
out vec4 color;

uniform float vignette_amount = 0.8;
uniform float vignette_intensity = 0.2;

float vignette(vec2 uv) {
	uv *= 1.0 - uv.xy;
	float vignette = uv.x * uv.y * 15.0;
	return pow(vignette, vignette_intensity * vignette_amount);
}

void main() {
  // if (abs(UV.x - UV.y) < 0.01 || abs(UV.x - (1.0 - UV.y)) < 0.01) {color = vec4(1.0, 0.0, 0.0, 1.0); return;}
  color = texture(layer1, UV);
  if (vignette_amount > 0.0) {
	color *= vignette(UV);
	}
  if (color.a == 0) {discard;}
}
