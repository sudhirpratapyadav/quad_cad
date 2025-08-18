import cadquery as cq
from math import cos, degrees, sin, tan ,pi, radians, sqrt

import numpy as np

### ------------PARAMETERS OF UPPER LEG-------------
## We will use (0,0) at rotor center (so its easy to later fit things properly)

HOLE_TOLERANCE = 0.25  # Tolerance for hole dimensions (in radius) due to 3D printing

## Motor coupler params (Based on Actual Motor)
rotor_disc_radius = 14.0 + 2 # 2 mm extra

inner_rect_w = 29 # Y direction
outer_rect_w = 40.2 # Y direction
hole_plate_w = (outer_rect_w-inner_rect_w)/2 # Y direction

inner_rect_l = 42.5 # This is from rotor center (not total l) (X direction)
outer_rect_l = inner_rect_l + hole_plate_w # (X direction)
l_offset = 10 # at what distance from rotor center to start the motor coupler (X direction)

motor_inner_thickness = 34.5 # 0.5 mm extra (Z dir)
motor_outer_thickness = 41.5 # 0.5 mm extra (Z dir)

LENGTH = outer_rect_l-l_offset # (X direction)
BREADTH = outer_rect_w + 10 # (Y direction)
HEIGHT = BREADTH # (Z direction)

assert HEIGHT > motor_outer_thickness, "Height must be greater than motor outer thickness"


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


box = cq.Workplane("XY").box(LENGTH, BREADTH, HEIGHT).translate((LENGTH/2+l_offset, 0, HEIGHT/2))
print("x,y,z",LENGTH, BREADTH, HEIGHT)
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

# Main outer box of motor
motor_box = box.faces(">Z").workplane().placeSketch(motor_coupler_holes).cutThruAll()

# 3 cuboidal cuts in the motor
cb1 =cq.Workplane().box(outer_rect_l, outer_rect_w, motor_inner_thickness).translate((outer_rect_l/2, 0, HEIGHT/2)) 
cb2 = cq.Workplane().box(inner_rect_l, inner_rect_w, motor_outer_thickness).translate((inner_rect_l/2, 0, HEIGHT/2))
cb3_l = h1_l-h3_l 
cb3 = cq.Workplane().box(cb3_l, HEIGHT*2+5, motor_inner_thickness).translate((h3_l+cb3_l/2, 0, HEIGHT/2)) # Y DIrection
cut_box_motor = cb1.union(cb2).union(cb3)

# final motor socket
motor_socket = motor_box.cut(cut_box_motor).translate((0, 0, -BREADTH/2))

xl = HEIGHT-LENGTH
wy = BREADTH-outer_rect_w
wz = HEIGHT-motor_inner_thickness
box_x = (
    cq.Workplane("XY")
    .box(xl,HEIGHT,BREADTH)
    .translate((xl/2+outer_rect_l,0,0))
    .faces(">X")
    .workplane()
    .rect(HEIGHT-wy, BREADTH-wz)
    .cutThruAll()
    
)
cut_box_z_size = 15
cut_box_z = cq.Workplane("XY").box(cut_box_z_size, cut_box_z_size, BREADTH).edges("|Z").fillet(cut_box_z_size/2-0.1).translate((outer_rect_l+xl/2, 0, 0))



# Front Left socket + motor
mfl = motor_socket
mfr = mfl.mirror(mirrorPlane="YZ", basePointVector=(l_offset+LENGTH+xl/2, 0, 0))

front_body = box_x.union(mfl).union(mfr).cut(cut_box_z)



size=(xl+LENGTH-wz)*2/sqrt(3)
zl = 3.5*size+10
box_z = (
    cq.Workplane("XY")
    .box(xl+LENGTH,HEIGHT,zl)
    .faces(">Z")
    .workplane()
    .rect(xl+LENGTH-wz, HEIGHT-wz)
    .cutThruAll()
    .translate(((xl+LENGTH)/2+l_offset+LENGTH/2,0,zl/2+HEIGHT/2))
)
cb_zl = 20

fs=4
tc1 = (
    cq.Workplane("XZ")
    .polyline([(0,size/2), (0,-size/2), (sqrt(3)*size/2,0), (0,size/2)]).close()
    .extrude(wz/2)
    .edges("|Y")
    .fillet(fs)
    .translate((l_offset+LENGTH/2+wz/2,BREADTH/2,HEIGHT/2+10))
)
gap = 2*size/2
stuss_cuts_top = (
    tc1.translate((fs/2,0,size/2))
    .union(tc1.rotateAboutCenter((0,1,0),180).translate((-fs/2+size*sqrt(3)/6,0,size/2+gap)))
    .union(tc1.translate((fs/2,0,size/2+2*gap)))
    .union(tc1.rotateAboutCenter((0,1,0),180).translate((-fs/2+size*sqrt(3)/6,0,size/2+3*gap)))
)
stuss_cut_bottom = stuss_cuts_top.mirror(mirrorPlane="ZX", basePointVector=(0, 0, 0)).rotateAboutCenter((1,0,0),180)
stuss_cut_left = stuss_cuts_top.rotateAboutCenter((0,0,1),90).translate(((xl+LENGTH)/2-wz/4,fs/2-size*sqrt(3)/3,0))
stuss_cut_right = stuss_cut_left.mirror(mirrorPlane="YZ", basePointVector=(l_offset+LENGTH+xl/2, 0, 0)).rotateAboutCenter((0,1,0),180)

box_z = box_z.cut(stuss_cuts_top).cut(stuss_cut_bottom).cut(stuss_cut_left).cut(stuss_cut_right)

front_body = front_body.union(box_z)


back_body = front_body.mirror(mirrorPlane="XY", basePointVector=(0, 0, (2*zl+HEIGHT)/2))

motor = cq.importers.importStep("/home/robot/sudhir/quad_cad/assets/mx64/MX-64AT_AR.stp")
motor = motor.translate((0, 0, 0)).rotate((0,0,0),(0,0,1),90)


body = front_body.union(back_body)

# show_object(mfl)
# show_object(mfl, options={"color": (0.5, 0.5, 0.5), "alpha": 0.5})
# show_object(mfr, options={"color": (0.5, 0.5, 0.5), "alpha": 0.5})
# show_object(box_x, options={"color": (0.5, 0.5, 0.5), "alpha": 0.5})
# show_object(box_z, options={"color": (0.5, 0.5, 0.5), "alpha": 0.5})
# show_object(motor)
# show_object(body, options={"color": (2/255, 50/255, 50/255), "alpha": 1.0})

body.export("../assets/quad_parts/body_v1.svg")
body.export("../assets/quad_parts/body_v1.step")
body.export("../assets/quad_parts/body_v1.stl")
print("body v1 saved successfully!")