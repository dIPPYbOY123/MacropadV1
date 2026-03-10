import board
import busio
from adafruit_ssd1306 import SSD1306_I2C

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.scanners import DiodeOrientation

from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler

from kmk.extensions.rgb import RGB

keyboard = KMKKeyboard()

# Display Pins: D4 (SDA), D5 (SCL)
i2c = busio.I2C(board.D5, board.D4)

macros = Macros()
encoder_handler = EncoderHandler()

keyboard.modules.append(encoder_handler)
keyboard.modules.append(macros)
keyboard.modules.append(Layers())

# Matrix Configuration (3x2 grid)
# User Specification:
# Rows: Pin 8 (D7), Pin 9 (D8)
# Cols: Pin 7 (D6), Pin 6 (D5), Pin 5 (D4)
keyboard.col_pins = (board.D6, board.D5, board.D4)
keyboard.row_pins = (board.D7, board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Rotary Encoder Rotation: Pin 1 (D0), Pin 2 (D1)
# Encoder Button: Pin 4 (D3)
encoder_handler.pins = ((board.D0, board.D1, board.D3),)

# RGB Lighting: Pin 3 (D2), 7 Pixels
rgb = RGB(pixel_pin=board.D2, num_pixels=7)
keyboard.extensions.append(rgb)

# OLED Display Logic
class Display(SSD1306_I2C):
    def on_layer_change(self, layer: int):
        self.fill(0)
        self.text(f'MACROPAD V1', 0, 0, 1)
        self.text(f'LAYER: {layer}', 0, 16, 1)
        self.show()

display = Display(128, 32, i2c)  
keyboard.extensions.append(display)  

# Keymap: 6 Switches + 1 Encoder Button
# The Encoder Button (D3) is handled by the EncoderHandler
keyboard.keymap = [
    [ # Layer 0: Default
        KC.MUTE,     KC.Macro(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL)), # Key 1, 2
        KC.Macro(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL)), KC.Macro(Press(KC.LCTRL), Tap(KC.X), Release(KC.LCTRL)), # Key 3, 4
        KC.MO(1),    KC.LT(2, KC.RGB_TOG), # Key 5, 6
    ],
    [ # Layer 1: Navigation/Macros
        KC.UNDO,     KC.REDO,
        KC.Macro(Press(KC.LGUI), Press(KC.LSHIFT), Tap(KC.S), Release(KC.LSHIFT), Release(KC.LGUI)), KC.SELECT_ALL,
        KC.TRNS,     KC.TRNS,
    ],
    [ # Layer 2: RGB Control
        KC.RGB_MODE_PLAIN, KC.RGB_MODE_BREATHE,
        KC.RGB_MODE_RAINBOW, KC.RGB_MODE_SWIRL,
        KC.RGB_SAI, KC.RGB_SAD,
    ]
]

# Encoder Mapping: Volume, Navigation, RGB
encoder_handler.map = [
    [ (KC.VOLU, KC.VOLD, KC.PLAY_PAUSE) ], # Layer 0: Vol + Play/Pause
    [ (KC.PGUP, KC.PGDN, KC.MUTE) ],       # Layer 1: Scroll + Mute
    [ (KC.RGB_HUI, KC.RGB_HUD, KC.RGB_TOG) ] # Layer 2: Color + Toggle
]

# Initial Display
display.fill(0)
display.text('MACROPAD V1', 0, 10, 1)
display.show()

if __name__ == '__main__':
    keyboard.go()