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

# Motor attachment disc parameters
disc_radius = 14.0  # Radius of the main disc (28 mm diameter)
hole_center_distance = 11.0  # Distance from disc center to hole centers (PCD) (22 mm diameter)
hole_radius = 1.25  # Radius of each mounting hole (2.5 mm diameter)
thickness = 5.0  # Thickness of the disc
num_holes = 8  # Number of mounting holes
axle_hole_radius = 5.0  # Radius of center hole for motor axle (10 mm diameter)

# Create the motor attachment disc with holes
disc = cq.Workplane("XY").circle(disc_radius)

# Add center hole for motor axle
disc = disc.circle(axle_hole_radius)

# Add holes at equally spaced positions on the pitch circle
for i in range(num_holes):
    angle = i * (360.0 / num_holes)  # Degrees
    x_pos = hole_center_distance * math.cos(math.radians(angle))
    y_pos = hole_center_distance * math.sin(math.radians(angle))
    disc = disc.center(x_pos, y_pos).circle(hole_radius).center(-x_pos, -y_pos)

# Extrude the 2D profile to create the 3D disc with holes
disc = disc.extrude(thickness)

# Export the result in multiple formats
disc.export("rotor_coupler.svg")
disc.export("rotor_coupler.step")
