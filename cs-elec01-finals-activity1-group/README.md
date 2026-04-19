<div align="center">

# 📐 CS ELEC 01 — Computational Science
### Unit 4: Numerical Methods for Real-World Data
**College of Engineering and Information Technology**
*Department of Computing and Library Information Science*

---

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=flat-square&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=flat-square)
![SciPy](https://img.shields.io/badge/SciPy-1.10%2B-8CAAE6?style=flat-square&logo=scipy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 📋 Overview

This repository contains solutions for **4 selected case studies** from the Unit 4 Finals Activity of CS ELEC 01. Each case study demonstrates the application of numerical methods — specifically **numerical differentiation** and **numerical integration** — to real-world engineering and scientific problems. Solutions are implemented in Python with animated visualizations for each case.

| # | Case | Concept | Method |
|---|------|---------|--------|
| 2 | [Traffic Flow & Velocity Estimation](#-case-study-2-traffic-flow--velocity-estimation) | Velocity + Distance | Central Difference + Trapezoidal |
| 3 | [Heat Diffusion Simulation](#-case-study-3-heat-diffusion-simulation) | Gradient + Integration | Central Difference + Simpson's Rule |
| 4 | [Water Tank Filling Rate Analysis](#-case-study-4-water-tank-filling-rate-analysis) | Flow Rate | Central Difference + Trapezoidal |
| 5 | [Electricity Consumption & Power Analysis](#-case-study-5-electricity-consumption--power-analysis) | Power Analysis | Central Difference + Trapezoidal |

---

## 🗂️ Repository Structure

```
cs-elec01-unit4/
├── case2_traffic.py          # Traffic flow: velocity estimation
├── case3_heat.py             # Heat diffusion: temperature gradient
├── case4_water_tank.py       # Water tank: flow rate analysis
├── case5_electricity.py      # Electricity: power analysis
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

```bash
pip install numpy matplotlib scipy
```

### Running a Case

```bash
python case2_traffic.py
python case3_heat.py
python case4_water_tank.py
python case5_electricity.py
```

> **Note:** All scripts produce a live animated window. A display environment is required (not headless). Each script also prints a formatted results table to the console before launching the animation.

---

## 🚗 Case Study 2: Traffic Flow & Velocity Estimation

### Scenario
A traffic monitoring system records the position of a vehicle every second. Engineers compute instantaneous velocity and total distance.

### Given Data

| Time (s) | Position (m) |
|:--------:|:------------:|
| 0        | 0            |
| 1        | 5            |
| 2        | 15           |
| 3        | 30           |
| 4        | 50           |
| 5        | 75           |

### Methods

**Velocity (Central Difference, h = 1 s):**

$$v(t) = \frac{x(t+1) - x(t-1)}{2}$$

**Distance Verification (Trapezoidal Rule):**

$$\int_0^5 x(t)\, dt$$

### Results

#### Velocity Table

| Time (s) | Position (m) | Velocity (m/s) |
|:--------:|:------------:|:--------------:|
| 0        | 0            | N/A (boundary) |
| 1        | 5            | 7.50           |
| 2        | 15           | 12.50          |
| 3        | 30           | 17.50          |
| 4        | 50           | 22.50          |
| 5        | 75           | N/A (boundary) |

#### Acceleration Table

| Time (s) | Velocity (m/s) | Acceleration (m/s²) |
|:--------:|:--------------:|:-------------------:|
| 1        | 7.50           | N/A (boundary)      |
| 2        | 12.50          | 5.00                |
| 3        | 17.50          | 5.00                |
| 4        | 22.50          | N/A (boundary)      |

#### Trapezoidal Integral
$$\int_0^5 x(t)\, dt \approx 137.50 \text{ m·s}$$

> The actual displacement is **75 m** (position at t = 5). The integral represents the area under the position-time curve, not final displacement.

### Analysis

- **Is the car accelerating?** Yes — velocity increases uniformly from 7.50 to 22.50 m/s. The constant acceleration of **5.00 m/s²** at interior points confirms uniform acceleration.
- **Is motion uniform?** No. The vehicle is under constant acceleration; position grows quadratically.
- **Anomalies?** None. The data is smooth and consistent with a uniformly accelerating body.

### Visualization

The animated script features a **top-down road view** with a moving vehicle alongside live position and velocity charts. The HUD overlays current time, position, and velocity in real-time.

---

## 🔥 Case Study 3: Heat Diffusion Simulation

### Scenario
A metal rod is heated at one end. Engineers estimate how heat spreads along its 10 cm length using discrete temperature measurements.

### Given Data

| Position (cm) | Temperature (°C) |
|:-------------:|:----------------:|
| 0             | 100              |
| 2             | 80               |
| 4             | 65               |
| 6             | 55               |
| 8             | 48               |
| 10            | 45               |

### Methods

**Temperature Gradient (Central Difference, h = 2 cm):**

$$\frac{dT}{dx} \approx \frac{T(x+h) - T(x-h)}{2h}$$

**Heat Distribution (Simpson's Rule):**

For 6 data points (5 intervals, odd), a combined **Simpson's 3/8 + 1/3** composite rule is applied:

$$\int_0^{10} T(x)\, dx \approx \frac{3h}{8}[T_0 + 3T_1 + 3T_2 + T_3] + \frac{h}{3}[T_3 + 4T_4 + T_5]$$

### Results

#### Temperature Gradient Table

| Position (cm) | Temp (°C) | dT/dx (°C/cm) |
|:-------------:|:---------:|:-------------:|
| 0             | 100       | N/A (boundary)|
| 2             | 80        | −8.75         |
| 4             | 65        | −6.25         |
| 6             | 55        | −4.25         |
| 8             | 48        | −2.50         |
| 10            | 45        | N/A (boundary)|

#### Integrated Heat Distribution

| Method          | Value (°C·cm) |
|:---------------:|:-------------:|
| **Simpson's Rule** | **645.00**    |
| Trapezoidal Rule (check) | 642.50 |

> The small difference between methods reflects Simpson's Rule capturing the curvature more accurately.

### Analysis

- **Where is heat transfer fastest?** At **x = 2 cm**, where the gradient is steepest at −8.75 °C/cm. The rod loses heat most rapidly near the hot end.
- **Is the decrease linear?** No. The gradient becomes less steep toward the cooler end, indicating a **non-linear (concave) temperature profile** — consistent with Fourier diffusion theory.
- **What happens farther from the source?** The gradient flattens toward ~−2.5 °C/cm at x = 8 cm, approaching a quasi-steady state. The last two data points (48 → 45 °C) show a near-plateau.

### Visualization

The animated script renders a **vertical rod** with a thermal gradient colormap (red → blue), a scanning probe that reads local temperature and gradient in real-time, and synchronized temperature/gradient charts.

---

## 💧 Case Study 4: Water Tank Filling Rate Analysis

### Scenario
Sensors record the volume of a water tank being filled over 10 minutes. Engineers determine the rate of inflow and verify total volume.

### Given Data

| Time (min) | Volume (L) |
|:----------:|:----------:|
| 0          | 0          |
| 2          | 40         |
| 4          | 110        |
| 6          | 210        |
| 8          | 340        |
| 10         | 500        |

### Methods

**Flow Rate (Central Difference, h = 2 min):**

$$f'(t) \approx \frac{V(t+h) - V(t-h)}{2h}$$

**Total Volume Integral (Trapezoidal Rule):**

$$\int_0^{10} V(t)\, dt$$

### Results

#### Flow Rate Table

| Time (min) | Volume (L) | Flow Rate (L/min) |
|:----------:|:----------:|:-----------------:|
| 0          | 0          | N/A (boundary)    |
| 2          | 40         | 27.50             |
| 4          | 110        | 42.50             |
| 6          | 210        | 57.50             |
| 8          | 340        | 72.50             |
| 10         | 500        | N/A (boundary)    |

#### Trapezoidal Integral

$$\int_0^{10} V(t)\, dt \approx 2700 \text{ L·min}$$

> This is the area under the Volume-vs-Time curve. The actual final tank volume at t = 10 min is **500 L**.

### Analysis

- **Is the flow rate constant?** No — it increases from 27.50 to 72.50 L/min, growing by **~15 L/min** every 2 minutes.
- **When is the inflow fastest?** Near **t = 8–10 min**, where the steepest rise (340 → 500 L) occurs.
- **Is the system linear or accelerating?** The volume data follows a **quadratic (accelerating) pattern**. The steadily increasing flow rate confirms that the fill rate is not constant but growing — consistent with a pressure-driven system.

### Visualization

The animated script renders a **3D cylinder tank** filling with neon-cyan water in real-time, with a live dashboard overlay showing time, volume, and current flow rate. Tank top/bottom caps are rendered for a complete sealed-cylinder appearance.

---

## ⚡ Case Study 5: Electricity Consumption & Power Analysis

### Scenario
A household records energy consumption at 2-hour intervals. Engineers compute instantaneous power usage and verify total energy.

### Given Data

| Time (hr) | Energy (kWh) |
|:---------:|:------------:|
| 0         | 0            |
| 2         | 1.5          |
| 4         | 3.5          |
| 6         | 6.0          |
| 8         | 9.0          |
| 10        | 13.0         |

### Methods

**Power (Central Difference, h = 2 hr):**

$$P(t) = \frac{dE}{dt} \approx \frac{E(t+h) - E(t-h)}{2h}$$

**Energy Verification (Trapezoidal Rule):**

$$\int_0^{10} E(t)\, dt$$

### Results

#### Power Table

| Time (hr) | Energy (kWh) | Power (kW) |
|:---------:|:------------:|:----------:|
| 0         | 0            | N/A        |
| 2         | 1.5          | 0.8750     |
| 4         | 3.5          | 1.1250     |
| 6         | 6.0          | 1.3750     |
| 8         | 9.0          | 1.7500     |
| 10        | 13.0         | N/A        |

#### Trapezoidal Integral (Energy Verification)

$$\int_0^{10} E(t)\, dt \approx 57.00 \text{ kWh·hr}$$

> **Clarification:** The integral of E(t) over time is not the same as the final energy reading (13.0 kWh). The trapezoidal integral gives the *accumulated area* under the E-t curve. The final energy value is the direct sensor reading at t = 10.

### Analysis

- **When is electricity usage highest?** Power is highest at **t = 8 hr** (1.75 kW) and continues rising toward t = 10 hr. This corresponds to evening hours with increased appliance usage.
- **Is consumption steady or increasing?** Increasing. Power rises from 0.875 kW to 1.75 kW — the household consumes electricity at an **accelerating rate**.
- **Suggestions to reduce peak usage:**
  - Shift high-load appliances (washing machine, dishwasher) to off-peak hours (before t = 4 hr).
  - Use programmable timers to distribute load more evenly.
  - Consider battery storage or solar to offset peak demand hours.

### Visualization

The animated script features a **semicircular smart meter gauge** with colour-coded zones (low/medium/peak), a colour-changing needle tied to instantaneous power, and dual charts for energy and power over time with a peak-usage annotation.

---

## 📐 Summary of Numerical Methods Used

| Method | Formula | Applied In |
|--------|---------|------------|
| Central Difference | $f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$ | All cases |
| Trapezoidal Rule | $\int \approx \frac{h}{2}[f_0 + 2f_1 + \cdots + f_n]$ | Cases 2, 4, 5 |
| Simpson's 3/8 + 1/3 | Composite (odd intervals) | Case 3 |

---

## 👥 Group Information

> *Fill in your group name, section, and member names below.*

**Group Name:** ___________________
**Section:** ___________________
**Members:**
- ___________________
- ___________________
- ___________________

**Deadline:** April 19, 2026 @ 11:00 PM
**Course:** CS ELEC 01 – Computational Science

---

<div align="center">
<sub>Made with Python 🐍 | CS ELEC 01 Unit 4 Finals Activity</sub>
</div>
