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
  .transformed(offset=(thickness / 2, 0, -button_height - crush_rib_depth), rotate=(0, 0, 90))
  .pushPoints(btn_holes)
  .rect(button_width, thickness * 3.0)
  .cutBlind(button_height)
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(width - thickness / 2, 0, -button_height - crush_rib_depth), rotate=(0, 0, 90))
  .pushPoints(btn_holes)
  .rect(button_width, thickness * 3.0)
  .cutBlind(button_height)
)

p2_5 = (p2
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(width - thickness / 2, length / 2 + 6.15, -crush_rib_depth), rotate=(0, 0, 90))
  .rect(7.0, thickness * 4.0)
  .cutBlind(-chip_height)
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(thickness / 2, length / 2 + 6.15, -crush_rib_depth), rotate=(0, 0, 90))
  .rect(7.0, thickness * 4.0)
  .cutBlind(-chip_height)
)

p3 = (p2_5
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(
    offset=(
      width - thickness / 2,
      (distance_to_usb_b + (usb_b_width / 2.0)),
      -crush_rib_depth
    ),
    rotate=(0, 0, 90)
  )
  .rect(usb_b_width, thickness * 4.0)
  .cutBlind(-usb_b_height)
)

p4 = (p3
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
    .transformed(
      offset=(
        thickness / 2,
        (distance_to_vibration_motor + (vibration_motor_width / 2.0)),
        -crush_rib_depth
      ),
      rotate=(0, 0, 90)
     )
  .rect(vibration_motor_width, thickness * 4.0)
  .cutBlind(-vibration_motor_height)
)
 
p5 = (p4
  .edges(
      BoxSelector(
      (0, 0, -crush_rib_depth),
      (width, length, -highest),
    )
    - BoxSelector(
      (taper_width - thickness, taper_width - thickness, -usb_b_height),
      (width - (taper_width - thickness), length - (taper_width - thickness), -highest + thickness),
    )
    - BoxSelector(
      (0, taper_width, -crush_rib_depth),
      (width, length - taper_width, -highest + thickness),
    )
  )
  .fillet(case_fillet)
)

p6 = (p5
  .faces(NearestToPointSelector((width / 2, length - (taper_width + thickness), -highest / 2))).wires().toPending().translate((0, -tbar_diameter, 0)).toPending().loft()
  .faces(NearestToPointSelector((width / 2, (taper_width + thickness), -highest / 2))).wires().toPending().translate((0, tbar_diameter, 0)).toPending().loft()
)

tbar_taper_width = abs(tan(((90 - 75) / 180) * pi) * (highest - thickness))
tbar_cut_length = thickness + tbar_diameter + tbar_taper_width

rect_inner_width = (width - taper_width * 2) / -2 - thickness * 2

p7 = (p6
  .faces("<Z")
  .workplane(centerOption="CenterOfBoundBox", invert=True)
  .move(0, length / -2 + taper_width + thickness)
  .rect(tbar_24_retracted, tbar_cut_length)
  .cutBlind(tbar_diameter + 1.0)
  .faces("<Z")
  .workplane(invert=True)
  .move(0, length / 2 - taper_width - thickness)
  .rect(tbar_24_retracted, tbar_cut_length)
  .cutBlind(tbar_diameter + 1.0)
)

tbar_space = width / 2 - tbar_24_retracted / 2 + 3
tbar_pin_x = tbar_space
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
    + NearestToPointSelector((inner_wall, inner_wall + tbar_diameter, -highest / 2))
    + NearestToPointSelector((inner_wall, length - (inner_wall + tbar_diameter), -highest / 2))

    + NearestToPointSelector((width - inner_wall, length / 2, -highest + thickness))
    + NearestToPointSelector((width - inner_wall, inner_wall + tbar_diameter, -highest / 2))
    + NearestToPointSelector((width - inner_wall, length - (inner_wall + tbar_diameter), -highest / 2))
  )
  .fillet(0.30)
)

p10 = (p9
  .edges(
      NearestToPointSelector((tbar_pin_x - 0.5, tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width - tbar_pin_x + 0.5, tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((tbar_pin_x - 0.5, length - tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width - tbar_pin_x + 0.5, length - tbar_cut_length, -highest + thickness / 2))
  )
  .fillet(0.47)
)
 
crl = (length - crush_rib_length) + 1.0

rib_sketch = (p10
  .faces(">Z")
  .workplane(origin=(0, crush_rib_length / 2 - 0.5, 0))
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

watchy_fake = (Workplane("XY")
  .move(width / 2, length / 2)
  .rect(width, length - crush_rib_length)
  .extrude(-highest + crush_rib_depth)
)

rib_cut = (rib_sketch
  .faces(">Z")
  .edges("%CIRCLE")
  .chamfer(0.45)
  #.union(watchy_fake)
)

case = rib_cut

show_object(case)

exporters.export(case, "wc2lf24.step")
