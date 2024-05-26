import numpy as np
import matplotlib.pyplot as plt

np.random.seed()

# Parameters
r = 0.03
b = 0.08
sigma = 0.2
u = 0.5
X0 = 1
T = 1
N = 100
dt = T / N

# Time array
t = np.linspace(0, T, N+1)

# Initialize the array to store the process values
X = np.zeros(N+1)
K,Y,L=X.copy(),X.copy(),X.copy()
X[0] = X0
K[0],Y[0],L[0]= X0,X0,X0
# Simulate the process
for i in range(1, N+1):
    Z = np.random.normal(0, 1)
    X[i] = X[i-1] + r * X[i-1] * dt + u * (b - r) * X[i-1] * dt + u * sigma * X[i-1] * np.sqrt(dt) * Z
    K[i] = K[i-1] + r * K[i-1] * dt +  u * sigma * K[i-1] * np.sqrt(dt) * Z
    Y[i] = Y[i-1] + r * Y[i-1] * dt + u * (b - r) * Y[i-1] * dt
    L[i]=  u * sigma * X[i-1] * np.sqrt(dt) * Z

# Plot the process
plt.plot(t, K, color='blue', label='Process $X_s$')
#plt.plot(t, Y, color='green', label='Process $Y_s$')
plt.plot(t, L, color='red', label='Process $L_s$')
plt.xlabel('Time $s$')
plt.ylabel('Wealth $X_s$')
plt.title('Simulation of the Controlled Wealth Process')
plt.legend()
plt.grid(True)
plt.show()
