import cadquery as cq
import math

### ------------PARAMETERS OF LOWER LEG-------------

HOLE_TOLERANCE = 0.25  # Tolerance for hole dimensions (in radius) due to 3D printing

## Motor rotor coupler params (Based on Actual Motor)
rotor_disc_radius = 14.0  # Radius of the motor rotor disc (28 mm diameter)
rotor_disc_holes_pcd = 11.0  # Distance from rotor center to hole centers (PCD) (22 mm diameter)
rotor_disc_holes_radius = 1.25 + HOLE_TOLERANCE  # Radius of each mounting hole (2.5 mm diameter)
rotor_disc_holes_num = 8  # Number of mounting holes
rotor_disc_axle_hole_radius = 5 + HOLE_TOLERANCE  # Radius of center hole for motor axle (10 mm diameter)

## Parameters of leg_part_1
rotor_coupler_thickness = 5.0  # Thickness of the coupler disc and extension attached to rotor disc
L1 = 90.0 # Length of leg_part_1: first part of leg (attached to motor rotor)
WIDTH = 20.0 # Width of the leg_part_1
motor_coupler_gap_half = 52/2 # Breadth of leg_part_1

# sketch parameters
offset = 0
angle_deg = 6
delta_back = math.tan(angle_deg*math.pi/180)*WIDTH/2
bottom_offset = 7

## Parameters for leg_part_2
L2 = 110 # Length of leg_part_2 (from end of leg_part_1 till sphere center)
rect_to_square_dist = 60
square_to_circle_dist = L2-rect_to_square_dist
start_rect_breadth = 2*(motor_coupler_gap_half+rotor_coupler_thickness) # breadth of the rectangular crossection at start of leg_part_2 (width is as same WIDTH)
midlle_square_size = 10 # size of the square cross section at the mid part of leg_part_2
end_circle_radius = 6 # radius of the circular cross-section at the end of leg_part_2

## End sphere params
sphere_radius = 10
sphere_cut_dist = math.sqrt(sphere_radius**2 - end_circle_radius**2) # distance from center of sphere where we need to cut the sphere to attach it to circular end
sphere_to_rotor_dist = L1+L2+sphere_cut_dist # Distance between rotor coupler center to sphere center

Total_LENGTH = L1 + L2 + sphere_cut_dist + sphere_radius
print("Total Length = ",Total_LENGTH)
### --------------------------------------------------------------

# Sketch of leg_part_1
sketch = (
    cq.Sketch()
    .arc((0, 0), rotor_disc_radius, 90.0, 90.0)
    .spline([(0, rotor_disc_radius), (25,WIDTH/2+offset)], [(1, 0), (1, 0)], False) 
    .segment((25,WIDTH/2+offset),(L1+delta_back,WIDTH/2+offset))
    .segment((L1+delta_back,WIDTH/2+offset),(L1-delta_back,-WIDTH/2+offset))
    .segment((L1-delta_back,-WIDTH/2+offset),(25,-WIDTH/2+offset))
    .spline([(25,-WIDTH/2+offset), (0, -rotor_disc_radius-bottom_offset), (-rotor_disc_radius, 0)], [(-1.0, 0), (-1.0, 0), (0, 1.0)], False)
)
sketch = sketch.arc((0.0, 0.0), rotor_disc_axle_hole_radius, 0.0, 360.0)
for i in range(rotor_disc_holes_num):
    angle = i * (360.0 / rotor_disc_holes_num)  # Degrees
    x_pos = rotor_disc_holes_pcd * math.cos(math.radians(angle))
    y_pos = rotor_disc_holes_pcd * math.sin(math.radians(angle))
    sketch = sketch.arc((-x_pos, -y_pos), rotor_disc_holes_radius, 0.0, 360.0)
sketch = sketch.assemble()
rotor_coupler_1 = cq.Workplane("XY").placeSketch(sketch).extrude(rotor_coupler_thickness).translate((0, 0, motor_coupler_gap_half)) 
rotor_coupler_2 = cq.Workplane("XY").placeSketch(sketch).extrude(rotor_coupler_thickness).translate((0, 0, -motor_coupler_gap_half-rotor_coupler_thickness))

# Extra rotor rotor disc extrusion for tight fit
rotor_disc_sketch = cq.Sketch().arc((0, 0), rotor_disc_radius, 0.0, 360.0).arc((0.0, 0.0), rotor_disc_axle_hole_radius, 0.0, 360.0)
for i in range(rotor_disc_holes_num):
    angle = i * (360.0 / rotor_disc_holes_num)  # Degrees
    x_pos = rotor_disc_holes_pcd * math.cos(math.radians(angle))
    y_pos = rotor_disc_holes_pcd * math.sin(math.radians(angle))
    rotor_disc_sketch = rotor_disc_sketch.arc((-x_pos, -y_pos), rotor_disc_holes_radius, 0.0, 360.0)
rotor_disc_sketch = rotor_disc_sketch.assemble()
rotor_disc1 = cq.Workplane("XY").placeSketch(rotor_disc_sketch).extrude(1).translate((0, 0, motor_coupler_gap_half-1))
rotor_disc2 = cq.Workplane("XY").placeSketch(rotor_disc_sketch).extrude(1).translate((0, 0, -motor_coupler_gap_half))

# Leg part one combined
leg_part_1 = rotor_coupler_1.union(rotor_coupler_2).union(rotor_disc1).union(rotor_disc2)

# Leg part 2 
start_rect = cq.Sketch().rect(start_rect_breadth, WIDTH).vertices().fillet(0.3)
mid_square = cq.Sketch().rect(midlle_square_size, midlle_square_size).vertices().fillet(0.3)
end_circle = cq.Sketch().circle(end_circle_radius)
leg_part_2 = cq.Workplane().placeSketch(
    start_rect, 
    mid_square.moved(cq.Location(cq.Vector(0, 0, rect_to_square_dist))), 
    end_circle.moved(cq.Location(cq.Vector(0, 0, rect_to_square_dist+square_to_circle_dist)))
).loft().rotate((0,0,0), (0,1,0), 90).translate((L1, 0, 0))

# End Sphere
cutting_box = cq.Workplane("XY").box(sphere_radius*2, sphere_radius*2, sphere_radius*2).translate((-sphere_cut_dist-sphere_radius, 0, 0))
sphere = cq.Workplane("XY").sphere(sphere_radius).cut(cutting_box).translate((sphere_to_rotor_dist, 0, 0))

# Combine leg part 2 and sphere to rotate them together
leg_part_23 = leg_part_2.union(sphere).rotate((L1,0,0), (L1,0,1), -angle_deg).translate((0, offset, 0))

# Combine All leg parts
lower_leg = leg_part_1.union(leg_part_23)

# Export the result in multiple formats
lower_leg.export("../assets/quad_parts/lower_leg.svg")
lower_leg.export("../assets/quad_parts/lower_leg.step")
lower_leg.export("../assets/quad_parts/lower_leg.stl")

# Alternative method using show_object for CQGI export
# show_object(lower_leg)
