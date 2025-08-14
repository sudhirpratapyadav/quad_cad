import cadquery as cq
import math


rotor_radius = 14.0  # Radius of the main rotor (28 mm diameter)
hole_center_distance = 11.0  # Distance from rotor center to hole centers (PCD) (22 mm diameter)
hole_radius = 1.25  # Radius of each mounting hole (2.5 mm diameter)
leg_part_1_thickness = 5.0  # Thickness of the disc
num_holes = 8  # Number of mounting holes
axle_hole_radius = 5.0  # Radius of center hole for motor axle (10 mm diameter)
W = 20.0
offset = 0
L1=90
bottom_offset=6
motor_width_half=55/2

R1 = 15
R2 = motor_width_half+leg_part_1_thickness+2
r = 6
d0 = 3
w = math.sqrt(R1**2 - d0**2)
d1 = 30
d2 = 40
d3 = 100


theta = math.atan2(w, d0)

# Sketch of first part of leg (attached to motor rotor)
sketch = (
    cq.Sketch()
    .arc((-R1,0), (0,R1), (d0,w))
    .spline([(d0, w), (d1,r)], [(math.sin(theta), -math.cos(theta)), (1, 0)], False)
    .segment((d1,r),(d2,r))
    .spline([(d2, r), (d3,R2)], [(1, 0), (1, 0)], False)
    .segment((d3,R2),(d3,0))
    .segment((d3,0),(0,0))
    
)
sketch = sketch.assemble()
solid = cq.Workplane().placeSketch(sketch).revolve(360, (0, 0, 0), (1, 0, 0))

cbox1 = cq.Workplane().box(80,30,80).translate((90, -25, 0))
cbox2 = cq.Workplane().box(80,30,80).translate((90, 25, 0))
cbox3 = cq.Workplane().box(50,30,10).translate((90, 0, 5+motor_width_half+leg_part_1_thickness))
cbox4 = cq.Workplane().box(50,30,10).translate((90, 0, -(5+motor_width_half+leg_part_1_thickness)))
sketch_semicirlce = (
    cq.Sketch()
    .arc((0,-motor_width_half), (-motor_width_half+7,0), (0,motor_width_half))
)
csc = cq.Workplane().placeSketch(sketch_semicirlce.assemble()).extrude(W).rotate((0,0,0),(1,0,0),90).translate((100,W/2,0))


leg = solid.cut(cbox1).cut(cbox2).cut(cbox3).cut(cbox4).cut(csc)



sketch = (
    cq.Sketch()
    .arc((0, 0), rotor_radius, 90.0, 90.0)
    .spline([(0, rotor_radius), (25,W/2+offset)], [(1, 0), (1, 0)], False) 
    .segment((25,W/2+offset),(L1,W/2+offset))
    .segment((L1,W/2+offset),(L1,-W/2+offset))
    .segment((L1,-W/2+offset),(25,-W/2+offset))
    .spline([(25,-W/2+offset), (0, -rotor_radius-bottom_offset), (-rotor_radius, 0)], [(-1.0, 0), (-1.0, 0), (0, 1.0)], False)
)
sketch = sketch.arc((0.0, 0.0), axle_hole_radius, 0.0, 360.0)
for i in range(num_holes):
    angle = i * (360.0 / num_holes)  # Degrees
    x_pos = hole_center_distance * math.cos(math.radians(angle))
    y_pos = hole_center_distance * math.sin(math.radians(angle))
    sketch = sketch.arc((-x_pos, -y_pos), hole_radius, 0.0, 360.0)
sketch = sketch.assemble()

rotor_coupler_1 = cq.Workplane("XY").placeSketch(sketch).extrude(leg_part_1_thickness).rotate((0,0,0),(0,0,1),180).translate((d3+L1, 0, motor_width_half))
rotor_coupler_2 = cq.Workplane("XY").placeSketch(sketch).extrude(leg_part_1_thickness).rotate((0,0,0),(0,0,1),180).translate((d3+L1, 0, -motor_width_half-leg_part_1_thickness))
