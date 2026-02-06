import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Configurações Iniciais (Constantes e Massas)
G = 6.67430e-11  # Constante Gravitacional
M_TERRA = 5.972e24 
M_LUA = 7.348e22
DISTANCIA_TL = 3.844e8 # Distância média em metros
V_LUA = 1022           # Velocidade orbital da Lua em m/s

# 2. Condições de Estado (Posição e Velocidade inicial)
# Colocamos a Terra no centro (0,0) e a Lua na distância R
pos_terra = np.array([0.0, 0.0])
pos_lua = np.array([DISTANCIA_TL, 0.0])

vel_terra = np.array([0.0, 0.0])
vel_lua = np.array([0.0, V_LUA])

# Listas para guardar o rastro da órbita
trajetoria_lua = []

def calcular_gravidade(p1, p2, m1, m2):
    vetor_r = p2 - p1
    distancia = np.linalg.norm(vetor_r)
    forca_magnitude = G * m1 * m2 / distancia**2
    direcao = vetor_r / distancia
    return forca_magnitude * direcao

# 3. Função de Atualização (O "Motor" da Simulação)
def atualizar(frame):
    global pos_lua, vel_lua
    
    # Calcula a força que a Terra exerce na Lua
    forca = calcular_gravidade(pos_lua, pos_terra, M_LUA, M_TERRA)
    
    # F = m * a  =>  a = F / m
    aceleracao = forca / M_LUA
    
    # Atualiza velocidade e posição (Integração de Euler simplificada)
    dt = 3600 * 2  # Salto de 2 horas por frame para vermos o movimento
    vel_lua += aceleracao * dt
    pos_lua += vel_lua * dt
    
    trajetoria_lua.append(pos_lua.copy())
    pontos_rastro = np.array(trajetoria_lua)
    
    # Atualiza o gráfico
    lua_plot.set_data([pos_lua[0]], [pos_lua[1]])
    rastro_plot.set_data(pontos_rastro[:,0], pontos_rastro[:,1])
    return lua_plot, rastro_plot

# 4. Configuração do Gráfico
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('black')
limit = DISTANCIA_TL * 1.5
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# Desenha a Terra e a Lua
ax.plot(0, 0, 'bo', markersize=10, label='Terra') # Terra fixa para simplificar
lua_plot, = ax.plot([], [], 'yo', markersize=5, label='Lua')
rastro_plot, = ax.plot([], [], 'w-', alpha=0.3, linewidth=1)

plt.legend()
plt.title("Simulação Gravitacional: Sistema Terra-Lua")

ani = FuncAnimation(fig, atualizar, frames=200, interval=20, blit=True)
plt.show()
