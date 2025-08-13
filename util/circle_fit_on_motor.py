# Try to fit a circle and holes on the motor rotor part

import cadquery as cq
import math

result = cq.importers.importStep("/home/robot/sudhir/quad_cad/assets/mx64/MX-64AT_AR.stp")

# Motor attachment disc parameters
disc_radius = 28.0  # Radius of the main disc
hole_center_distance = 22.0  # Distance from disc center to hole centers (PCD)
hole_radius = 2.5  # Radius of each mounting hole
thickness = 5.0  # Thickness of the disc
num_holes = 8  # Number of mounting holes
disc_z_offset = 20.0  # Z-axis translation in mm (10 cm)
axle_hole_radius = 7.5  # Radius of center hole for motor axle

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

# Translate the disc along Z-axis
disc = disc.translate((0, 0, disc_z_offset))

# Now you have both the imported motor (result) and the mounting disc (disc)