import cadquery as cq
from math import cos, degrees, sin, tan ,pi, radians, sqrt

import numpy as np

class Transform2D:
    def __init__(self, origin=(0, 0), rotation_deg=0):
        self.set_origin_rotation(origin, rotation_deg)

    def set_origin_rotation(self, origin, rotation_deg):
        self.origin = np.asarray(origin, dtype=float)
        theta = np.deg2rad(rotation_deg)
        self.R = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])

    def transform(self, p1, p2):
        point = np.asarray([p1, p2], dtype=float)
        rotated = self.R @ point
        translated = rotated + self.origin
        return tuple(translated)

tf = Transform2D()

### ------------PARAMETERS OF UPPER LEG-------------
## We will use (0,0) at rotor center (so its easy to later fit things properly)

HOLE_TOLERANCE = 0.25  # Tolerance for hole dimensions (in radius) due to 3D printing

## Motor coupler params (Based on Actual Motor)
rotor_disc_radius = 15.0
inner_rect_w = 29
inner_rect_l = 42.5 # This is from rotor center (not total l)
motor_inner_thickness = 34.5 # 0.5 mm extra
motor_outer_thickness = 41 # exact
coupler_plate_thickness = 3.5 # exact minimum 
outer_rect_w = 40.2
hole_plate_w = (outer_rect_w-inner_rect_w)/2
outer_rect_l = inner_rect_l + hole_plate_w
hole_radius = 1.5 + HOLE_TOLERANCE
h1_w = 22/2
h2_w = 34.6/2
h3_w = h2_w
h1_l = 45.3
h2_l = 40.0
h3_l = 18.0

## Leg Params
L1= 170
L1_extend = 210
L2 = 40
theta=radians(-60)
delta0 = pi/2-radians(-5)
delta1 = pi/2-radians(20)
delta2 = pi/2-radians(20)
delta3 = pi/2+theta-radians(0)
delta4 = pi/2+theta-radians(0)
r1=(outer_rect_w+10)/2
r2=40/2
r3=(outer_rect_w+10)/2
start_cir_back_l = r1
p1 = (rotor_disc_radius+outer_rect_l/2-5,4)
p2 = (L1, 0)
p3 = (L1_extend+L2*cos(theta), L2*sin(theta))

c1a  = (p1[0]+r1*cos(delta0), p1[1]+r1*sin(delta0))
c1b = (p1[0]-r1*cos(delta0), p1[1]-r1*sin(delta0))
c1c = (p1[0]+start_cir_back_l*cos(pi/2+delta0), p1[1]+start_cir_back_l*sin(pi/2+delta0))
c2a  = (p2[0]+r2*cos(delta1), p2[1]+r2*sin(delta1))
c2b = (p2[0]-r2*cos(delta2), p2[1]-r2*sin(delta2))
c3a  = (p3[0]+r3*cos(delta3), p3[1]+r3*sin(delta3))
c3b = (p3[0]-r3*cos(delta4), p3[1]-r3*sin(delta4))
c3c = (p3[0]+r3*cos(theta), p3[1]+r3*sin(theta))
t1 = (-cos(pi/2+delta0), -sin(pi/2+delta0))
t2_d1 = (-cos(pi/2+delta1), -sin(pi/2+delta1))
t2_d2 = (-cos(pi/2+delta2), -sin(pi/2+delta2))
t3_d1 = (-cos(pi/2+delta3), -sin(pi/2+delta3))
t3_d2 = (-cos(pi/2+delta4), -sin(pi/2+delta4))


tf.set_origin_rotation(p3, 140)

leg_sketch = (
    cq.Sketch()
    .arc(c1a,c1c,c1b)
    .arc(c3a,c3c,c3b)
    .spline([c1a, c2a, c3a], [t1,t2_d1,t3_d1], False)
    .spline([c1b, c2b, c3b], [t1,t2_d2,t3_d2], False)
    .arc((h1_l, h1_w), hole_radius, 0, 360)
    .arc((h1_l, -h1_w), hole_radius, 0, 360)
    .arc((h2_l, h2_w), hole_radius, 0, 360)
    .arc((h2_l, -h2_w), hole_radius, 0, 360)
    .arc((h3_l, h3_w), hole_radius, 0, 360)
    .arc(tf.transform(h1_l, h1_w), hole_radius, 0, 360)
    .arc(tf.transform(h1_l, -h1_w), hole_radius, 0, 360)
    .arc(tf.transform(h2_l, h2_w), hole_radius, 0, 360)
    .arc(tf.transform(h2_l, -h2_w), hole_radius, 0, 360)
    .arc(tf.transform(h3_l, h3_w), hole_radius, 0, 360)
    .arc(tf.transform(h3_l, -h3_w), hole_radius, 0, 360)
).assemble()

leg1 = cq.Workplane("XY").placeSketch(leg_sketch).extrude(coupler_plate_thickness)
leg2 = cq.Workplane("XY").placeSketch(leg_sketch).extrude(coupler_plate_thickness).translate((0, 0, motor_outer_thickness - coupler_plate_thickness))

upper_leg = leg1.union(leg2)

upper_leg.export("../assets/quad_parts/upper_leg_v3.svg")
upper_leg.export("../assets/quad_parts/upper_leg_v3.step")
upper_leg.export("../assets/quad_parts/upper_leg_v3.stl")
print("Upper leg v3 saved successfully!")