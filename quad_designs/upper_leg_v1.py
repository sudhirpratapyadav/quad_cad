import cadquery as cq
import math

import numpy as np


L1 = 210
L1_actual = 170
L2 = 40
L3 = 80
L4 = 130
th1 = 27*math.pi/180
th2=-60*math.pi/180
th3 = 0
th4=20*math.pi/180

r0=80/2
r1=30/2
r1_actual=40/2
r2=30/2
r3=20/2
r4=40/2

p0 = (0,0)
p1 = (L1*math.cos(th1),L1*math.sin(th1))
p1_actual = (L1_actual*math.cos(th1),L1_actual*math.sin(th1))
p2 = (p1[0]+L2*math.cos(th1+th2), p1[1]+L2*math.sin(th1+th2))
p3 = (p2[0]+L3*math.cos(th1+th2+th3), p2[1]+L3*math.sin(th1+th2+th3))
p4 = (p3[0]+L4*math.cos(th1+th2+th3+th4), p3[1]+L4*math.sin(th1+th2+th3+th4))

c1a  = (p0[0]+r0*math.cos(th1+math.pi/2), p0[1]+r0*math.sin(th1+math.pi/2))
c1b = (p0[0]+r0*math.cos(th1-math.pi/2), p0[1]+r0*math.sin(th1-math.pi/2))
c2a  = (p1[0]+r1*math.cos(th1+math.pi/2), p1[1]+r1*math.sin(th1+math.pi/2))
c2b = (p1[0]+r1*math.cos(th1-math.pi/2), p1[1]+r1*math.sin(th1-math.pi/2))

delta_ang = -15*math.pi/180
c2a_actual = (p1_actual[0]+r1_actual*math.cos(th1+delta_ang+math.pi/2), p1_actual[1]+r1_actual*math.sin(th1+delta_ang+math.pi/2))
c2b_actual = (p1_actual[0]+r1_actual*math.cos(th1+delta_ang-math.pi/2), p1_actual[1]+r1_actual*math.sin(th1+delta_ang-math.pi/2))

c3a = (p1[0]+r1*math.cos(th1+th2+math.pi/2), p1[1]+r1*math.sin(th1+th2+math.pi/2))
c3b = (p1[0]+r1*math.cos(th1+th2-math.pi/2), p1[1]+r1*math.sin(th1+th2-math.pi/2))
c4a = (p2[0]+r2*math.cos(th1+th2+math.pi/2), p2[1]+r2*math.sin(th1+th2+math.pi/2))
c4b = (p2[0]+r2*math.cos(th1+th2-math.pi/2), p2[1]+r2*math.sin(th1+th2-math.pi/2))

c5a = (p2[0]+r2*math.cos(th1+th2+th3+math.pi/2), p2[1]+r2*math.sin(th1+th2+th3+math.pi/2))
c5b = (p2[0]+r2*math.cos(th1+th2+th3-math.pi/2), p2[1]+r2*math.sin(th1+th2+th3-math.pi/2))
c6a = (p3[0]+r3*math.cos(th1+th2+th3+math.pi/2), p3[1]+r3*math.sin(th1+th2+th3+math.pi/2))
c6b = (p3[0]+r3*math.cos(th1+th2+th3-math.pi/2), p3[1]+r3*math.sin(th1+th2+th3-math.pi/2))

delta=-(th1+th2+th3+th4)+20*math.pi/180
c7a = (p3[0]+r3*math.cos(th1+th2+th3+th4+math.pi/2), p3[1]+r3*math.sin(th1+th2+th3+th4+math.pi/2))
c7b = (p3[0]+r3*math.cos(th1+th2+th3+th4-math.pi/2), p3[1]+r3*math.sin(th1+th2+th3+th4-math.pi/2))
c8a = (p4[0]+r4*math.cos(th1+th2+th3+th4+delta+math.pi/2), p4[1]+r4*math.sin(th1+th2+th3+th4+delta+math.pi/2))
c8b = (p4[0]+r4*math.cos(th1+th2+th3+th4-math.pi/2), p4[1]+r4*math.sin(th1+th2+th3+th4-math.pi/2))

t1 = (math.cos(th1), math.sin(th1))
t1_actual = (math.cos(th1+delta_ang), math.sin(th1+delta_ang))
t2 = (math.cos(th1+th2), math.sin(th1+th2))
t3 = (math.cos(th1+th2+th3), math.sin(th1+th2+th3))
t4 = (math.cos(th1+th2+th3+th4+delta), math.sin(th1+th2+th3+th4+delta))

# Sketch of first part of leg (attached to motor rotor)
sketch = cq.Sketch()
sketch = sketch.arc(p0,r0,90+th1*180/math.pi,180)
sketch = sketch.arc(p2,r2,-123,180)
sketch = sketch.spline([c1a, c2a_actual, c5a], [t1, t1_actual, t2], False)
sketch = sketch.spline([c1b, c2b_actual, c5b], [t1, t1_actual, t2], False)


# sketch = sketch.hull()
sketch = sketch.assemble()

d1 = np.linalg.norm(np.array(p2) - np.array(p0))
d2 = np.linalg.norm(np.array(p4) - np.array(p2))
d3 = np.linalg.norm(np.array(p4) - np.array(p0))

print(d1,d2,d3)