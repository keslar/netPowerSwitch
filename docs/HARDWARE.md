# Hardware Setup

This document outlines the necessary hardware and how to connect it for the `netPowerSwitch` project.

## Required Hardware

1. **Raspberry Pi Pico**
   - The microcontroller used to run the `netPowerSwitch` project.

2. **WIZnet W5500 Ethernet HAT (WIZnet5K)**
   - Provides Ethernet connectivity for the Pico.
   - Interfaces via SPI.

3. **SKU21277 Relay HAT**
   - Controls power to external devices using GPIO signals.
   - Stackable design for seamless integration.

4. **Miscellaneous Components**
   - Micro USB cable (for power and programming).
   - Ethernet cable (for network connectivity).

## Connection Setup

The components are designed to stack together. Follow these steps to assemble the hardware:

1. **Bottom: SKU21277 Relay HAT**
   - Place the relay HAT at the bottom of the stack.
   - Ensure the relay HAT is correctly oriented with its GPIO pins aligned with the Raspberry Pi Pico.

2. **Middle: Raspberry Pi Pico**
   - Mount the Pico onto the relay HAT.
   - Ensure the Pico’s GPIO pins are fully seated into the relay HAT’s header.
   - The Pico should have CircuitPython pre-installed.

3. **Top: WIZnet W5500 Ethernet HAT**
   - Stack the WIZnet HAT on top of the Pico.
   - Ensure the SPI pins (SCK, MISO, MOSI) and power connections align with the Pico.

## Wiring Notes

- **Power**: The stack can be powered via the Pico’s micro USB port.
- **SPI Communication**: The WIZnet HAT communicates with the Pico using SPI (pins `GP2` to `GP6` by default).
- **GPIO Control**: The relay HAT uses GPIO pins from the Pico to control the relays.
  - GPIO 6 is configured as the main control pin for this project.

## Final Check

1. Verify the stack is securely connected.
2. Ensure no pins are bent or misaligned.
3. Connect the Ethernet cable to the WIZnet HAT.
4. Power the stack using a micro USB cable connected to the Pico.

Your hardware is now ready to use with the `netPowerSwitch` project!

