import cadquery as cq
from math import cos, sin, tan, pi, radians, sqrt

HOLE_TOLERANCE = 0.25  # Tolerance for hole dimensions (in radius) due to 3D printing

## Motor rotor coupler params (Based on Actual Motor)
rotor_disc_radius = 15.0  # Radius of the motor rotor disc (30 mm diameter)
rotor_disc_holes_pcd = 11.0  # Distance from rotor center to hole centers (PCD) (22 mm diameter)
rotor_disc_holes_radius = 1.25 + HOLE_TOLERANCE  # Radius of each mounting hole (2.5 mm diameter)
rotor_disc_holes_num = 8  # Number of mounting holes
rotor_disc_axle_hole_radius = 5 + HOLE_TOLERANCE  # Radius of center hole for motor axle (10 mm diameter)


rotor_disc_sketch = cq.Sketch().arc((0, 0), rotor_disc_radius, 0.0, 360.0).arc((0.0, 0.0), rotor_disc_axle_hole_radius, 0.0, 360.0)
for i in range(rotor_disc_holes_num):
    angle = i * (360.0 / rotor_disc_holes_num)  # Degrees
    x_pos = rotor_disc_holes_pcd * cos(radians(angle))
    y_pos = rotor_disc_holes_pcd * sin(radians(angle))
    rotor_disc_sketch = rotor_disc_sketch.arc((-x_pos, -y_pos), rotor_disc_holes_radius, 0.0, 360.0)
rotor_disc_sketch = rotor_disc_sketch.assemble()
rotor_disc_2mm = cq.Workplane("XY").placeSketch(rotor_disc_sketch).extrude(2)

rotor_disc_1_5mm = cq.Workplane("XY").placeSketch(rotor_disc_sketch).extrude(1.5)
rotor_disc_2_5mm = cq.Workplane("XY").placeSketch(rotor_disc_sketch).extrude(2.5)


rotor_disc_2mm.export("../assets/quad_parts/rotor_disc_2mm.svg")
rotor_disc_2mm.export("../assets/quad_parts/rotor_disc_2mm.step")
rotor_disc_2mm.export("../assets/quad_parts/rotor_disc_2mm.stl")

rotor_disc_1_5mm.export("../assets/quad_parts/rotor_disc_1_5mm.step")
rotor_disc_1_5mm.export("../assets/quad_parts/rotor_disc_1_5mm.stl")

rotor_disc_2_5mm.export("../assets/quad_parts/rotor_disc_2_5mm.step")
rotor_disc_2_5mm.export("../assets/quad_parts/rotor_disc_2_5mm.stl")

print("Rotor disc saved successfully!")