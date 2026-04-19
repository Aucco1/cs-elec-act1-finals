import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch

time     = np.array([0, 1, 2, 3, 4, 5])
position = np.array([0, 5, 15, 30, 50, 75])

print("=" * 55)
print("  VELOCITY TABLE  (Central Difference, h = 1 s)")
print("=" * 55)
print(f"  {'Time (s)':<10} {'Position (m)':<16} {'Velocity (m/s)'}")
print("-" * 55)

h = 1
velocities = {}
for i in range(len(time)):
    if i == 0 or i == len(time) - 1:
        print(f"  {time[i]:<10} {position[i]:<16} N/A (boundary)")
    else:
        v = (position[i + 1] - position[i - 1]) / (2 * h)
        velocities[time[i]] = v
        print(f"  {time[i]:<10} {position[i]:<16} {v:.2f}")
print("=" * 55)

v_array = np.array([velocities[t] for t in sorted(velocities)])
t_inner = np.array([1, 2, 3, 4])

print("\n  ACCELERATION TABLE  (Central Difference on velocity)")
print("=" * 55)
print(f"  {'Time (s)':<10} {'Velocity (m/s)':<18} {'Acceleration (m/s²)'}")
print("-" * 55)
for i in range(len(t_inner)):
    if i == 0 or i == len(t_inner) - 1:
        print(f"  {t_inner[i]:<10} {v_array[i]:<18.2f} N/A (boundary)")
    else:
        a = (v_array[i + 1] - v_array[i - 1]) / (2 * h)
        print(f"  {t_inner[i]:<10} {v_array[i]:<18.2f} {a:.2f}")
print("=" * 55)

trap_dist = np.trapezoid(position, time)
actual_displacement = position[-1] - position[0]

print(f"\n  Trapezoidal integral (area under x-t curve) : {trap_dist:.2f} m·s")
print(f"  Actual displacement (x[5] - x[0])           : {actual_displacement:.2f} m")
print("=" * 55 + "\n")

frames = 120
t_smooth = np.linspace(time.min(), time.max(), frames)
x_smooth = np.interp(t_smooth, time, position)
v_smooth = np.gradient(x_smooth, t_smooth)
a_smooth = np.gradient(v_smooth, t_smooth)

plt.style.use('dark_background')
BG      = '#0D0D0D'
ROAD    = '#1A1A1A'
LANE    = '#F5C518'
CAR     = '#00E5FF'
VEL_CLR = '#FF6B35'
ACC_CLR = '#7BFF72'
TXT     = '#FFFFFF'

fig = plt.figure(figsize=(13, 8), facecolor=BG)
fig.canvas.manager.set_window_title('Infographic: Traffic Flow Analysis')
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35,
                        left=0.08, right=0.96, top=0.88, bottom=0.10)

ax_road = fig.add_subplot(gs[:, 0])
ax_xvt  = fig.add_subplot(gs[0, 1])
ax_vt   = fig.add_subplot(gs[1, 1])

for ax in [ax_road, ax_xvt, ax_vt]:
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')

ax_road.set_xlim(-1, 1)
ax_road.set_ylim(-0.5, 80)
ax_road.set_xticks([])
ax_road.set_yticks([])
ax_road.set_facecolor(ROAD)
ax_road.set_title("VEHICLE POSITION", color=CAR, fontsize=11,
                  fontweight='bold', fontfamily='monospace', pad=8)

ax_road.axvline(-0.8, color='#FFFFFF', lw=1.5, alpha=0.4)
ax_road.axvline( 0.8, color='#FFFFFF', lw=1.5, alpha=0.4)

for y in range(0, 80, 8):
    ax_road.plot([0, 0], [y, y + 4], color=LANE, lw=1, alpha=0.4)

for mark in [0, 15, 30, 50, 75]:
    ax_road.axhline(mark, color='#444444', lw=0.5, ls='--')
    ax_road.text(0.82, mark, f"{mark} m", color='#888888',
                 fontsize=7, va='center', fontfamily='monospace')

car_body = plt.Polygon([[-0.3, 0], [0.3, 0], [0.3, 2.5], [-0.3, 2.5]],
                        closed=True, color=CAR, zorder=5)
car_roof = plt.Polygon([[-0.15, 2.5], [0.15, 2.5], [0.15, 3.5], [-0.15, 3.5]],
                        closed=True, color=CAR, zorder=5)
ax_road.add_patch(car_body)
ax_road.add_patch(car_roof)

hud_t  = ax_road.text(-0.75, 78, "T: 0.0 s",   color=TXT,     fontsize=9,  fontfamily='monospace', va='top')
hud_x  = ax_road.text(-0.75, 76, "X: 0.0 m",   color=CAR,     fontsize=10, fontfamily='monospace', va='top', fontweight='bold')
hud_v  = ax_road.text(-0.75, 73, "V: -- m/s",  color=VEL_CLR, fontsize=9,  fontfamily='monospace', va='top', fontweight='bold')

ax_xvt.plot(t_smooth, x_smooth, color=CAR, lw=1.5, alpha=0.35)
ax_xvt.scatter(time, position, color=CAR, s=40, zorder=5)
dot_x, = ax_xvt.plot([], [], 'o', color=TXT, ms=6, zorder=6)
ax_xvt.set_xlabel("Time (s)", color='#888888', fontsize=8)
ax_xvt.set_ylabel("Position (m)", color='#888888', fontsize=8)
ax_xvt.set_title("POSITION vs TIME", color=CAR, fontsize=9,
                  fontweight='bold', fontfamily='monospace')
ax_xvt.tick_params(colors='#555555', labelsize=7)

ax_vt.plot(t_smooth, v_smooth, color=VEL_CLR, lw=1.5, alpha=0.35)
ax_vt.scatter(t_inner, v_array, color=VEL_CLR, s=40, zorder=5)
dot_v, = ax_vt.plot([], [], 'o', color=TXT, ms=6, zorder=6)
ax_vt.set_xlabel("Time (s)", color='#888888', fontsize=8)
ax_vt.set_ylabel("Velocity (m/s)", color='#888888', fontsize=8)
ax_vt.set_title("VELOCITY vs TIME", color=VEL_CLR, fontsize=9,
                  fontweight='bold', fontfamily='monospace')
ax_vt.tick_params(colors='#555555', labelsize=7)

fig.suptitle("TRAFFIC FLOW & VELOCITY ESTIMATION",
             color=TXT, fontsize=14, fontweight='bold', fontfamily='monospace', y=0.95)

def update(frame):
    cx = x_smooth[frame]
    ct = t_smooth[frame]
    cv = v_smooth[frame]

    car_body.set_xy([[-0.3, cx], [0.3, cx], [0.3, cx + 2.5], [-0.3, cx + 2.5]])
    car_roof.set_xy([[-0.15, cx + 2.5], [0.15, cx + 2.5],
                     [0.15, cx + 3.5], [-0.15, cx + 3.5]])

    hud_t.set_text(f"T: {ct:.1f} s")
    hud_x.set_text(f"X: {cx:.1f} m")
    hud_v.set_text(f"V: {cv:.1f} m/s")

    dot_x.set_data([ct], [cx])
    dot_v.set_data([ct], [cv])

    return car_body, car_roof, hud_t, hud_x, hud_v, dot_x, dot_v

ani = FuncAnimation(fig, update, frames=frames, interval=40, repeat=False)
plt.show()