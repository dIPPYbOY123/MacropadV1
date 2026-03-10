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

keyboard.col_pins = (board.D7, board.D11)
keyboard.row_pins = (board.D0, board.D1, board.D8, board.D9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler.pins = ((board.D2, board.D3, None))

rgb = RGB(pixel_pin=board.D10, num_pixels=7)
keyboard.extensions.append(rgb)

class Display(SSD1306_I2C):
    def on_layer_change(self, layer: int):
        self.fill(0)
        self.text(f'M7R - {layer}', 0, 0, 1)
        self.show()

display = Display(128, 32, i2c)  
keyboard.extensions.append(display)  

keyboard.keymap = [
  [
    KC.MUTE, KC.Macro(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL)),
    KC.Macro(Press(KC.LCTRL), Tap(KC.X), Release(KC.LCTRL)), KC.Macro(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL)),
    KC.Macro(Press(KC.LALT), Press(KC.LSHIFT), Tap(KC.F), Release(KC.LSHIFT), Release(KC.LALT)), KC.Macro(Press(KC.LGUI), Tap(KC.PSCREEN), Release(KC.LGUI)),
    KC.MO(1), KC.LT(2, KC.RGB_TOG)
  ],
  [
    KC.MUTE, KC.MACRO(Press(KC.LCTRL), Tap(KC.A), Release(KC.LCTRL)),
    KC.MACRO(Press(KC.LCTRL), Tap(KC.S), Release(KC.LCTRL)), KC.Macro(Press(KC.LALT), Tap(KC.Tab), Release(KC.LALT)), 
    KC.Macro(Press(KC.LGUI), Press(KC.LSHIFT), Tap(KC.S), Release(KC.LSHIFT), Release(KC.LGUI)), KC.MEDIA_PREV_TRACK,
    KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK,
  ],
  [
    KC.KC.RGB_MODE_PLAIN, KC.RGB_MODE_BREATHE,
    KC.RGB_MODE_RAINBOW, KC.RGB_MODE_KNIGHT,
    KC.RGB_MODE_BREATHE_RAINBOW, KC.RGB_MODE_SWIRL,
    KC.RGB_SAI, KC.RGB_SAD,
  ]
]

encoder_handler.map = [
  [
    KC.VOLU, KC.VOLD
  ],
  [
    KC.VOLU, KC.VOLD
  ],
  [
    KC.RGB_HUI, KC.RGB_HUD
  ]
]

display.fill(0)
display.text('M7R', 0, 0, 1)
display.show()

if __name__ == '__main__':
    keyboard.go()