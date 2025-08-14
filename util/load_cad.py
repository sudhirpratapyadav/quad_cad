import cadquery as cq

motor = cq.importers.importStep("/home/robot/sudhir/quad_cad/assets/mx64/MX-64AT_AR.stp")
lower_leg = cq.importers.importStep("/home/robot/sudhir/quad_cad/assets/quad_parts/lower_leg_v3.step")
lower_leg = lower_leg.translate((0, 0, -30)).rotate((0,0,0),(0,0,1),-100)