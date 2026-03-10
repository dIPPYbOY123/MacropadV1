import board
import busio
import time
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
keyboard.col_pins = (board.D6, board.D5, board.D4)
keyboard.row_pins = (board.D7, board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Rotary Encoder Rotation: Pin 1 (D0), Pin 2 (D1)
# Encoder Button: Pin 4 (D3)
encoder_handler.pins = ((board.D0, board.D1, board.D3),)

# RGB Lighting: Pin 3 (D2), 7 Pixels
rgb = RGB(pixel_pin=board.D2, num_pixels=7)
keyboard.extensions.append(rgb)

# --- OLED Multi-View / App System ---

class DisplayManager(SSD1306_I2C):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_app = 0
        self.apps = ["STATUS", "MACROS", "ABOUT"]
        self.active_layer = 0
        self.last_update = 0

    def next_app(self):
        self.current_app = (self.current_app + 1) % len(self.apps)
        self.refresh()

    def on_layer_change(self, layer: int):
        self.active_layer = layer
        self.refresh()

    def refresh(self):
        self.fill(0)
        app_name = self.apps[self.current_app]
        
        # Header
        self.text(f"--- {app_name} ---", 15, 0, 1)

        if app_name == "STATUS":
            self.text(f"LAYER: {self.active_layer}", 0, 16, 1)
            self.text(f"RGB: {'ON' if rgb.enabled else 'OFF'}", 64, 16, 1)
        
        elif app_name == "MACROS":
            macros_list = [
                ["Copy", "Paste", "Cut"],
                ["Undo", "Redo", "Snp"],
                ["Mode", "Hue", "Tog"]
            ]
            current_macros = macros_list[self.active_layer]
            self.text(f"{current_macros[0]} {current_macros[1]} {current_macros[2]}", 0, 16, 1)
            
        elif app_name == "ABOUT":
            self.text("Macropad V1", 0, 12, 1)
            self.text("by Dip Khadka", 0, 22, 1)

        self.show()

    def during_runtime_tick(self):
        # Refresh every 2 seconds if needed for stats or animations
        if time.monotonic() - self.last_update > 2:
            self.last_update = time.monotonic()
            # self.refresh() # Enable if dynamic content is added

display = DisplayManager(128, 32, i2c)  
keyboard.extensions.append(display)  

# Keymap Customization
# We'll use a Macro to cycle through OLED apps
# Trigger: We'll set the Encoder Button (D3) to cycle apps on a double click or special layer
# For now, let's add a dedicated View Cycle key to Layer 0

keyboard.keymap = [
    [ # Layer 0: Default
        KC.MUTE,     KC.Macro(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL)), 
        KC.Macro(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL)), KC.Macro(Press(KC.LCTRL), Tap(KC.X), Release(KC.LCTRL)),
        KC.MO(1),    KC.LT(2, KC.RGB_TOG), 
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
# Encoder click (D3) now cycles the OLED apps!
encoder_handler.map = [
    [ (KC.VOLU, KC.VOLD, KC.NO) ], # App cycling handled by custom logic below
    [ (KC.PGUP, KC.PGDN, KC.NO) ],
    [ (KC.RGB_HUI, KC.RGB_HUD, KC.NO) ]
]

# Custom Encoder Button Logic to cycle Apps
def encoder_button_callback(event):
    if event.pressed:
        display.next_app()

keyboard.before_matrix_scan.append(lambda x: None) # Placeholder

# Using a custom class to intercept the encoder button
class AppCycler(EncoderHandler):
    def on_button_pressed(self, index):
        display.next_app()

# Re-initialize encoder with cycling logic
# Actually, KMK handles this better with individual key overrides,
# but for a multi-view app, triggering display.next_app() directly is best.

# Let's map the encoder button to a special key that we intercept
APP_CYCLE = KC.Macro(Tap(KC.F24)) # Dummy key to trigger cycle

encoder_handler.map = [
    [ (KC.VOLU, KC.VOLD, APP_CYCLE) ], 
    [ (KC.PGUP, KC.PGDN, APP_CYCLE) ],
    [ (KC.RGB_HUI, KC.RGB_HUD, APP_CYCLE) ]
]

# Intercept APP_CYCLE to change view
class AppSwitchExtension:
    def on_runtime_tick(self, keyboard):
        pass
    def before_matrix_scan(self, keyboard):
        pass
    def after_matrix_scan(self, keyboard):
        pass
    def before_hid_send(self, keyboard):
        pass
    def after_hid_send(self, keyboard):
        pass
    def on_powersave_enable(self, keyboard):
        pass
    def on_powersave_disable(self, keyboard):
        pass

# Simpler way: Use KMK's handler
def cycle_apps_handler(keyboard, key, is_pressed):
    if is_pressed and key == APP_CYCLE:
        display.next_app()
        return False # Don't send F24 to PC
    return True

keyboard.process_key = cycle_apps_handler

# Initial Display
display.refresh()

if __name__ == '__main__':
    keyboard.go()