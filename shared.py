nozzle_diameter = 0.2

thickness = 1.0

crush_rib_length = 2.4
crush_rib_depth  = 1.0

width   = 31.5 # Gives room for buttons to poke out.
length  = 46.0 + crush_rib_length
lowest  = 0.0
highest = 8.6 + crush_rib_depth

pcb_thickness = 1.5
case_fillet   = 2.5

offset_to_button = 7.5

button_width  = 5.0
button_height = 2.0

distance_between_buttons = 21.6

vibration_motor_width  = 11.0
vibration_motor_height = 2.5

usb_b_width  = 7.5
usb_b_height = 3.0

distance_to_vibration_motor = 16.6
distance_to_usb_b           = 19.5

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
