import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch

time   = np.array([0, 2, 4, 6, 8, 10])
energy = np.array([0, 1.5, 3.5, 6.0, 9.0, 13.0])

print("=" * 58)
print("  POWER TABLE  (Central Difference, h = 2 hrs)")
print("=" * 58)
print(f"  {'Time (hr)':<12} {'Energy (kWh)':<16} {'Power (kW)'}")
print("-" * 58)

h = 2
powers = {}
for i in range(len(time)):
    if i == 0 or i == len(time) - 1:
        print(f"  {time[i]:<12} {energy[i]:<16} N/A (boundary)")
    else:
        p = (energy[i + 1] - energy[i - 1]) / (2 * h)
        powers[time[i]] = p
        print(f"  {time[i]:<12} {energy[i]:<16} {p:.4f}")
print("=" * 58)

trap_energy = np.trapezoid(energy, time)
actual_energy = energy[-1]

print(f"\n  Trapezoidal integral (area under E-t curve) : {trap_energy:.4f} kWh·hr")
print(f"  Recorded final energy at t=10 hr            : {actual_energy:.1f} kWh")
print(f"  Note: Integral ≠ final reading — it is the")
print(f"         cumulative area under the E(t) curve.")
print("=" * 58 + "\n")

frames = 120
t_smooth = np.linspace(0, 10, frames)
e_smooth = np.interp(t_smooth, time, energy)
p_smooth = np.gradient(e_smooth, t_smooth)

plt.style.use('dark_background')
BG       = '#0A0A0F'
GRID_CLR = '#1A1A2E'
ENERGY_C = '#FFD700'
POWER_C  = '#FF007F'
PEAK_C   = '#FF4500'
TXT      = '#E8E8FF'
ACCENT   = '#00FFFF'

fig = plt.figure(figsize=(14, 8), facecolor=BG)
fig.canvas.manager.set_window_title('Infographic: Electricity Consumption & Power Analysis')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4,
                        left=0.06, right=0.97, top=0.87, bottom=0.10)

ax_meter = fig.add_subplot(gs[:, 0])
ax_E     = fig.add_subplot(gs[0, 1:])
ax_P     = fig.add_subplot(gs[1, 1:])

for ax in [ax_meter, ax_E, ax_P]:
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2A2A3A')

ax_meter.set_xlim(-1.2, 1.2)
ax_meter.set_ylim(-1.5, 1.4)
ax_meter.set_aspect('equal')
ax_meter.set_xticks([])
ax_meter.set_yticks([])
ax_meter.set_title("SMART METER", color=ACCENT, fontsize=11,
                   fontweight='bold', fontfamily='monospace', pad=8)

theta_bg = np.linspace(np.pi, 0, 200)
ax_meter.plot(np.cos(theta_bg), np.sin(theta_bg), color='#222233', lw=18, solid_capstyle='round')

zones = [
    (np.pi,     np.pi * 2/3, '#00CC44'),
    (np.pi*2/3, np.pi * 1/3, ENERGY_C),
    (np.pi/3,   0,           PEAK_C),
]
for t_start, t_end, col in zones:
    th = np.linspace(t_start, t_end, 60)
    ax_meter.plot(np.cos(th), np.sin(th), color=col, lw=18,
                  alpha=0.35, solid_capstyle='round')

ax_meter.text(-0.95, 0.12, "LOW",  color='#00CC44', fontsize=7, fontfamily='monospace', ha='center')
ax_meter.text( 0.0,  1.05, "MED",  color=ENERGY_C,  fontsize=7, fontfamily='monospace', ha='center')
ax_meter.text( 0.95, 0.12, "PEAK", color=PEAK_C,     fontsize=7, fontfamily='monospace', ha='center')

needle_line, = ax_meter.plot([], [], color=TXT, lw=2, zorder=10)
needle_base  = ax_meter.add_patch(plt.Circle((0, 0), 0.06, color='#AAAACC', zorder=11))

hud_t  = ax_meter.text(0, -0.45, "TIME: 0.0 hr",   color=TXT,       fontsize=9,  fontfamily='monospace', ha='center')
hud_e  = ax_meter.text(0, -0.65, "ENERGY: 0.00 kWh", color=ENERGY_C, fontsize=11, fontfamily='monospace',
                        ha='center', fontweight='bold')
hud_p  = ax_meter.text(0, -0.85, "POWER: 0.00 kW",  color=POWER_C,  fontsize=10, fontfamily='monospace',
                        ha='center', fontweight='bold')

for angle_deg in range(0, 181, 18):
    angle_rad = np.radians(180 - angle_deg)
    x0, y0 = 0.80 * np.cos(angle_rad), 0.80 * np.sin(angle_rad)
    x1, y1 = 0.92 * np.cos(angle_rad), 0.92 * np.sin(angle_rad)
    ax_meter.plot([x0, x1], [y0, y1], color='#444455', lw=1)

ax_E.fill_between(t_smooth, e_smooth, alpha=0.15, color=ENERGY_C)
ax_E.plot(t_smooth, e_smooth, color=ENERGY_C, lw=2, alpha=0.4)
ax_E.scatter(time, energy, color=ENERGY_C, s=50, zorder=5, edgecolors=BG, linewidths=1)
dot_E, = ax_E.plot([], [], 'o', color=TXT, ms=7, zorder=6)
ax_E.set_ylabel("Energy (kWh)", color='#888899', fontsize=8)
ax_E.set_title("ENERGY CONSUMPTION vs TIME", color=ENERGY_C, fontsize=9,
               fontweight='bold', fontfamily='monospace')
ax_E.tick_params(colors='#555566', labelsize=7)
ax_E.grid(True, color='#1A1A2E', lw=0.5)

ax_P.fill_between(t_smooth, p_smooth, alpha=0.15, color=POWER_C)
ax_P.plot(t_smooth, p_smooth, color=POWER_C, lw=2, alpha=0.4)
t_inner = [t for t in time if t in powers]
ax_P.scatter(t_inner, [powers[t] for t in t_inner],
             color=POWER_C, s=50, zorder=5, edgecolors=BG, linewidths=1)
dot_P, = ax_P.plot([], [], 'o', color=TXT, ms=7, zorder=6)
ax_P.axhline(0, color='#333344', lw=0.5, ls='--')
ax_P.set_xlabel("Time (hours)", color='#888899', fontsize=8)
ax_P.set_ylabel("Power (kW)", color='#888899', fontsize=8)
ax_P.set_title("INSTANTANEOUS POWER vs TIME", color=POWER_C, fontsize=9,
               fontweight='bold', fontfamily='monospace')
ax_P.tick_params(colors='#555566', labelsize=7)
ax_P.grid(True, color='#1A1A2E', lw=0.5)

peak_t = t_smooth[np.argmax(p_smooth)]
peak_p = p_smooth.max()
ax_P.annotate(f"Peak: {peak_p:.2f} kW",
              xy=(peak_t, peak_p), xytext=(peak_t - 1.8, peak_p * 0.85),
              color=PEAK_C, fontsize=7, fontfamily='monospace',
              arrowprops=dict(arrowstyle='->', color=PEAK_C, lw=0.8))

fig.suptitle("HOUSEHOLD ELECTRICITY CONSUMPTION & POWER ANALYSIS",
             color=TXT, fontsize=13, fontweight='bold', fontfamily='monospace', y=0.94)

def update(frame):
    ct = t_smooth[frame]
    ce = e_smooth[frame]
    cp = p_smooth[frame]

    p_max = p_smooth.max()
    angle = np.pi * (1 - np.clip(cp / p_max, 0, 1))
    nx, ny = 0.75 * np.cos(angle), 0.75 * np.sin(angle)
    needle_line.set_data([0, nx], [0, ny])

    hud_t.set_text(f"TIME: {ct:.1f} hr")
    hud_e.set_text(f"ENERGY: {ce:.2f} kWh")
    hud_p.set_text(f"POWER: {cp:.2f} kW")

    frac = np.clip(cp / p_max, 0, 1)
    r = int(0 + 255 * frac)
    g = int(255 * (1 - frac))
    b = int(127 * (1 - frac))
    needle_line.set_color(f'#{r:02X}{g:02X}{b:02X}')

    dot_E.set_data([ct], [ce])
    dot_P.set_data([ct], [cp])

    return needle_line, hud_t, hud_e, hud_p, dot_E, dot_P

ani = FuncAnimation(fig, update, frames=frames, interval=40, repeat=False)
plt.show()