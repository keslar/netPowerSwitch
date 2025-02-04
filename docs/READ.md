# netPowerSwitch

`netPowerSwitch` is a Python-based web-controlled power switch built for the Raspberry Pi Pico. It allows you to control GPIO pins via a web interface, toggle GPIO states with a physical button, and configure network and authentication settings.

## Features
- Control GPIO pins through a web interface.
- Physical button to toggle GPIO states.
- Visual state indication with LEDs.
- NTP time synchronization.
- Network configuration (DHCP or static IP).
- User authentication with session management.
- Modular and extensible design.

## Setup

### Prerequisites
- A Raspberry Pi Pico.
- WIZnet Ethernet HAT for network connectivity.
- CircuitPython installed on the Pico.

### Installing CircuitPython
1. Download CircuitPython for Raspberry Pi Pico from the [CircuitPython website](https://circuitpython.org/).
2. Flash the downloaded `.uf2` file onto your Pico by holding down the `BOOTSEL` button while connecting it to your computer.

### Setting Up the Development Environment
1. Clone this repository or copy the source files to your project directory.
2. Download the Adafruit CircuitPython Bundle from [CircuitPython Libraries](https://circuitpython.org/libraries/).
3. Extract the bundle and copy the following libraries into the `lib/` directory of your Pico:
   - `adafruit_wiznet5k.mpy`
   - `adafruit_bus_device`
   - `adafruit_register`
   - `adafruit_requests.mpy`
4. Ensure the following structure:
   ```
   /lib/
       adafruit_wiznet5k.mpy
       adafruit_bus_device/
       adafruit_register/
       adafruit_requests.mpy
   ```

### Uploading Files to the Pico
1. Copy the following project files to the root of your Pico:
   - `main.py` (the main application script).
   - `templates/` (HTML and CSS templates).
   - `settings.txt` (optional, for initial settings).

2. Ensure the `templates/` directory contains:
   - `login.html`
   - `control.html`
   - `setup.html`
   - `style.css`

### Running the Project
1. Reset the Pico or disconnect and reconnect it to power.
2. The Pico will start the web server, accessible via the assigned IP address.
3. Open the IP address in a web browser to access the control interface.

## Usage
- Use the web interface to control the GPIO state.
- Configure network and password settings via the setup page.
- Monitor the LED indicators for state updates.
- Press the physical button to toggle the GPIO state.

## Dependencies
The following CircuitPython libraries are required:
- `adafruit_wiznet5k`
- `adafruit_bus_device`
- `adafruit_register`
- `adafruit_requests`
- `ntptime` (built-in)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

