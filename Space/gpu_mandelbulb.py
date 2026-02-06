from moderngl_window.context.base import WindowConfig
import moderngl_window as mglw



VERT_SRC = """
#version 330

in vec2 in_position;
out vec2 uv;

void main() {
    uv = in_position;
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""


FRAG_SRC = """
#version 330

out vec4 fragColor;
in vec2 uv;

uniform float iTime;
uniform vec2 iResolution;


// ---------- Mandelbulb distance estimator ----------
float mandelbulb(vec3 p) {
    vec3 z = p;
    float dr = 1.0;
    float r = 0.0;

    const int ITER = 8;
    const float POWER = 8.0;

    for (int i = 0; i < ITER; i++) {
        r = length(z);
        if (r > 2.0) break;

        float theta = acos(z.z/r);
        float phi = atan(z.y, z.x);
        dr = pow(r, POWER-1.0)*POWER*dr + 1.0;

        float zr = pow(r, POWER);
        theta *= POWER;
        phi *= POWER;

        z = zr * vec3(
            sin(theta)*cos(phi),
            sin(phi)*sin(theta),
            cos(theta)
        );

        z += p;
    }

    return 0.5 * log(r) * r / dr;
}


// ---------- Ray march ----------
float raymarch(vec3 ro, vec3 rd) {
    float t = 0.0;

    for (int i=0; i<100; i++) {
        vec3 pos = ro + rd * t;
        float d = mandelbulb(pos);
        if (d < 0.001) return t;
        t += d;
        if (t > 50.0) break;
    }

    return -1.0;
}


// ---------- Normal ----------
vec3 getNormal(vec3 p) {
    float e = 0.001;
    return normalize(vec3(
        mandelbulb(p+vec3(e,0,0)) - mandelbulb(p-vec3(e,0,0)),
        mandelbulb(p+vec3(0,e,0)) - mandelbulb(p-vec3(0,e,0)),
        mandelbulb(p+vec3(0,0,e)) - mandelbulb(p-vec3(0,0,e))
    ));
}


// ---------- Camera ----------
vec3 getRay(vec2 uv) {
    vec3 ro = vec3(0, 0, -4.0);

    float ang = iTime * 0.3;
    ro.xz = mat2(cos(ang), -sin(ang), sin(ang), cos(ang)) * ro.xz;

    vec3 look = vec3(0);
    vec3 f = normalize(look - ro);
    vec3 r = normalize(cross(vec3(0,1,0), f));
    vec3 u = cross(f, r);

    return normalize(f + uv.x*r + uv.y*u);
}


void main() {

    vec2 p = uv;
    p.x *= iResolution.x / iResolution.y;

    vec3 ro = vec3(0,0,-4);
    vec3 rd = getRay(p);

    float t = raymarch(ro, rd);

    if (t < 0.0) {
        fragColor = vec4(0,0,0,1);
        return;
    }

    vec3 pos = ro + rd * t;
    vec3 n = getNormal(pos);

    vec3 light = normalize(vec3(1,1,-1));
    float diff = max(dot(n, light), 0.0);

    vec3 col = vec3(0.2,0.5,1.0) * diff;

    fragColor = vec4(col, 1.0);
}
"""


# ---------- Window App ----------

class MandelApp(WindowConfig):

    gl_version = (3, 3)
    title = "GPU Mandelbulb Ray Marching"
    window_size = (900, 700)
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader=VERT_SRC,
            fragment_shader=FRAG_SRC,
        )

        self.quad = mglw.geometry.quad_fs() # type: ignore

    def on_render(self, time, frame_time): # Nome atualizado
        self.ctx.clear()
        
        # Atribuição direta (testar se o erro do Pylance some)
        self.prog["iTime"] = time 
        self.prog["iResolution"] = self.window_size

        self.quad.render(self.prog)


# ---------- Run ----------

if __name__ == "__main__":
    mglw.run_window_config(MandelApp)