from cadquery import *
from watchy import *

p1 = (Workplane("XY")
  .spline([
    (lowest, lowest),
    (8.0, 5.0),
    (15.0, 7.0),
    (26.0, 8.5),
    (length, lowest),
  ])
  .close()
  .extrude(width)
  .faces("|Z").edges("%BSPLINE").fillet(fillet)
  .faces("<Y").shell(thickness)  
)

p2 = (p1
  .faces("|Z").pushPoints(btn_holes)
  .rect(button_width, button_height).cutThruAll()
)

p3 = (p2
  .faces("<Z")
    .moveTo(distance_to_usb_b + (usb_b_width / 2.0), usb_b_height / 2.0)
  .rect(usb_b_width, usb_b_height)
  .cutBlind(-thickness)
)

p4 = (p3
  .faces(">Z")
  .workplane()
    .moveTo(distance_to_vibration_motor + (vibration_motor_width / 2.0), vibration_motor_height / 2.0)
  .rect(vibration_motor_width, vibration_motor_height)
  .cutBlind(-thickness)
)

show_object(p4)


exporters.export(p4, "wc1lf.stl")
