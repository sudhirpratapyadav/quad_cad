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
rotor_coupler_thickness = 10.0  # Thickness of the coupler disc and extension attached to rotor disc
motor_coupler_gap_half = 52/2
motor_outer_thickness = 41.5 # 0.5 mm extra
WIDTH = 2*(motor_coupler_gap_half+rotor_coupler_thickness)


L=rotor_disc_radius+rotor_coupler_thickness+motor_coupler_gap_half

sketch = (cq.Sketch()
           .arc((0,0),rotor_disc_radius,90,180)
           .segment((0,rotor_disc_radius),(L,rotor_disc_radius))
           .segment((L,rotor_disc_radius),(L,-rotor_disc_radius))
           .segment((L,-rotor_disc_radius),(0,-rotor_disc_radius))
)
sketch = sketch.arc((0.0, 0.0), rotor_disc_axle_hole_radius, 0.0, 360.0)
for i in range(rotor_disc_holes_num):
    angle = i * (360.0 / rotor_disc_holes_num)  # Degrees
    x_pos = rotor_disc_holes_pcd * cos(radians(angle))
    y_pos = rotor_disc_holes_pcd * sin(radians(angle))
    sketch = sketch.arc((-x_pos, -y_pos), rotor_disc_holes_radius, 0.0, 360.0)
sketch = sketch.assemble()

bl = 2*rotor_disc_radius
bb = motor_coupler_gap_half*2
bh = rotor_disc_radius*2
box_cut = (
    cq.Workplane("XY").box(bl, bh, bb)
    .faces("<Y")
    .workplane()
    .moveTo(bl/2,0)
    .circle(motor_coupler_gap_half)
    .extrude(-bh)
    .translate((bl/2-rotor_disc_radius, 0, bb/2+rotor_coupler_thickness))
)

coupler_1 = cq.Workplane("XY").add(sketch).extrude(WIDTH).cut(box_cut)
coupler_2 = coupler_1.rotate((0,0,0),(0,1,0),-90).translate((WIDTH+L-rotor_coupler_thickness,0,-L+rotor_coupler_thickness))

w = WIDTH-rotor_coupler_thickness
box = cq.Workplane("XY").box(w, bh, w).edges("|Y and >Z and >X").fillet(20).translate((L+w/2,0,w/2+rotor_coupler_thickness))
# boxc = cq.Workplane("XY").box(WIDTH/2, bh, WIDTH/2).edges("|Y and >Z and >X").fillet(20).translate((L+WIDTH/2,0,WIDTH/2))
boxc = (
    cq.Workplane("XZ")
    .circle(motor_coupler_gap_half-10)
    .extrude(bh)
    .translate((L+motor_coupler_gap_half,bh/2,WIDTH/2))
)
box = box.cut(boxc)
w = 2*rotor_coupler_thickness
boxs = (
    cq.Workplane("XY")
    .box(w, bh, w)
    .faces("<Y")
    .workplane()
    .moveTo(-w/2,-w/2)
    .circle(w)
    .cutThruAll()
    .translate((L-w/2-rotor_coupler_thickness,0,-w/2))
)




coupler = coupler_1.union(coupler_2).union(box).union(boxs)

# # rot_up = 5
# motor = cq.importers.importStep("/home/robot/sudhir/quad_cad/assets/mx64/MX-64AT_AR.stp")
# motor1 = motor.translate((0, 0, WIDTH/2)).rotate((0,0,0),(0,0,1),0)
# motor2 = motor.rotate((0,0,0),(0,1,0),90).rotate((0,0,0),(1,0,0),90).translate((L+motor_coupler_gap_half,0,0-L+rotor_coupler_thickness))

# body = cq.Workplane("XY").box(300, motor_outer_thickness, 100).translate((50,0,-50-L-rotor_coupler_thickness/2+rotor_disc_radius-10))

# show_object(coupler)
# show_object(motor1)
# show_object(motor2)
# show_object(body)

coupler.export("../assets/quad_parts/coupler_v1.svg")
coupler.export("../assets/quad_parts/coupler_v1.step")
coupler.export("../assets/quad_parts/coupler_v1.stl")
print("coupler v1 saved successfully!")