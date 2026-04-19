import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

time = np.array([0, 2, 4, 6, 8, 10])
volume = np.array([0, 40, 110, 210, 340, 500])

print("=" * 45)
print("  FLOW RATE TABLE (Central Difference Method)")
print("=" * 45)
print(f"  {'Time (min)':<12} {'Volume (L)':<14} {'Flow Rate (L/min)'}")
print("-" * 45)
h = 2
for i in range(len(time)):
    if i == 0 or i == len(time) - 1:
        print(f"  {time[i]:<12} {volume[i]:<14} {'N/A (boundary)'}")
    else:
        rate = (volume[i + 1] - volume[i - 1]) / (2 * h)
        print(f"  {time[i]:<12} {volume[i]:<14} {rate:.2f}")
print("=" * 45)

trap_integral = np.trapezoid(volume, time)
print(f"\n  Trapezoidal Integral (area under V-t curve): {trap_integral:.2f} L·min")
print(f"  Final Volume at t=10 min: {volume[-1]} L")
print("=" * 45 + "\n")

frames = 100
t_smooth = np.linspace(time.min(), time.max(), frames)
v_smooth = np.interp(t_smooth, time, volume)
flow_rate_smooth = np.gradient(v_smooth, t_smooth)

plt.style.use('dark_background')
bg_color = '#121212'
water_color = '#00E5FF'
tank_edge_color = '#444444'
text_color = '#FFFFFF'

fig = plt.figure(figsize=(10, 8), facecolor=bg_color)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor(bg_color)
fig.canvas.manager.set_window_title('Infographic: Tank Filling Analysis')

radius = 5
theta = np.linspace(0, 2 * np.pi, 50)
theta_grid, _ = np.meshgrid(theta, np.array([0, 1]))

X = radius * np.cos(theta_grid)
Y = radius * np.sin(theta_grid)

theta_disk = np.linspace(0, 2 * np.pi, 50)
r_disk = np.linspace(0, radius, 10)
R_disk, T_disk = np.meshgrid(r_disk, theta_disk)
X_disk = R_disk * np.cos(T_disk)
Y_disk = R_disk * np.sin(T_disk)

def update(frame):
    ax.clear()

    current_v = v_smooth[frame]
    current_t = t_smooth[frame]
    current_rate = flow_rate_smooth[frame]

    ax.set_xlim([-8, 8])
    ax.set_ylim([-8, 8])
    ax.set_zlim([0, 550])
    ax.set_axis_off()

    ax.text2D(0.05, 0.95, "WATER TANK SENSOR LOG", transform=ax.transAxes,
              color=water_color, fontsize=16, fontweight='bold', fontfamily='sans-serif')
    ax.text2D(0.05, 0.90, f"TIME: {current_t:04.1f} MIN", transform=ax.transAxes,
              color=text_color, fontsize=14, fontfamily='monospace')
    ax.text2D(0.05, 0.85, f"VOL : {current_v:05.1f} L", transform=ax.transAxes,
              color=water_color, fontsize=20, fontweight='bold', fontfamily='monospace')
    ax.text2D(0.05, 0.80, f"RATE: {current_rate:04.1f} L/MIN", transform=ax.transAxes,
              color='#FF0055', fontsize=14, fontweight='bold', fontfamily='monospace')

    Z_tank = np.zeros_like(X)
    Z_tank[1, :] = 500
    ax.plot_wireframe(X, Y, Z_tank, color=tank_edge_color, alpha=0.3)

    ax.plot_surface(X_disk, Y_disk, np.zeros_like(X_disk),
                    color=tank_edge_color, alpha=0.2)
    ax.plot_surface(X_disk, Y_disk, np.full_like(X_disk, 500),
                    color=tank_edge_color, alpha=0.1)

    if current_v > 0:
        Z_water = np.zeros_like(X)
        Z_water[1, :] = current_v
        ax.plot_surface(X, Y, Z_water, color=water_color, alpha=0.9, rstride=1, cstride=1)

        ax.plot_surface(X_disk, Y_disk, np.full_like(X_disk, current_v),
                        color=water_color, alpha=0.95)
        ax.plot_surface(X_disk, Y_disk, np.zeros_like(X_disk),
                        color=water_color, alpha=0.95)

    return ax,

ani = FuncAnimation(fig, update, frames=frames, interval=40, repeat=False)
plt.show()