import numpy as np #
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------------------
# Mandelbulb simplificado
# -------------------------

def mandelbulb_points(power=8, iterations=8, bound=2.0, grid=40): # https://en.wikipedia.org/wiki/Mandelbulb
    pts = []
#    grid = 40
    xs = np.linspace(-1.5, 1.5, grid)
    ys = np.linspace(-1.5, 1.5, grid)
    zs = np.linspace(-1.5, 1.5, grid)
#    xs = np.linspace(-0.5, 0.5, grid)
#    ys = np.linspace(-0.5, 0.5, grid)
#    zs = np.linspace(-0.5, 0.5, grid)
    for x in xs:
        for y in ys:
            for z in zs:
                c = np.array([x, y, z])
                v = c.copy()

                for _ in range(iterations):
                    r = np.linalg.norm(v)
                    if r > bound:
                        break

                    if r == 0:
                        break

                    theta = np.arccos(v[2] / r)
                    phi = np.arctan2(v[1], v[0])

                    rn = r ** power
                    thetan = theta * power
                    phin = phi * power

                    v = rn * np.array([
                        np.sin(thetan) * np.cos(phin),
                        np.sin(thetan) * np.sin(phin),
                        np.cos(thetan)
                    ])

                    v += c

                else:
                    pts.append(c)

    return np.array(pts)


print("Calculando pontos 3D...")
points = mandelbulb_points(grid=32)

# -------------------------
# Plot 3D
# -------------------------

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(
    points[:,0],
    points[:,1],
    points[:,2],
    s=2 # type: ignore
)

ax.set_title("Mandelbulb 3D — Python")
ax.set_xlim(-1.5,1.5)
ax.set_ylim(-1.5,1.5)
ax.set_zlim(-1.5,1.5) # type: ignore

# -------------------------
# Animação de rotação
# -------------------------

def update(frame):
    ax.view_init(elev=30, azim=frame) # type: ignore
    return sc,

ani = FuncAnimation(
    fig,
    update,
    frames=np.arange(0, 360, 2),
    interval=50
)

plt.show()
