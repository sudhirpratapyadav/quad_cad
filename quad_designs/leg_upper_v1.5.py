import cadquery as cq
from math import cos, degrees, sin, tan ,pi, radians, sqrt

import numpy as np

### ------------PARAMETERS OF UPPER LEG-------------
## We will use (0,0) at rotor center (so its easy to later fit things properly)

HOLE_TOLERANCE = 0.25  # Tolerance for hole dimensions (in radius) due to 3D printing

## Motor coupler params (Based on Actual Motor)
rotor_disc_radius = 14.0 + 2 # 2 mm extra
inner_rect_w = 29
inner_rect_l = 42.5 # This is from rotor center (not total l)
motor_inner_thickness = 34.5 # 0.5 mm extra
motor_outer_thickness = 41.5 # 0.5 mm extra
coupler_plate_thickness = 3+(motor_outer_thickness-motor_inner_thickness)/2 # 3 mm extra
outer_rect_w = 40.2
hole_plate_w = (outer_rect_w-inner_rect_w)/2
outer_rect_l = inner_rect_l + hole_plate_w

leg_B = 2*coupler_plate_thickness+motor_inner_thickness

# Holes params
hole_radius = 1.5 + HOLE_TOLERANCE
h1_w = 22/2
h2_w = 34.6/2
h3_w = h2_w
h1_l = 45.3
h2_l = 40.0
h3_l = 18.0
h4_l = -4.0
h4_w = h2_w

## Leg Params
L1= 150 # From rotor center to first bent
l1_ext = 170 # From rotor center to first bent (extended)
L2 = 50 # From bent to end rotor center
bend_angle=radians(-50) # Bend Anlge

# Control points/params to define profile
w1_h = outer_rect_w/2 +5 # width at start (5 mm extra from outer rectangle of motor)
w2_u=20 # Half upper width at bend
w2_l=19.5 # Half lower width at end 
w3_h=outer_rect_w/2 + 3 # width at end (3 mm extra from outer rectangle of motor)
l_offset = 10 # at what distance from rotor center to start the motor coupler

# Calculations for control points
c1_u = (l_offset,w1_h) # Start upper point
c1_l = (l_offset,-w1_h) # Start lower point
t1 = (1,0) # tangent at start point

delta1 = radians(10)
c2 = (L1, 0) # second point (Point of bend)
c2_u  = (c2[0]+w2_u*sin(delta1), c2[1]+w2_u*cos(delta1)) # upper point at point of bend 
c2_l = (c2[0], c2[1]-w2_l) # lower point at point of bend
t2_u = (cos(delta1), -sin(delta1)) # tangent at upper point (c2u)
t2_l = (1, 0) # tangent at lower point (c2l)

c3 = (l1_ext+(L2-l_offset)*cos(bend_angle), (L2-l_offset)*sin(bend_angle)) # point before rotor center (-l_offset from rotor center)
c3_u  = (c3[0]+w3_h*-sin(bend_angle), c3[1]+w3_h*cos(bend_angle)) # upper point of c3
c3_l = (c3[0]-w3_h*-sin(bend_angle), c3[1]-w3_h*cos(bend_angle)) # lower point of c3
t3_u = (cos(bend_angle), sin(bend_angle)) # tangent at c3_u
t3_l = (cos(bend_angle), sin(bend_angle)) # tangent at c3_l

# extra control point for little up bent to avoid lower leg intersection
c4  = (155,-21)
c4_tangent_angle = radians(-30)
t4 = (cos(c4_tangent_angle), sin(c4_tangent_angle))

c5 = (l1_ext+L2*cos(bend_angle), L2*sin(bend_angle)) # end rotor center

# Rotate the motor coupler holes to align with end rotor

leg_profile = (
    cq.Sketch()
    .segment(c1_u,c1_l)
    .segment(c3_u,c3_l)
    .spline([c1_u, c2_u, c3_u], [t1,t2_u,t3_u], False) # upper spline
    .spline([c1_l, c2_l, c4, c3_l], [t1,t2_l, t4, t3_l], False) # lower spline
).assemble()
motor_coupler_holes = (cq.Sketch()
    .arc((0,0),rotor_disc_radius,0,360)
    .arc((h1_l, h1_w), hole_radius, 0, 360)
    .arc((h1_l, -h1_w), hole_radius, 0, 360)
    .arc((h2_l, h2_w), hole_radius, 0, 360)
    .arc((h2_l, -h2_w), hole_radius, 0, 360)
    .arc((h3_l, h3_w), hole_radius, 0, 360)
    .arc((h3_l, -h3_w), hole_radius, 0, 360)
    # .arc((h4_l, h4_w), hole_radius, 0, 360)
    # .arc((h4_l, -h4_w), hole_radius, 0, 360)
).assemble()
leg_sketch = leg_profile.face(motor_coupler_holes, mode='s').face(motor_coupler_holes.moved(c5[0],c5[1],0,0,0,180+degrees(bend_angle)+3), mode='s')

print("Link end point, length (rotor to rotor)", c5, np.linalg.norm(c5))


leg_solid = cq.Workplane("XY").placeSketch(leg_sketch).extrude(leg_B)

cb1 =cq.Workplane().box(outer_rect_l, outer_rect_w, motor_inner_thickness).translate((outer_rect_l/2, 0, leg_B/2))
cb2 = cq.Workplane().box(inner_rect_l, inner_rect_w, motor_outer_thickness).translate((inner_rect_l/2, 0, leg_B/2))

# show_object(cut_box_motor)
cb3_l = h1_l-h3_l
cb3 = cq.Workplane().box(cb3_l, w1_h*2+5, motor_inner_thickness).translate((h3_l+cb3_l/2, 0, leg_B/2))
cut_box_motor = cb1.union(cb2).union(cb3)
box_l2 = 50
cut_box = (
    cq.Workplane()
    .box(box_l2, outer_rect_w, motor_inner_thickness)
    .translate((box_l2/2, 0, leg_B/2))
)


## Inner Cut Box
offset = 4 # offset for inner cut box

# Calculations for control points
c1_u = (l_offset,w1_h-offset) # Start upper point
c1_l = (l_offset,-w1_h+offset) # Start lower point
t1 = (1,0) # tangent at start point

# delta1 = radians(10)
w2_u = w2_u-offset # upper width at bend
c2 = (L1, 0) # second point (Point of bend)
c2_u  = (c2[0]+w2_u*sin(delta1), c2[1]+w2_u*cos(delta1)) # upper point at point of bend 
c2_l = (c2[0], c2[1]-w2_l+offset) # lower point at point of bend
t2_u = (cos(delta1), -sin(delta1)) # tangent at upper point (c2u)
t2_l = (1, 0) # tangent at lower point (c2l)

w3_h=w3_h-offset
c3 = (l1_ext+(L2-l_offset)*cos(bend_angle), (L2-l_offset)*sin(bend_angle)) # point before rotor center (-l_offset from rotor center)
c3_u  = (c3[0]+w3_h*-sin(bend_angle), c3[1]+w3_h*cos(bend_angle)) # upper point of c3
c3_l = (c3[0]-w3_h*-sin(bend_angle), c3[1]-w3_h*cos(bend_angle)) # lower point of c3
t3_u = (cos(bend_angle), sin(bend_angle)) # tangent at c3_u
t3_l = (cos(bend_angle), sin(bend_angle)) # tangent at c3_l

# # extra control point for little up bent to avoid lower leg intersection
c4  = (155+offset/2,-21+offset)
c4_tangent_angle = radians(-30)
t4 = (cos(c4_tangent_angle), sin(c4_tangent_angle))

leg_inner_profile = (
    cq.Sketch()
    .segment(c1_u,c1_l)
    .segment(c3_u,c3_l)
    .spline([c1_u, c2_u, c3_u], [t1,t2_u,t3_u], False) # upper spline
    .spline([c1_l, c2_l, c4, c3_l], [t1,t2_l, t4, t3_l], False) # lower spline
).assemble()
cut_inner_leg = (cq.Workplane()
                 .placeSketch(leg_inner_profile)
                 .extrude(motor_inner_thickness)
                 .translate((0, 0, coupler_plate_thickness))
)



# Triangle cuts
triangle_cut_1 = (
    cq.Workplane()
    .sketch()
    .regularPolygon(20, 3, tag="outer")
    .vertices(tag="outer")
    .fillet(3)
    .finalize()
    .extrude(20)
    .translate((0,0,-10))
)
triangle_cut_2 = (
    cq.Workplane()
    .sketch()
    .regularPolygon(19, 3, tag="outer")
    .vertices(tag="outer")
    .fillet(3)
    .finalize()
    .extrude(20)
    .translate((0,0,-10))
)
triangle_cut_3 = (
    cq.Workplane()
    .sketch()
    .regularPolygon(18, 3, tag="outer")
    .vertices(tag="outer")
    .fillet(3)
    .finalize()
    .extrude(20)
    .translate((0,0,-10))
)
size=13
triangle_cut_4 = (
    cq.Workplane()
    .polyline([(-size,size), (size*1.4,size*0.4), (0,-size), (-size,size)]).close()
    .extrude(20)
    .edges("|Z")
    .fillet(3)
    .translate((0,0,-10))
)
size=13
triangle_cut_4_5 = (
    cq.Workplane()
    .polyline([(5,size), (-size,-size), (size*1.6,size*0.6), (5,size)]).close()
    .extrude(20)
    .edges("|Z")
    .fillet(3)
    .translate((0,0,-10))
)
size=motor_inner_thickness
triangle_cut_5 = (
    cq.Workplane()
    .polyline([(0,-0.5*size),(-size*0.5,0.5*size), (size*0.5,0.5*size), (0,-0.5*size)]).close()
    .extrude(20)
    .edges("|Z")
    .fillet(3)
    .translate((0,0,-10))
).rotate((0,0,0),(1,0,0),90).translate((0,w1_h, leg_B/2-2))
upper_leg = (
    leg_solid
    .cut(cut_box_motor)
    .cut(cut_box_motor.rotate((0,0,0),(0,0,1),(180 + degrees(bend_angle) + 3)).translate((c5[0],c5[1],0)))
    .cut(cut_box)
    .cut(cut_inner_leg)
    .cut(triangle_cut_1.rotateAboutCenter((0,0,1),3).translate((70, -3, 0)))
    .cut(triangle_cut_2.rotateAboutCenter((0,0,1),180).translate((100, 5, 0)))
    .cut(triangle_cut_3.rotateAboutCenter((0,0,1),0).translate((130, -2, 0)))
    .cut(triangle_cut_4.translate((154, 0, 0)))
    .cut(triangle_cut_1.rotateAboutCenter((0,0,1),180).translate((70, 4, leg_B)))
    .cut(triangle_cut_2.rotateAboutCenter((0,0,1),3).translate((100, -3, leg_B)))
    .cut(triangle_cut_3.rotateAboutCenter((0,0,1),177).translate((130, 4, leg_B)))
    .cut(triangle_cut_4_5.rotateAboutCenter((0,0,1),0).translate((150, -5, leg_B)))
    .cut(triangle_cut_5.translate((70, 0, 0)))
    .cut(triangle_cut_5.rotateAboutCenter((0,1,0),180).translate((100, 0, -8)))
    .cut(triangle_cut_5.translate((130, 0, 0)))
    .cut(triangle_cut_5.rotateAboutCenter((0,1,0),180).translate((160, -10, -8)))
    .cut(triangle_cut_5.rotateAboutCenter((0,1,0),180).translate((70, -2*w1_h, -8)))
    .cut(triangle_cut_5.translate((100, -2*w1_h, 0)))
    .cut(triangle_cut_5.rotateAboutCenter((0,1,0),180).translate((130, -2*w1_h, -8)))
)



upper_leg.export("../assets/quad_parts/leg_upper_v1.5.svg")
upper_leg.export("../assets/quad_parts/leg_upper_v1.5.step")
upper_leg.export("../assets/quad_parts/leg_upper_v1.5.stl")
print("Upper leg v1.5 saved successfully!")

# show_object(triangle_cut, name="triangle_cut", options={"color": (0.5, 0.5, 0.5), "alpha": 0.5})

# show_object(leg_solid, options={"color": (0.5, 0.5, 0.5), "alpha": 0.5})
# show_object(cut_box1)
# show_object(cut_box2)
# show_object(cut_box_motor)
# show_object(cut_inner_leg)
# show_object(cut_box)
# show_object(upper_leg, name="upper_leg_trans", options={"color": (0.5, 0.5, 0.5), "alpha": 0.5})
# show_object(upper_leg, name="upper_leg", options={"color": (2/255, 50/255, 50/255)})
