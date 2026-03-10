# MacropadV1

MacropadV1 is a custom-designed 6-key mechanical macropad featuring a rotary encoder, an OLED display, and vibrant RGB lighting. Powered by the Seeeduino Xiao (Cortex-M0+) and running the flexible KMK firmware, it's a powerful tool for productivity, gaming, and creative workflows.

![Macropad Render](media/Screenshot%202026-03-09%20at%2012.37.25%20PM.png)

## ✨ Features

- **6 Mechanical Switches**: Hot-swappable support for your favorite MX switches.
- **Rotary Encoder**: Smooth scrolling and volume control with a satisfying tactile click.
- **OLED Display (128x32)**: Real-time feedback on layers, status, and custom animations.
- **7 Addressable RGB LEDs**: Fully customizable underglow and per-key lighting effects.
- **Compact Design**: Ergonomic layout with a custom-designed 3D printable case.
- **KMK Firmware**: Easily customizable using Python—no complex compilation required.

## 🛠 Hardware Components

- **Controller**: [Seeeduino Xiao](https://www.seeedstudio.com/Seeeduino-XIAO-Arduino-Microcontroller-SAMD21-Cortex-M0+-p-4426.html) (SAMD21)
- **Keys**: 6x Mechanical Switches (MX Style)
- **Diodes**: 6x 1N4148 (SOD-123 or Through-hole)
- **Encoder**: EC11 Rotary Encoder with Push Button
- **Display**: 0.91" 128x32 I2C OLED
- **LEDs**: 7x SK6812 Mini-E addressable RGB LEDs
- **PCB**: Custom-designed 2-layer PCB

### Case Design
The project includes a custom 3D printable case designed for a sleek, low-profile look.

![Case Render](media/Screenshot%202026-03-09%20at%2012.38.25%20PM.png)

## 🖥 Firmware

MacropadV1 runs on **KMK Firmware**, a feature-rich keyboard firmware written in CircuitPython.

### Keymap Configuration
The default keymap includes dedicated layers for media control, macros (Copy/Paste/Save), and RGB lighting effects.

- **Layer 0**: Media controls, Copy/Paste/Cut macros, Screen Snipping.
- **Layer 1**: Navigation and Select All macros.
- **Layer 2**: RGB Lighting controls (Mode, Brightness, Color).

The rotary encoder is mapped to volume control by default.

## 🎨 PCB & Electronics

Designed in KiCad, the PCB ensures a clean and reliable build.

![PCB Layout](media/Screenshot%202026-03-09%20at%2010.18.53%20PM.png)
![Schematic](media/Screenshot%202026-03-09%20at%2010.20.10%20PM.png)

## 📂 Project Structure

- `firmware/`: KMK configuration (`main.py`)
- `pcb/`: KiCad project files
- `cad/`: 3D design files for the case (STLs/Step)
- `media/`: Project images and documentation assets

---
Designed by **Dip Khadka**
