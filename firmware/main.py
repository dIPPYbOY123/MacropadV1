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
i2c = busio.I2C(board.SCL, board.SDA)

macros = Macros()
encoder_handler = EncoderHandler()

keyboard.modules.append(encoder_handler)
keyboard.modules.append(macros)
keyboard.modules.append(Layers())

# Matrix Configuration (3x2 grid)
# Based on Schematic: 
# Columns: D6, D7, D8
# Rows: D10, D9
keyboard.col_pins = (board.D6, board.D7, board.D8)
keyboard.row_pins = (board.D10, board.D9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Rotary Encoder Rotation: D0, D1
encoder_handler.pins = ((board.D0, board.D1, None),)

# RGB Lighting: Pin D2, 7 Pixels
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

# Keymap: 6 Switches + 1 Encoder Button (D3)
# The Encoder Button is a separate trigger in this setup
# We use a scanner extension or manual mapping if not in matrix
# Since the matrix is 3x2, we have 6 keys. We'll add the encoder button as a 7th key.

keyboard.keymap = [
    [ # Layer 0: Default
        KC.MUTE,     KC.Macro(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL)), # Button 1, 2
        KC.Macro(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL)), KC.Macro(Press(KC.LCTRL), Tap(KC.X), Release(KC.LCTRL)), # Button 3, 4
        KC.MO(1),    KC.LT(2, KC.RGB_TOG), # Button 5, 6
        KC.PLAY_PAUSE # Encoder Button (D3 - mapping added via scanner)
    ],
    [ # Layer 1: Navigation/Macros
        KC.UNDO,     KC.REDO,
        KC.Macro(Press(KC.LGUI), Press(KC.LSHIFT), Tap(KC.S), Release(KC.LSHIFT), Release(KC.LGUI)), KC.SELECT_ALL,
        KC.TRNS,     KC.TRNS,
        KC.MUTE
    ],
    [ # Layer 2: RGB Control
        KC.RGB_MODE_PLAIN, KC.RGB_MODE_BREATHE,
        KC.RGB_MODE_RAINBOW, KC.RGB_MODE_SWIRL,
        KC.RGB_SAI, KC.RGB_SAD,
        KC.RGB_TOG
    ]
]

# Adding Encoder Button on D3 as extra key
keyboard.matrix_scanner = KeysScanner(
    pins=(board.D6, board.D7, board.D8, board.D10, board.D9, board.D3),
    # This scanner treats them as individual keys rather than a matrix for simplicity
    # but since schematic shows a matrix for 6 keys and a separate D3 for encoder:
)

# Refined Matrix Scanner to combine matrix + individual pin
# For simplicity with KMK, we'll use the MatrixScanner and add D3 to the sequence
# Or better: redefine matrix as 3x3 with dummy pins if needed, but a single scanner is cleaner.

# Wait, let's keep it simple: 6 keys in matrix, and use the encoder_handler for the button
encoder_handler.map = [
    [ (KC.VOLU, KC.VOLD) ], # Layer 0
    [ (KC.VOLU, KC.VOLD) ], # Layer 1
    [ (KC.RGB_HUI, KC.RGB_HUD) ] # Layer 2
]

# Initial Display
display.fill(0)
display.text('MACROPAD V1', 0, 10, 1)
display.show()

if __name__ == '__main__':
    keyboard.go()