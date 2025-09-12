shader_type spatial;

uniform float amplitude = 0.1;
uniform float frequency = 1.0;
uniform float speed = 1.0;
uniform vec4 custom_color = vec4(0, 0.15, 0, 1.0);

void vertex() {
    float wave = sin(VERTEX.x * frequency + TIME * speed) * amplitude;
    VERTEX.x += wave * 0.5;
}

void fragment() {
    ALBEDO = custom_color.rgb;
}