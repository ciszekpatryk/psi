import numpy as np
import matplotlib.pyplot as plt

# Funkcja przynależności Gaussa
def gauss(x, c, sigma):
    return np.exp(-0.5 * ((x - c) / sigma) ** 2)

# Dziedzina wyjścia (prędkość wentylatora 0-100%)
Y_DOMAIN = np.linspace(0, 100, 100)

# Zbiory rozmyte dla wyjścia (Prędkość wentylatora)
fan_low = gauss(Y_DOMAIN, 15, 15)
fan_med = gauss(Y_DOMAIN, 50, 15)
fan_high = gauss(Y_DOMAIN, 85, 15)

def fuzzy_controller(cpu_temp, gpu_load, room_temp):
    # Wagi cech
    w_cpu = 1.0   # najwyższa
    w_gpu = 0.6   # średnia
    w_room = 0.3  # najmniejsza

    # BLOK ROZMYWANIA z uwzględnieniem wag
    cpu_cold = gauss(cpu_temp, 35, 12) * w_cpu
    cpu_warm = gauss(cpu_temp, 65, 12) * w_cpu
    cpu_hot  = gauss(cpu_temp, 95, 12) * w_cpu

    gpu_low  = gauss(gpu_load, 20, 20) * w_gpu
    gpu_high = gauss(gpu_load, 80, 20) * w_gpu

    room_cool = gauss(room_temp, 18, 5) * w_room
    room_hot  = gauss(room_temp, 32, 5) * w_room

    # BLOK WNIOSKOWANIA
    # min() = AND, max() = OR
    
    # Wentylator wolno
    r1 = min(cpu_cold, gpu_low)
    
    # Wentylator średnio
    r2 = max(cpu_warm, min(gpu_high, room_cool))
    
    # Wentylator szybko
    r3 = max(cpu_hot, min(gpu_high, room_hot))

    # Przycinanie zbiorów wyjściowych wartościami aktywacji reguł
    out_low  = np.fmin(r1, fan_low)
    out_med  = np.fmin(r2, fan_med)
    out_high = np.fmin(r3, fan_high)

    # Agregacja wszystkich reguł w jedną figurę
    aggregated = np.fmax(out_low, np.fmax(out_med, out_high))

    # BLOK WYOSTRZANIA
    if np.sum(aggregated) == 0:
        return 0.0
    return np.sum(Y_DOMAIN * aggregated) / np.sum(aggregated)

# GENEROWANIE WYKRESÓW 3D
cpu_range = np.linspace(30, 100, 30)
gpu_range = np.linspace(0, 100, 30)
X, Y = np.meshgrid(cpu_range, gpu_range)

# Dwa wykresy dla ustalonej trzeciej cechy ("czwarty wymiar": temp. pokoju)
fig = plt.figure(figsize=(12, 5))

for idx, r_temp in enumerate([18, 32]):
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = fuzzy_controller(X[i, j], Y[i, j], r_temp)

    ax = fig.add_subplot(1, 2, idx + 1, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_title(f'Sterowanie wentylatorem (Temp. pokoju: {r_temp}°C)')
    ax.set_xlabel('Temp. CPU (°C)')
    ax.set_ylabel('Obciążenie GPU (%)')
    ax.set_zlabel('Wentylator (%)')
    ax.set_zlim(0, 100)

plt.tight_layout()
plt.show()