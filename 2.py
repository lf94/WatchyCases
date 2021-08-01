import importlib
from math import tan, sqrt, sin, pi

from cadquery import *
from cadquery.selectors import *
from shared import *
import shared

importlib.reload(shared)

base = (Workplane("XY")
  .transformed(offset=(width / 2, length / 2, 0))
  .rect(width, length)
  .extrude(-highest, taper=15)
  .faces(">Z").shell(-thickness, kind="intersection")
)

taper_width = abs(tan(((90 - 75) / 180) * pi) * highest)
rect_bottom_width = width - (taper_width  * 2)
rect_bottom_length = length - (taper_width  * 2)

inner_wall = taper_width + thickness

with_button_cuts = (base
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(thickness / 2, crush_rib_length / 2, -button_height - crush_rib_depth), rotate=(0, 0, 90))
  .pushPoints(btn_holes)
  .rect(button_width, thickness * 3.0)
  .cutBlind(button_height)
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(width - thickness / 2, crush_rib_length / 2, -button_height - crush_rib_depth), rotate=(0, 0, 90))
  .pushPoints(btn_holes)
  .rect(button_width, thickness * 3.0)
  .cutBlind(button_height)
)

with_chip_cuts = (with_button_cuts
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(width - thickness / 2, length / 2, -crush_rib_depth), rotate=(0, 0, 90))
  .rect(25.0, thickness * 4.0)
  .cutBlind(-chip_height)
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(offset=(thickness / 2, length / 2, -crush_rib_depth), rotate=(0, 0, 90))
  .rect(25.0, thickness * 4.0)
  .cutBlind(-chip_height)
)

with_usb_cut = (with_chip_cuts
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
  .transformed(
    offset=(
      thickness / 2,
      crush_rib_length / 2 + (distance_to_usb_b + (usb_b_width / 2.0)),
      -crush_rib_depth
    ),
    rotate=(0, 0, 90)
  )
  .rect(usb_b_width, thickness * 4.0)
  .cutBlind(-usb_b_height)
)

with_vib_cut = (with_usb_cut
  .faces(">Z")
  .workplane(origin=(0, 0, 0))
    .transformed(
      offset=(
        width - thickness / 2,
        crush_rib_length / 2 + (distance_to_vibration_motor + (vibration_motor_width / 2.0)),
        -crush_rib_depth
      ),
      rotate=(0, 0, 90)
     )
  .rect(vibration_motor_width, thickness * 4.0)
  .cutBlind(-vibration_motor_height)
)
 
with_outer_fillet = (with_vib_cut
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

with_inner_far_sides_extruded = (with_outer_fillet
  .faces(NearestToPointSelector((width / 2, length - (taper_width + thickness), -highest / 2))).wires().toPending().translate((0, -past_slot, 0)).toPending().loft()
  .faces(NearestToPointSelector((width / 2, (taper_width + thickness), -highest / 2))).wires().toPending().translate((0, past_slot, 0)).toPending().loft()
)

tbar_taper_width = abs(tan(((90 - 75) / 180) * pi) * (highest - thickness))
tbar_cut_length = thickness + tbar_diameter + tbar_taper_width

rect_inner_width = (width - taper_width * 2) / -2 - thickness * 2

with_strap_cuts  = (with_inner_far_sides_extruded
  .faces("<Z")
  .workplane(centerOption="CenterOfBoundBox", invert=True)
  .move(0, length / -2 + taper_width + thickness)
  .rect(tbar_24_retracted, tbar_cut_length)
  .cutBlind(tbar_diameter + 0.5)
  .faces("<Z")
  .workplane(invert=True)
  .move(0, length / 2 - taper_width - thickness)
  .rect(tbar_24_retracted, tbar_cut_length)
  .cutBlind(tbar_diameter + 0.5)
)

tbar_space = width / 2 - tbar_24_retracted / 2 + 3
tbar_pin_x = tbar_space
tbar_pin_y = inner_wall + tbar_diameter / 2

with_rod_cuts = (with_strap_cuts
  .faces(NearestToPointSelector((tbar_pin_x, tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
  .faces(NearestToPointSelector((width - tbar_pin_x, length - tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
  .faces(NearestToPointSelector((tbar_pin_x, length - tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
  .faces(NearestToPointSelector((width - tbar_pin_x, tbar_pin_y, -highest)))
    .workplane(centerOption="CenterOfBoundBox").circle(tbar_hole / 2).cutBlind(-tbar_pin_depth)
)

with_inner_fillet = (with_rod_cuts
  .edges(
      NearestToPointSelector((inner_wall, length / 2, -highest + thickness))
    + NearestToPointSelector((inner_wall, inner_wall + tbar_diameter, -highest / 2))
    + NearestToPointSelector((inner_wall, length - (inner_wall + tbar_diameter), -highest / 2))
    + NearestToPointSelector((width / 2, (inner_wall + tbar_diameter + 1), -highest + thickness))

    + NearestToPointSelector((width - inner_wall, length / 2, -highest + thickness))
    + NearestToPointSelector((width - inner_wall, inner_wall + tbar_diameter, -highest / 2))
    + NearestToPointSelector((width - inner_wall, length - (inner_wall + tbar_diameter), -highest / 2))
    + NearestToPointSelector((width / 2, length - (inner_wall + tbar_diameter + 1), -highest + thickness))
  )
  .fillet(0.50)
)

with_fillets_near_straps = (with_inner_fillet
  .edges(
      NearestToPointSelector((tbar_pin_x - 0.5, tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width - tbar_pin_x + 0.5, tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((tbar_pin_x - 0.5, length - tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width - tbar_pin_x + 0.5, length - tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width / 2, length - tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width / 2, tbar_cut_length, -highest + thickness / 2))
    + NearestToPointSelector((width - tbar_pin_x + 0.5, tbar_cut_length + 1, -highest + tbar_diameter / 2))
    + NearestToPointSelector((tbar_pin_x + 0.5, tbar_cut_length + 1, -highest + tbar_diameter / 2))
    + NearestToPointSelector((width - tbar_pin_x + 0.5, length - (tbar_cut_length + 1), -highest + tbar_diameter / 2))
    + NearestToPointSelector((tbar_pin_x + 0.5, length - (tbar_cut_length + 1), -highest + tbar_diameter / 2))
    + NearestToPointSelector((width / 2, tbar_cut_length, -highest + tbar_diameter))
    + NearestToPointSelector((width / 2, length - tbar_cut_length, -highest + tbar_diameter))
  )
  .fillet(0.5)
)

with_fillets_near_straps_2 = (with_fillets_near_straps
  .edges(
    NearestToPointSelector((width / 2, taper_width, -highest + tbar_diameter))
    + NearestToPointSelector((width / 2, length - taper_width, -highest + tbar_diameter))
  )
  .fillet(0.5)
)
 
crl = (length - crush_rib_length) + 1.0

rib_sketch = (with_fillets_near_straps_2
  .faces(">Z")
  .workplane(origin=(0, crush_rib_length / 2 - (crush_rib_radius / 2), 0))
  .hLine(pcb_edge)
  .sagittaArc((pcb_edge + crush_rib_radius * 2, 0.0), crush_rib_sag)
  .hLineTo((width / 2) - crush_rib_radius)
  .sagittaArc(((width / 2) + crush_rib_radius, 0.0), crush_rib_sag)
  .hLineTo((width - pcb_edge) - crush_rib_radius * 2)
  .sagittaArc((width - pcb_edge, 0.0), crush_rib_sag)
  .hLine(pcb_edge)
  .vLine(crl)
  .hLine(-pcb_edge)
  .sagittaArc(((width - pcb_edge) - crush_rib_radius * 2, crl), crush_rib_sag)
  .hLineTo((width / 2) + crush_rib_radius)
  .sagittaArc(((width / 2) - crush_rib_radius, crl), crush_rib_sag)
  .hLineTo(pcb_edge + crush_rib_radius * 2)
  .sagittaArc((pcb_edge, crl), crush_rib_sag)
  .hLine(-pcb_edge)
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
  .chamfer(0.5)
  #.union(watchy_fake)
)

face_hole_cut_depth = 4.0

face_holes_cut = (rib_cut
  .faces(">Z[-2]")
  .workplane(origin=(0, 0, 0))
  .moveTo((width / 2 + 25.5 / 2) - 2.1 / 2, stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y)
  .slot2D(stub_length, stub_thickness).tag("s1")
  .moveTo((width / 2 - 25.5 / 2) + 2.1 / 2, stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y)
  .slot2D(stub_length, stub_thickness).tag("s2")
  .moveTo((width / 2 + 25.5 / 2) - 2.1 / 2, length - (stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y))
  .slot2D(stub_length, stub_thickness).tag("s3")
  .moveTo((width / 2 - 25.5 / 2) + 2.1 / 2, length - (stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y))
  .slot2D(stub_length, stub_thickness).tag("s4")
  .cutBlind(-face_hole_cut_depth, taper=-10)
  .edges(
      NearestToPointSelector(((width / 2 + 25.5 / 2) - 2.1 / 2, stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y, 0))
    + NearestToPointSelector(((width / 2 - 25.5 / 2) + 2.1 / 2, stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y, 0))
    + NearestToPointSelector(((width / 2 + 25.5 / 2) - 2.1 / 2, length - (stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y), 0))
    + NearestToPointSelector(((width / 2 - 25.5 / 2) + 2.1 / 2, length - (stub_thickness / 2 + crush_rib_length / 2 + to_pcb_slot_y), 0))
  )
  .chamfer(0.6)
)

base = face_holes_cut

top_of_face =  (length / 2) - (29 / 2)

side_seal_height = 2.6

face = (Workplane("XY")
  .rect(width + 1.0, length)
  .extrude(side_seal_height)
  .faces(">Z")
  .wires()
  .toPending()
  .offset2D(-0.6)
  .cutBlind(-(side_seal_height - 0.8))
  .workplane()
  .pushPoints([
    (25.5 / 2 - 2.1 / 2,  length / -2 + (to_pcb_slot_y + (stub_thickness / 2) + crush_rib_length / 2)),
    (-25.5 / 2 + 2.1 / 2, length/ -2  + (to_pcb_slot_y + (stub_thickness / 2) + crush_rib_length / 2)),
    (25.5 / 2 - 2.1 / 2,  length / 2  - (to_pcb_slot_y + (stub_thickness / 2) + crush_rib_length / 2)),
    (-25.5 / 2 + 2.1 / 2, length / 2  - (to_pcb_slot_y + (stub_thickness / 2) + crush_rib_length / 2)),
  ])
  .slot2D(stub_length, stub_thickness)
  .extrude(face_hole_cut_depth + 1.8)
  .faces(">Z")
  .chamfer(0.5)
  .faces("<Z")
  .workplane()
  .move(0, top_of_face - 5.8 - crush_rib_length / 2)
  .rect(28.6, 28.4)
  .cutThruAll()
  .edges("|Z")
  .fillet(case_fillet)
)


case = (
  Assembly()
  .add(base, name="base")
  .add(face, name="face")
)

#case.solve()

show_object(face)

svgopts = {
  "width": 800,
  "height": 200,
  "marginLeft": 0,
  "showHidden": False,
  "projectionDir": (-1, 1, 0.2),
}

exporters.export(base, "pictures/wc2lf24_base.svg", opt=svgopts)
exporters.export(face, "pictures/wc2lf24_face.svg", opt=svgopts)
exporters.export(base, "printable/wc2lf24_base.amf")
exporters.export(face, "printable/wc2lf24_face.amf")
exporters.export(base, "printable/wc2lf24_base.stl")
exporters.export(face, "printable/wc2lf24_face.stl")
