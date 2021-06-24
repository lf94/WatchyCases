nozzle_diameter = 0.2

thickness = 1.0

crush_rib_length = 3.6
crush_rib_depth  = 1.6

width   = 33.8
length  = 45.8 + crush_rib_length
lowest  = 0.0
highest = 8.6 + crush_rib_depth

pcb_thickness = 1.5
case_fillet   = 1.2

pcb_edge = 3.0

offset_to_button = 7.4

chip_height = 1.2

button_width  = 5.0
button_height = 2.0

distance_between_buttons = 21.8

vibration_motor_width  = 11.0
vibration_motor_height = 2.8

usb_b_width  = 8.4
usb_b_height = 3.0

distance_to_vibration_motor = 19.5
distance_to_usb_b           = 17.9

btn_holes = ([
  (offset_to_button + (button_width / 2.0), 0.0),
  (offset_to_button + button_width + distance_between_buttons + (button_width / 2.0), 0.0)
])

tbar_22_extended  = 24.6
tbar_22_retracted = 21.7
tbar_24_extended   = 26.4
tbar_24_retracted  = 24.0
tbar_pin_depth  = 1.0 # or tbar_extended - tbar_retracted
tbar_thickness  = 3.5
tbar_diameter   = 3.0
tbar_hole       = 1.0
