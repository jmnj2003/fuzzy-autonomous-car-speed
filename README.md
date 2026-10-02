# Fuzzy Logic Speed Controller for an Autonomous Car

A **Mamdani fuzzy logic controller** that chooses a safe driving speed for an autonomous car from three uncertain inputs: **road curvature**, the **posted speed limit** and the **distance to the nearest pedestrian**. It is built with `scikit-fuzzy` and uses 27 IF-THEN rules with centroid defuzzification.
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

### More scenarios (computed with the same controller)

| Curvature | Limit | Pedestrian | → Speed |
|---|---|---|---|
| 0° | 120 km/h | 100 m | 104.4 km/h |
| 45° | 90 km/h | 50 m | 65.0 km/h |
| 80° | 110 km/h | 100 m | 65.0 km/h |
| 50° | 100 km/h | 25 m | 36.7 km/h |
| 0° | 120 km/h | 5 m | 20.4 km/h |


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
└──  requirements.txt
```
