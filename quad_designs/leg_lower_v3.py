import cadquery as cq
from math import cos, sin, tan ,pi, radians, sqrt

import numpy as np

### ------------PARAMETERS OF LOWER LEG-------------

HOLE_TOLERANCE = 0.25  # Tolerance for hole dimensions (in radius) due to 3D printing

## Motor rotor coupler params (Based on Actual Motor)
rotor_disc_radius = 15.0  # Radius of the motor rotor disc (30 mm diameter)
rotor_disc_holes_pcd = 11.0  # Distance from rotor center to hole centers (PCD) (22 mm diameter)
rotor_disc_holes_radius = 1.25 + HOLE_TOLERANCE  # Radius of each mounting hole (2.5 mm diameter)
rotor_disc_holes_num = 8  # Number of mounting holes
rotor_disc_axle_hole_radius = 5 + HOLE_TOLERANCE  # Radius of center hole for motor axle (10 mm diameter)

## Parameters of leg_part_1
rotor_coupler_thickness = 5.0  # Thickness of the coupler disc and extension attached to rotor disc
L1 = 90.0 # Length of leg_part_1: first part of leg (attached to motor rotor)
motor_coupler_gap_half = 52/2
WIDTH = 2*(motor_coupler_gap_half+rotor_coupler_thickness)

# sketch parameters
offset = 0
angle_deg = 6
bottom_offset = 7





L1= 80
L2 = 130
theta=-radians(20)
delta1 = pi/2-radians(10)
delta2 = pi/2-radians(5)
delta3 = pi/2+theta-radians(10)
delta4 = pi/2+theta-radians(10)
r2=15/2
r3=40/2
rubber_bumper_radius=15
p1 = (0,0)
p2 = (L1, 0)
p3 = (L1+L2*cos(theta), L2*sin(theta))
c1a  = (0, rotor_disc_radius)
c1b = (0, -rotor_disc_radius)
c2a  = (p2[0]+r2*cos(delta1), p2[1]+r2*sin(delta1))
c2b = (p2[0]-r2*cos(delta2), p2[1]-r2*sin(delta2))
c3a  = (p3[0]+r3*cos(delta3), p3[1]+r3*sin(delta3))
c3b = (p3[0]-r3*cos(delta4), p3[1]-r3*sin(delta4))
c3c = (p3[0]+rubber_bumper_radius*cos(theta), p3[1]+rubber_bumper_radius*sin(theta))
t1 = (1, 0)
t2_d1 = (-cos(pi/2+delta1), -sin(pi/2+delta1))
t2_d2 = (-cos(pi/2+delta2), -sin(pi/2+delta2))
t3_d1 = (-cos(pi/2+delta3), -sin(pi/2+delta3))
t3_d2 = (-cos(pi/2+delta4), -sin(pi/2+delta4))

# # Sketch of first part of leg (attached to motor rotor)
# sketch = cq.Sketch()
# sketch = sketch.arc(p1,rotor_disc_radius,90,180)
# sketch = sketch.arc(p2,r2,0,360)
# sketch = sketch.arc(p3,r3,0,360)
# sketch = sketch.segment(p2,c2a)
# sketch = sketch.segment(p2,c2b)
# sketch = sketch.segment(p3,c3a)
# sketch = sketch.segment(p3,c3b)
# sketch = sketch.spline([c1a, c2a, c3a], [t1,t2_d1,t3_d1], False)
# sketch = sketch.spline([c1b, c2b, c3b], [t1,t2_d2,t3_d2], False)


sketch = (cq.Sketch()
          .arc(p1,rotor_disc_radius,90,90)
          .spline([c1a, c2a, c3a], [t1,t2_d1,t3_d1], False)
          .arc(c3a,c3c,c3b)
          .spline([(-rotor_disc_radius, 0),(0, -rotor_disc_radius-bottom_offset), c2b, c3b], [(0.0, -1.0),(1.0, 0), t2_d2,t3_d2], False)
)
sketch = sketch.arc((0.0, 0.0), rotor_disc_axle_hole_radius, 0.0, 360.0)
for i in range(rotor_disc_holes_num):
    angle = i * (360.0 / rotor_disc_holes_num)  # Degrees
    x_pos = rotor_disc_holes_pcd * cos(radians(angle))
    y_pos = rotor_disc_holes_pcd * sin(radians(angle))
    sketch = sketch.arc((-x_pos, -y_pos), rotor_disc_holes_radius, 0.0, 360.0)
sketch = sketch.assemble()

leg_solid = cq.Workplane("XY").add(sketch).extrude(WIDTH)
csc_l2 = 40
csc_l = L1-csc_l2

sketch_semicirlce = (
    cq.Sketch()
    # .arc((0,motor_coupler_gap_half), (motor_coupler_gap_half*1.5,0), (0,-motor_coupler_gap_half))
    .spline([(0,motor_coupler_gap_half), (40,0), (0,-motor_coupler_gap_half)],[(1,0),(0,-1),(-1,0)],False)
    .segment((-csc_l,motor_coupler_gap_half), (0,motor_coupler_gap_half))
    .segment((-csc_l,-motor_coupler_gap_half), (0,-motor_coupler_gap_half))
    .segment((-csc_l,-motor_coupler_gap_half), (-csc_l,motor_coupler_gap_half))
).assemble()
csc = cq.Workplane().placeSketch(sketch_semicirlce).extrude(rotor_disc_radius*2+bottom_offset).rotate((0,0,0),(1,0,0),90).translate((L1-rotor_disc_radius-csc_l2,rotor_disc_radius,motor_coupler_gap_half+rotor_coupler_thickness))

side_cut_L = 140
side_cut_l1 = 35
side_cut_w = (WIDTH-30)/2
sketch_side_cut = (
    cq.Sketch()
    .spline([(side_cut_l1,side_cut_w), (side_cut_L, 0)],[(1,0),(1,0)],False)
    .segment((0,0),(side_cut_L,0))
    .segment((0,0),(0,side_cut_w))
    .segment((0,side_cut_w),(side_cut_l1,side_cut_w))
).assemble()
side_cut_1 = cq.Workplane().placeSketch(sketch_side_cut).extrude(rotor_disc_radius*8).rotate((0,0,0),(1,0,0),-90).rotate((0,0,0),(0,1,0),180).translate((p3[0]+20,-rotor_disc_radius*5,0))
side_cut_2 = cq.Workplane().placeSketch(sketch_side_cut).extrude(rotor_disc_radius*8).rotate((0,0,0),(1,0,0),90).rotate((0,0,0),(0,1,0),180).translate((p3[0]+20,rotor_disc_radius*3,WIDTH))



leg = leg_solid.cut(csc).cut(side_cut_1).cut(side_cut_2)

# Extra rotor rotor disc extrusion for tight fit
rotor_disc_sketch = cq.Sketch().arc((0, 0), rotor_disc_radius, 0.0, 360.0).arc((0.0, 0.0), rotor_disc_axle_hole_radius, 0.0, 360.0)
for i in range(rotor_disc_holes_num):
    angle = i * (360.0 / rotor_disc_holes_num)  # Degrees
    x_pos = rotor_disc_holes_pcd * cos(radians(angle))
    y_pos = rotor_disc_holes_pcd * sin(radians(angle))
    rotor_disc_sketch = rotor_disc_sketch.arc((-x_pos, -y_pos), rotor_disc_holes_radius, 0.0, 360.0)
rotor_disc_sketch = rotor_disc_sketch.assemble()
rotor_disc1 = cq.Workplane("XY").placeSketch(rotor_disc_sketch).extrude(1).translate((0, 0, rotor_coupler_thickness))
rotor_disc2 = cq.Workplane("XY").placeSketch(rotor_disc_sketch).extrude(1).translate((0, 0, WIDTH-rotor_coupler_thickness-1))

lower_leg = leg.union(rotor_disc1).union(rotor_disc2)
lower_leg.export("../assets/quad_parts/lower_leg_v3.svg")
lower_leg.export("../assets/quad_parts/lower_leg_v3.step")
lower_leg.export("../assets/quad_parts/lower_leg_v3.stl")
print("Lower leg v3 saved successfully!")