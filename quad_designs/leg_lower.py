"""
Quadruped Lower Leg - Motor Attachment Disc

This script creates a parametric disc for attaching to a motor rotor.
The disc features:
- Main circular disc with configurable radius
- 8 mounting holes equally spaced on a pitch circle
- Configurable hole size and position
- Adjustable thickness for extrusion

Modify the parameters below to customize the design.
"""

import cadquery as cq
import math

# Motor rotor coupler params
rotor_radius = 14.0  # Radius of the main rotor (28 mm diameter)
hole_center_distance = 11.0  # Distance from rotor center to hole centers (PCD) (22 mm diameter)
hole_radius = 1.25  # Radius of each mounting hole (2.5 mm diameter)
thickness = 5.0  # Thickness of the disc
num_holes = 8  # Number of mounting holes
axle_hole_radius = 5.0  # Radius of center hole for motor axle (10 mm diameter)

# Exntension params
L = 60.0
W = 20.0
offset = 0
bottom_offset = 3

sketch = (
    cq.Sketch()
    .arc((0, 0), rotor_radius, 90.0, 90.0)
    .spline([(0, rotor_radius), (25,W/2+offset)], [(1, 0), (1, 0)], False) 
    .segment((25,W/2+offset),(L,W/2+offset))
    .segment((L,W/2+offset),(L,-W/2+offset))
    .segment((L,-W/2+offset),(25,-W/2+offset))
    .spline([(25,-W/2+offset), (0, -rotor_radius-bottom_offset), (-rotor_radius, 0)], [(-1.0, 0), (-1.0, 0), (0, 1.0)], False)
)

# Add center hole for motor axle at origin
sketch = sketch.arc((0.0, 0.0), axle_hole_radius, 0.0, 360.0)

# Add holes at equally spaced positions on the pitch circle
for i in range(num_holes):
    angle = i * (360.0 / num_holes)  # Degrees
    x_pos = hole_center_distance * math.cos(math.radians(angle))
    y_pos = hole_center_distance * math.sin(math.radians(angle))
    sketch = sketch.arc((-x_pos, -y_pos), hole_radius, 0.0, 360.0)

# Extrude the 2D profile to create the 3D disc with holes
sketch = sketch.assemble()

rotor_coupler = cq.Workplane("XY").placeSketch(sketch).extrude(thickness)

# Export the result in multiple formats
rotor_coupler.export("rotor_coupler.svg")
rotor_coupler.export("rotor_coupler.step")
