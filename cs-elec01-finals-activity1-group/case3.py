import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from scipy.interpolate import CubicSpline

position    = np.array([0, 2, 4, 6, 8, 10])
temperature = np.array([100, 80, 65, 55, 48, 45])

print("=" * 58)
print("  TEMPERATURE GRADIENT TABLE  (Central Difference, h = 2 cm)")
print("=" * 58)
print(f"  {'Pos (cm)':<12} {'Temp (°C)':<14} {'dT/dx (°C/cm)'}")
print("-" * 58)

h = 2
gradients = {}
for i in range(len(position)):
    if i == 0 or i == len(position) - 1:
        print(f"  {position[i]:<12} {temperature[i]:<14} N/A (boundary)")
    else:
        g = (temperature[i + 1] - temperature[i - 1]) / (2 * h)
        gradients[position[i]] = g
        print(f"  {position[i]:<12} {temperature[i]:<14} {g:.4f}")
print("=" * 58)

def simpsons_composite(y, h_step):
    n = len(y) - 1
    if n % 2 == 0:
        result = y[0] + y[-1]
        for i in range(1, n):
            result += (4 if i % 2 != 0 else 2) * y[i]
        return (h_step / 3) * result
    else:
        s38 = (3 * h_step / 8) * (y[0] + 3*y[1] + 3*y[2] + y[3])
        s13 = (h_step / 3) * (y[3] + 4*y[4] + y[5])
        return s38 + s13

heat_integral = simpsons_composite(temperature, h)
trap_check     = np.trapezoid(temperature, position)

print(f"\n  Simpson's Rule integral  ∫T(x)dx [0→10] : {heat_integral:.4f} °C·cm")
print(f"  Trapezoidal Rule check                   : {trap_check:.4f} °C·cm")
print("=" * 58 + "\n")

cs         = CubicSpline(position, temperature)
x_smooth   = np.linspace(0, 10, 300)
T_smooth   = cs(x_smooth)
dT_smooth = cs(x_smooth, 1)

plt.style.use('dark_background')
BG       = '#0D0D0D'
HOT_CLR  = '#FF4500'
COOL_CLR = '#00BFFF'
GRAD_CLR = '#FFD700'
TXT      = '#FFFFFF'

fig = plt.figure(figsize=(13, 8), facecolor=BG)
fig.canvas.manager.set_window_title('Infographic: Heat Diffusion Analysis')
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.50, wspace=0.38,
                        left=0.08, right=0.96, top=0.88, bottom=0.10)

ax_rod  = fig.add_subplot(gs[:, 0])
ax_T    = fig.add_subplot(gs[0, 1])
ax_dT   = fig.add_subplot(gs[1, 1])

for ax in [ax_rod, ax_T, ax_dT]:
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')

frames = 150
x_frames = np.linspace(0, 10, frames)

ax_rod.set_xlim(-0.5, 1.5)
ax_rod.set_ylim(-0.5, 11)
ax_rod.set_xticks([])
ax_rod.set_yticks([])
ax_rod.set_title("HEAT DIFFUSION ALONG ROD", color=HOT_CLR, fontsize=11,
                  fontweight='bold', fontfamily='monospace', pad=8)

ax_rod.fill_betweenx([0, 10], -0.15, 0.15, color='#222222', zorder=1)
ax_rod.plot([-0.15, -0.15], [0, 10], color='#444444', lw=1, zorder=2)
ax_rod.plot([ 0.15,  0.15], [0, 10], color='#444444', lw=1, zorder=2)

ax_rod.plot([0], [-0.25], marker='v', ms=12, color=HOT_CLR, zorder=10)
ax_rod.text(0.22, -0.25, "HEAT SOURCE", color=HOT_CLR, fontsize=8,
            fontfamily='monospace', va='center')

for p in position:
    ax_rod.axhline(p, color='#2A2A2A', lw=0.5, ls='--')
    ax_rod.text(0.22, p, f"{p} cm", color='#666666', fontsize=7,
                va='center', fontfamily='monospace')

probe_dot, = ax_rod.plot([], [], 'o', color=TXT, ms=8, zorder=10)
hud_x  = ax_rod.text(-0.45, 10.6, "POS : 0.0 cm",  color=TXT,     fontsize=9,  fontfamily='monospace')
hud_T  = ax_rod.text(-0.45, 10.3, "TEMP: --- °C",  color=HOT_CLR, fontsize=10, fontfamily='monospace', fontweight='bold')
hud_dT = ax_rod.text(-0.45, 10.0, "dT/dx: --- °C/cm", color=GRAD_CLR, fontsize=9, fontfamily='monospace')

ax_T.plot(x_smooth, T_smooth, color=HOT_CLR, lw=1.5, alpha=0.35)
ax_T.scatter(position, temperature, color=HOT_CLR, s=45, zorder=5)
dot_T, = ax_T.plot([], [], 'o', color=TXT, ms=6, zorder=6)
ax_T.set_xlabel("Position (cm)", color='#888888', fontsize=8)
ax_T.set_ylabel("Temperature (°C)", color='#888888', fontsize=8)
ax_T.set_title("TEMPERATURE vs POSITION", color=HOT_CLR, fontsize=9,
               fontweight='bold', fontfamily='monospace')
ax_T.tick_params(colors='#555555', labelsize=7)

ax_dT.plot(x_smooth, dT_smooth, color=GRAD_CLR, lw=1.5, alpha=0.35)
interior_pos = [p for p in position if p in gradients]
ax_dT.scatter(interior_pos, [gradients[p] for p in interior_pos],
              color=GRAD_CLR, s=45, zorder=5)
dot_dT, = ax_dT.plot([], [], 'o', color=TXT, ms=6, zorder=6)
ax_dT.axhline(0, color='#444444', lw=0.5, ls='--')
ax_dT.set_xlabel("Position (cm)", color='#888888', fontsize=8)
ax_dT.set_ylabel("dT/dx (°C/cm)", color='#888888', fontsize=8)
ax_dT.set_title("TEMPERATURE GRADIENT", color=GRAD_CLR, fontsize=9,
                fontweight='bold', fontfamily='monospace')
ax_dT.tick_params(colors='#555555', labelsize=7)

fig.suptitle("HEAT DIFFUSION IN A METAL ROD",
             color=TXT, fontsize=14, fontweight='bold', fontfamily='monospace', y=0.95)

def temp_to_color(T_val):
    frac = np.clip((T_val - 45) / (100 - 45), 0, 1)
    r = int(255 * frac + 0 * (1 - frac))
    g = int(69  * frac + 191 * (1 - frac))
    b = int(0   * frac + 255 * (1 - frac))
    return f'#{r:02X}{g:02X}{b:02X}'

bar_segments = 200
y_bar = np.linspace(0, 10, bar_segments)
T_bar = cs(y_bar)
for i in range(len(y_bar) - 1):
    ax_rod.fill_betweenx([y_bar[i], y_bar[i + 1]], -0.14, 0.14,
                          color=temp_to_color(T_bar[i]), alpha=0.9, zorder=3)

def update(frame):
    xp = x_frames[frame]
    Tp = float(cs(xp))
    dTp = float(cs(xp, 1))

    probe_dot.set_data([0], [xp])
    hud_x.set_text(f"POS : {xp:.1f} cm")
    hud_T.set_text(f"TEMP: {Tp:.1f} °C")
    hud_dT.set_text(f"dT/dx: {dTp:.2f} °C/cm")
    hud_T.set_color(temp_to_color(Tp))

    dot_T.set_data([xp], [Tp])
    dot_dT.set_data([xp], [dTp])

    return probe_dot, hud_x, hud_T, hud_dT, dot_T, dot_dT

ani = FuncAnimation(fig, update, frames=frames, interval=35, repeat=False)
plt.show()