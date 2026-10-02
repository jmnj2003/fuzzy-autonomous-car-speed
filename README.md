# Fuzzy Logic Speed Controller for an Autonomous Car

A **Mamdani fuzzy logic controller** that chooses a safe driving speed for an autonomous car from three uncertain inputs: **road curvature**, the **posted speed limit** and the **distance to the nearest pedestrian**. It is built with `scikit-fuzzy` and uses 27 IF-THEN rules with centroid defuzzification.

> Group project for **Computational Intelligence**, Bachelor in Artificial Intelligence, Universiti Teknologi Malaysia.
>
> ▶️ **Demo video:** https://youtu.be/E-kaYVgac0Q

<p align="center">
  <img src="assets/control_surface.png" alt="3D control surface: recommended speed vs road curvature and pedestrian distance at a 110 km/h limit" width="620">
</p>

---

## Why fuzzy logic?

Sensor readings in a car are noisy and conditions change all the time. A road isn't simply "straight" or "curved", and a pedestrian isn't simply "near" or "far". Fuzzy logic handles these degrees of truth and uses rules a person can read, such as *"IF the road is a sharp curve AND a pedestrian is near THEN drive slow"*. This makes the controller's decisions easy to explain.

## System design

| Variable | Type | Range | Fuzzy sets |
|---|---|---|---|
| Road curvature | Input | 0–90° | straight · slight curve · sharp curve |
| Speed limit | Input | 60–120 km/h | low · medium · high |
| Pedestrian distance | Input | 0–100 m | near · moderate · far |
| **Car speed** | **Output** | 0–120 km/h | slow · moderate · fast |

<p align="center"><img src="assets/membership_functions.png" alt="Membership functions for the three inputs and the output" width="820"></p>

| Set | Shape | Parameters |
|---|---|---|
| Curvature: straight / slight / sharp | trap / tri / trap | [0,0,15,30] · [20,45,70] · [60,75,90,90] |
| Limit: low / medium / high | trap / tri / trap | [60,60,70,80] · [70,90,110] · [100,110,120,120] |
| Pedestrian: near / moderate / far | trap / tri / trap | [0,0,15,30] · [20,50,80] · [70,85,100,100] |
| Speed: slow / moderate / fast | trap / tri / trap | [0,0,30,50] · [40,65,90] · [80,100,120,120] |

Trapezoids are used for ranges where a whole band of values fully belongs to the set. Triangles are used for sets with a single ideal point.

### Rule base (3 × 3 × 3 = 27 rules, combined with AND)

| Curvature → | Straight | | | Slight curve | | | Sharp curve | | |
|---|---|---|---|---|---|---|---|---|---|
| **Pedestrian →** | near | moderate | far | near | moderate | far | near | moderate | far |
| Limit **low** | slow | moderate | moderate | slow | slow | moderate | slow | slow | moderate |
| Limit **medium** | slow | moderate | fast | slow | moderate | fast | slow | slow | moderate |
| Limit **high** | slow | moderate | fast | slow | moderate | fast | slow | slow | moderate |

The main patterns in the rules:

- **A near pedestrian always means slow.**
- **A sharp curve never allows fast.**
- **Fast is only allowed on straight or gently curving roads with a clear path.**

## Example

| Input | Value |
|---|---|
| Road curvature | 20° (partly *straight*, partly *slight curve*) |
| Speed limit | 110 km/h (between *medium* and *high*) |
| Pedestrian distance | 100 m (fully *far*) |

Every rule that fires points to **fast**. Centroid defuzzification gives:

**Recommended speed: 103.11 km/h**

<p align="center"><img src="assets/example_output.png" alt="Aggregated output membership with centroid at 103.11 km/h" width="460"></p>

### More scenarios (computed with the same controller)

| Curvature | Limit | Pedestrian | → Speed |
|---|---|---|---|
| 0° | 120 km/h | 100 m | 104.4 km/h |
| 45° | 90 km/h | 50 m | 65.0 km/h |
| 80° | 110 km/h | 100 m | 65.0 km/h |
| 50° | 100 km/h | 25 m | 36.7 km/h |
| 0° | 120 km/h | 5 m | 20.4 km/h |

## Limitations found in testing

Running the controller across its whole input range shows three things to fix before it could be trusted on a road:

1. **It never stops.** With centroid defuzzification the output can't go below about **20 km/h**. Even with a pedestrian at **0 m**, it still recommends 20.4 km/h. A real system needs a hard emergency-braking override outside the fuzzy controller.
2. **It can exceed the speed limit.** On a straight, clear road with a **60 km/h** limit, the "low limit + far pedestrian → moderate" rules give **65 km/h**. The output should be capped at the posted limit, or the "moderate" set should be scaled to the limit.
3. **Limited input range.** Speed limits below 60 km/h, such as school zones, fall outside the model.

## Future work

- An emergency-stop override and a speed-limit cap on the output
- More inputs: weather and road surface, traffic density, vehicle ahead
- Adaptive tuning of the membership functions, for example with a genetic algorithm or ANFIS
- More detailed rules for low-speed urban zones

## Getting started

```bash
git clone https://github.com/jmnj2003/fuzzy-autonomous-car-speed.git
cd fuzzy-autonomous-car-speed
pip install -r requirements.txt
python fuzzy_speed_controller.py
```

The script prints the recommended speed and shows the membership function plots. To try your own scenario, change the three `speed_sim.input[...]` values.

## Project structure

```
├── fuzzy_speed_controller.py   # variables, membership functions, 27 rules, simulation, plots
├── requirements.txt
└── assets/                     # figures used in this README
```

## Team (Group 1)

Bong Xin Ting · **Jessie Moh Ngiik Jun** · Lavinia Mary · Wafa Wan

## Tech stack

Python · scikit-fuzzy · NumPy · Matplotlib
