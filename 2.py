import importlib
from math import tan, sqrt, sin, pi

from cadquery import *
from cadquery.selectors import *
from shared import *
import shared

importlib.reload(shared)

p1 = (Workplane("XY")
  .transformed(offset=(width / 2, length / 2, 0))
  .rect(width, length)
  .extrude(-highest, taper=15)
  .faces(">Z").shell(-thickness, kind="intersection")
)

taper_width = abs(tan(((90 - 75) / 180) * pi) * highest)
rect_bottom_width = width - (taper_width  * 2)
rect_bottom_length = length - (taper_width  * 2)

inner_wall = taper_width + thickness

p2 = (p1
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(thickness / 2, 0, -button_height), rotate=(0, 0, 90))
  .pushPoints(btn_holes)
  .rect(button_width, thickness * 3.0)
  .cutBlind(button_height)
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(width - thickness / 2, 0, -button_height), rotate=(0, 0, 90))
  .pushPoints(btn_holes)
  .rect(button_width, thickness * 3.0)
  .cutBlind(button_height)
)

p3 = (p2
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(
    offset=(
      thickness / 2,
      (distance_to_usb_b + (usb_b_width / 2.0)),
      0
    ),
    rotate=(0, 0, 90)
  )
  .rect(usb_b_width, thickness * 3.0)
  .cutBlind(-usb_b_height)
)

p4 = (p3
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
    .transformed(
      offset=(
        width - thickness / 2,
        (distance_to_vibration_motor + (vibration_motor_width / 2.0)),
        0
      ),
      rotate=(0, 0, 90)
     )
  .rect(vibration_motor_width, thickness * 3.0)
  .cutBlind(-vibration_motor_height)
)
 

p5 = (p4
  .edges(
      BoxSelector(
      (0, 0, -usb_b_height),
      (width, length, -highest),
    )
    - BoxSelector(
      (taper_width - thickness, taper_width - thickness, -usb_b_height),
      (width - (taper_width - thickness), length - (taper_width - thickness), -highest + thickness),
    )
  )
  .fillet(case_fillet)
)

p6 = (p5
  .faces("<<Y[3]").wires().toPending().translate((0, -tbar_diameter, 0)).toPending().loft()
  .faces(">>Y[3]").wires().toPending().translate((0, tbar_diameter, 0)).toPending().loft()
)

tbar_taper_width = abs(tan(((90 - 75) / 180) * pi) * (highest - thickness))
tbar_cut_length = thickness + tbar_diameter + tbar_taper_width + 1

p7 = (p6
  .faces("<Z")
  .workplane(centerOption="CenterOfBoundBox", invert=True)
  .move(0, length / -2 + tbar_cut_length / 2)
  .rect(tbar_22_retracted, tbar_cut_length)
  .cutBlind(tbar_diameter)
  .faces("<Z")
  .workplane(centerOption="CenterOfBoundBox", invert=True)
  .move(0, length / 2 - tbar_cut_length / 2)
  .rect(tbar_22_retracted, tbar_cut_length)
  .cutBlind(tbar_diameter)
)

tbar_space = width - rect_bottom_width
tbar_pin_x = inner_wall + tbar_space / 2
tbar_pin_y = inner_wall + tbar_diameter / 2

p8 = (p7
  .faces(NearestToPointSelector((tbar_pin_x, tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
  .faces(NearestToPointSelector((width - tbar_pin_x, length - tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
  .faces(NearestToPointSelector((tbar_pin_x, length - tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
  .faces(NearestToPointSelector((width - tbar_pin_x, tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
)

p9 = (p8
  .edges(
      NearestToPointSelector((inner_wall, length / 2, -highest + thickness))
    + NearestToPointSelector((inner_wall, inner_wall + tbar_diameter, -highest + thickness))
    + NearestToPointSelector((inner_wall, inner_wall + tbar_diameter, -highest / 2))
    + NearestToPointSelector((inner_wall, length - (inner_wall + tbar_diameter), -highest + thickness))
    + NearestToPointSelector((inner_wall, length - (inner_wall + tbar_diameter), -highest / 2))
    
    + NearestToPointSelector((width - inner_wall, length / 2, -highest + thickness))
    + NearestToPointSelector((width - inner_wall, inner_wall + tbar_diameter, -highest + thickness))
    + NearestToPointSelector((width - inner_wall, inner_wall + tbar_diameter, -highest / 2))
    + NearestToPointSelector((width - inner_wall, length - (inner_wall + tbar_diameter), -highest + thickness))
    + NearestToPointSelector((width - inner_wall, length - (inner_wall + tbar_diameter), -highest / 2))
  )
  .fillet(1.0)
)

p10 = (p9
  .edges(
      NearestToPointSelector((tbar_pin_x, tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width - tbar_pin_x, tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((tbar_pin_x, length - tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width - tbar_pin_x, length - tbar_cut_length, -highest + thickness / 2))
  )
  .fillet(1.0)
)
 
crl = length - crush_rib_length;

rib_sketch = (p10
  .faces(">Z")
  .workplane(origin=(0, crush_rib_length / 2, 0))
  .hLine(1.0)
  .sagittaArc((3.0, 0.0), 0.5)
  .hLineTo((width / 2) - 1.0)
  .sagittaArc(((width / 2) + 1.0, 0.0), 0.5)
  .hLineTo(width - 3.0)
  .sagittaArc((width - 1.0, 0.0), 0.5)
  .hLine(1.0)
  .vLine(crl)
  .hLine(-1.0)
  .sagittaArc((width - 3.0, crl), 0.5)
  .hLineTo((width / 2) + 1.0)
  .sagittaArc(((width / 2) - 1.0, crl), 0.5)
  .hLineTo(3.0)
  .sagittaArc((1.0, crl), 0.5)
  .hLine(-1.0)
  .close()
  .cutBlind(-crush_rib_depth)
)

rib_cut_close = (Workplane("YZ")
  .polarLine(crush_rib_length, 360 - 45)
  .vLineTo(0)
  .hLineTo(0)
  .close().extrude(width)
)

rib_cut_far = (Workplane("YZ")
  .transformed(rotate=(0, 0, 360 - 90))
  .polarLine(crush_rib_length, 360 - 45)
  .hLineTo(0)
  .vLineTo(0)
  .close()
  .extrude(width)
)

rib_cut_depth = (crush_rib_length * sqrt(2)) / 2

rib_cut = (rib_sketch
  .workplane(origin=(0, 0, 0))
  .cut(rib_cut_close.translate((0, crush_rib_length / 2, 0)))
  .workplane(origin=(0, 0, 0))
  .cut(rib_cut_far.translate(( 0, length - (crush_rib_length / 2), 0)))
)

case = rib_cut

show_object(case)

exporters.export(case, "wc2lf.stl")
