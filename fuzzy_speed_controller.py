"""
Fuzzy Logic Speed Controller for an Autonomous Car
--------------------------------------------------
Mamdani fuzzy inference system (scikit-fuzzy) that recommends a car speed from
road curvature, the posted speed limit and the distance to the nearest pedestrian.

Run:  python fuzzy_speed_controller.py
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define input variables
road_curvature = ctrl.Antecedent(np.arange(0, 91, 1), 'road_curvature')             # 0 to 90 degrees
speed_limit = ctrl.Antecedent(np.arange(60, 121, 1), 'speed_limit')                 # 60 to 120 km/h
pedestrian_distance = ctrl.Antecedent(np.arange(0, 101, 1), 'pedestrian_distance')  # 0 to 100 meters

# Define output variable
car_speed = ctrl.Consequent(np.arange(0, 121, 1), 'car_speed')                      # 0 to 120 km/h

# Road Curvature
road_curvature['straight'] = fuzz.trapmf(road_curvature.universe, [0, 0, 15, 30])
road_curvature['slight_curve'] = fuzz.trimf(road_curvature.universe, [20, 45, 70])
road_curvature['sharp_curve'] = fuzz.trapmf(road_curvature.universe, [60, 75, 90, 90])

# Speed Limit
speed_limit['low'] = fuzz.trapmf(speed_limit.universe, [60, 60, 70, 80])
speed_limit['medium'] = fuzz.trimf(speed_limit.universe, [70, 90, 110])
speed_limit['high'] = fuzz.trapmf(speed_limit.universe, [100, 110, 120, 120])

# Pedestrian Distance
pedestrian_distance['near'] = fuzz.trapmf(pedestrian_distance.universe, [0, 0, 15, 30])
pedestrian_distance['moderate'] = fuzz.trimf(pedestrian_distance.universe, [20, 50, 80])
pedestrian_distance['far'] = fuzz.trapmf(pedestrian_distance.universe, [70, 85, 100, 100])

# Car Speed (Output)
car_speed['slow'] = fuzz.trapmf(car_speed.universe, [0, 0, 30, 50])
car_speed['moderate'] = fuzz.trimf(car_speed.universe, [40, 65, 90])
car_speed['fast'] = fuzz.trapmf(car_speed.universe, [80, 100, 120, 120])

rules = [
    #straight road
    ctrl.Rule(road_curvature['straight'] & speed_limit['low'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['low'] & pedestrian_distance['moderate'], car_speed['moderate']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['low'] & pedestrian_distance['far'], car_speed['moderate']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['medium'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['medium'] & pedestrian_distance['moderate'], car_speed['moderate']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['medium'] & pedestrian_distance['far'], car_speed['fast']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['high'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['high'] & pedestrian_distance['moderate'], car_speed['moderate']),
    ctrl.Rule(road_curvature['straight'] & speed_limit['high'] & pedestrian_distance['far'], car_speed['fast']),

    #slight curve road
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['low'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['low'] & pedestrian_distance['moderate'], car_speed['slow']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['low'] & pedestrian_distance['far'], car_speed['moderate']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['medium'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['medium'] & pedestrian_distance['moderate'], car_speed['moderate']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['medium'] & pedestrian_distance['far'], car_speed['fast']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['high'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['high'] & pedestrian_distance['moderate'], car_speed['moderate']),
    ctrl.Rule(road_curvature['slight_curve'] & speed_limit['high'] & pedestrian_distance['far'], car_speed['fast']),

    #sharp curve road
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['low'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['low'] & pedestrian_distance['moderate'], car_speed['slow']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['low'] & pedestrian_distance['far'], car_speed['moderate']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['medium'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['medium'] & pedestrian_distance['moderate'], car_speed['slow']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['medium'] & pedestrian_distance['far'], car_speed['moderate']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['high'] & pedestrian_distance['near'], car_speed['slow']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['high'] & pedestrian_distance['moderate'], car_speed['slow']),
    ctrl.Rule(road_curvature['sharp_curve'] & speed_limit['high'] & pedestrian_distance['far'], car_speed['moderate']),
]

speed_ctrl = ctrl.ControlSystem(rules)
speed_sim = ctrl.ControlSystemSimulation(speed_ctrl)

# Example input values
speed_sim.input['road_curvature'] = 20        # straightness
speed_sim.input['speed_limit'] = 110          # km/h
speed_sim.input['pedestrian_distance'] =100   # meters

# Compute result
speed_sim.compute()

# Output result
try:
    result = speed_sim.output['car_speed']
    print(f"Recommended car speed: {result:.2f} km/h")
    car_speed.view(sim=speed_sim)
except Exception as e:
    print("Error during simulation:", e)

# Black line: final crisp output (103.11 km/h for this example)
# Shaded region: aggregated output of all fired rules (larger area = stronger support)

# Plot membership functions
road_curvature.view()
speed_limit.view()
pedestrian_distance.view()
car_speed.view()
plt.show()
