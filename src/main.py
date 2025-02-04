import socket
import machine
import network
import os
import time
import ntptime  # Module for obtaining time from NTP server

# Project Name
PROJECT_NAME = "netPowerSwitch"

# Initialize GPIO pin 6
led_pin = machine.Pin(6, machine.Pin.OUT)

# Define LED pins
red_led = machine.Pin(2, machine.Pin.OUT)
yellow_led = machine.Pin(3, machine.Pin.OUT)
green_led = machine.Pin(4, machine.Pin.OUT)

# Define the physical switch pin
switch_pin = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

# File to store settings
SETTINGS_FILE = "settings.txt"
SESSION_TIMEOUT = 3600  # 1 hour in seconds
NTP_SERVER = "pool.ntp.org"  # Default NTP server

# Default configuration
PASSWORD = "mypassword"
default_network_mode = "dhcp"
static_ip_config = {
    "ip": "192.168.1.100",
    "subnet": "255.255.255.0",
    "gateway": "192.168.1.1",
    "dns": "8.8.8.8"
}

# Track authenticated sessions
last_access_time = None

# Load settings from file
def load_settings():
    global PASSWORD, default_network_mode, static_ip_config, NTP_SERVER
    try:
        with open(SETTINGS_FILE, "r") as f:
            lines = f.readlines()
            PASSWORD = lines[0].strip()
            default_network_mode = lines[1].strip()
            static_ip_config["ip"] = lines[2].strip()
            static_ip_config["subnet"] = lines[3].strip()
            static_ip_config["gateway"] = lines[4].strip()
            static_ip_config["dns"] = lines[5].strip()
            if len(lines) > 6:
                NTP_SERVER = lines[6].strip()
            print("Settings loaded.")
    except (OSError, IndexError):
        print("Using default settings.")
        save_settings()

# Save settings to file
def save_settings():
    global PASSWORD, default_network_mode, static_ip_config, NTP_SERVER
    try:
        with open(SETTINGS_FILE, "w") as f:
            f.write(f"{PASSWORD}\n")
            f.write(f"{default_network_mode}\n")
            f.write(f"{static_ip_config['ip']}\n")
            f.write(f"{static_ip_config['subnet']}\n")
            f.write(f"{static_ip_config['gateway']}\n")
            f.write(f"{static_ip_config['dns']}\n")
            f.write(f"{NTP_SERVER}\n")
        print("Settings saved.")
    except OSError as e:
        print("Failed to save settings:", e)

# Check authentication session
def is_authenticated():
    global last_access_time
    if last_access_time is None:
        return False
    if time.time() - last_access_time > SESSION_TIMEOUT:
        last_access_time = None
        return False
    return True

# Update the last access time
def update_session():
    global last_access_time
    last_access_time = time.time()

# Synchronize time with NTP server
def synchronize_time():
    global NTP_SERVER
    try:
        ntptime.host = NTP_SERVER
        ntptime.settime()
        print("Time synchronized with NTP server.")
    except Exception as e:
        print("Failed to synchronize time:", e)

# Update LED states based on initialization and GPIO state
def update_led_states(initializing):
    if initializing:
        yellow_led.on()
        red_led.off()
        green_led.off()
    else:
        yellow_led.off()
        if led_pin.value():
            red_led.off()
            green_led.on()
        else:
            red_led.on()
            green_led.off()

# Handle the switch press to toggle GPIO state
def handle_switch():
    if not switch_pin.value():  # Switch is pressed
        time.sleep(0.1)  # Debounce delay
        if not switch_pin.value():  # Confirm switch press
            toggle_pin()

# Toggle the state of the GPIO pin
def toggle_pin():
    led_pin.value(not led_pin.value())
    update_led_states(False)

# Get the current state of the GPIO pin
def get_pin_state():
    return led_pin.value()

# Parse POST data
def parse_post_data(request):
    try:
        post_data = request.split("\r\n\r\n", 1)[1]
        data = dict(pair.split("=") for pair in post_data.split("&"))
        return data
    except Exception:
        return {}

# Load HTML templates
def load_html_template(template_name):
    try:
        with open(f"templates/{template_name}.html", "r") as f:
            return f.read()
    except OSError as e:
        print(f"Failed to load template {template_name}: {e}")
        return "<html><body><h1>Error Loading Page</h1></body></html>"

# Load static files like CSS
def load_static_file(filename):
    try:
        with open(f"templates/{filename}", "r") as f:
            return f.read()
    except OSError as e:
        print(f"Failed to load static file {filename}: {e}")
        return None

# Initialize the network connection
def initialize_network():
    nic = network.WIZNET5K(machine.SPI(0), machine.Pin(15), machine.Pin(14))
    nic.active(True)

    if default_network_mode == "dhcp":
        nic.ifconfig('dhcp')
        while not nic.isconnected():
            print("Waiting for network connection...")
    else:
        static_config = (
            static_ip_config["ip"],
            static_ip_config["subnet"],
            static_ip_config["gateway"],
            static_ip_config["dns"]
        )
        nic.ifconfig(static_config)
        print("Static network configured.")

    print("Network connected with IP:", nic.ifconfig()[0])
    return nic.ifconfig()[0]

# Start a simple web server
def start_server():
    global PASSWORD, default_network_mode, static_ip_config, NTP_SERVER
    load_settings()
    update_led_states(True)
    ip_address = initialize_network()
    synchronize_time()
    print("Server running at http://{}:80/".format(ip_address))
    update_led_states(False)

    # Create a socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)

    while True:
        handle_switch()  # Check switch state

        # Accept client connection
        cl, addr = s.accept()
        print('Client connected from', addr)
        try:
            # Receive request
            request = cl.recv(1024).decode('utf-8')
            print('Request:', request)

            if '/style.css' in request:
                css_content = load_static_file("style.css")
                if css_content:
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/css\r\n\r\n')
                    cl.send(css_content)
                else:
                    cl.send('HTTP/1.0 404 Not Found\r\n\r\n')
            elif not is_authenticated():
                if 'POST' in request and '/' in request:
                    post_data = parse_post_data(request)
                    if post_data.get('password') == PASSWORD:
                        update_session()
                        pin_state = get_pin_state()
                        state_text = 'ON' if pin_state else 'OFF'
                        button_class = 'on' if pin_state else 'off'
                        response = load_html_template("control").format(
                            button_class=button_class,
                            state=state_text
                        )
                    else:
                        response = load_html_template("login")
                else:
                    response = load_html_template("login")
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
            else:
                update_session()
                if '/toggle' in request:
                    toggle_pin()
                    pin_state = get_pin_state()
                    state_text = 'ON' if pin_state else 'OFF'
                    button_class = 'on' if pin_state else 'off'
                    response = load_html_template("control").format(
                        button_class=button_class,
                        state=state_text
                    )
                else:
                    pin_state = get_pin_state()
                    state_text = 'ON' if pin_state else 'OFF'
                    button_class = 'on' if pin_state else 'off'
                    response = load_html_template("control").format(
                        button_class=button_class,
                        state=state_text
                    )
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
        except Exception as e:
            print('Error:', e)
        finally:
            cl.close()

# Run the server
start_server()
