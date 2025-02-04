# Test Plan for netPowerSwitch

This document outlines the tests required to validate the functionality, performance, and reliability of the `netPowerSwitch` project. Each test is described with its objective, steps, and expected outcome.

## Test Categories

### 1. HTML Templates Tests
#### 1.1 Ensure All Templates Load Successfully
- **Objective**: Verify that all required HTML templates (`login.html`, `control.html`, `setup.html`) load without error.
- **Steps**:
  1. Start the web server.
  2. Navigate to the respective endpoints in a browser.
- **Expected Outcome**: The HTML pages render correctly without errors.

#### 1.2 Validate Template Placeholders
- **Objective**: Ensure dynamic placeholders like `{button_class}` or `{state}` are correctly replaced.
- **Steps**:
  1. Trigger GPIO state changes.
  2. Refresh the control page.
- **Expected Outcome**: The placeholders are replaced with the correct values.

### 2. Static File Handling
#### 2.1 Test `/style.css` Endpoint
- **Objective**: Ensure the `style.css` file is served correctly.
- **Steps**:
  1. Open `/style.css` in a browser.
- **Expected Outcome**: The CSS file loads correctly with the appropriate MIME type.

#### 2.2 Test Missing Static File
- **Objective**: Validate behavior when a static file is missing.
- **Steps**:
  1. Remove `style.css` from the `templates/` directory.
  2. Open `/style.css` in a browser.
- **Expected Outcome**: The server responds with a 404 error.

### 3. Authentication Tests
#### 3.1 Correct Password
- **Objective**: Verify authentication with the correct password.
- **Steps**:
  1. Enter the correct password on the login page.
- **Expected Outcome**: The user is granted access to the control page.

#### 3.2 Incorrect Password
- **Objective**: Verify authentication denial with an incorrect password.
- **Steps**:
  1. Enter an incorrect password on the login page.
- **Expected Outcome**: The user is denied access.

#### 3.3 Session Timeout
- **Objective**: Validate session expiration after inactivity.
- **Steps**:
  1. Authenticate with the correct password.
  2. Wait for the session timeout duration.
  3. Attempt to access the control page.
- **Expected Outcome**: The user is redirected to the login page.

### 4. Network Configuration Tests
#### 4.1 DHCP Mode
- **Objective**: Validate network initialization in DHCP mode.
- **Steps**:
  1. Set the network mode to DHCP in the setup page.
  2. Restart the device.
- **Expected Outcome**: The device obtains an IP address via DHCP.

#### 4.2 Static IP Configuration
- **Objective**: Verify static IP settings.
- **Steps**:
  1. Set static IP settings in the setup page.
  2. Restart the device.
- **Expected Outcome**: The device uses the configured static IP settings.

#### 4.3 Error Handling
- **Objective**: Test behavior with invalid network configurations.
- **Steps**:
  1. Enter invalid IP settings in the setup page.
  2. Restart the device.
- **Expected Outcome**: The device fails gracefully and logs an error.

### 5. GPIO and LED State Tests
#### 5.1 LED State on Initialization
- **Objective**: Validate LED states during initialization.
- **Steps**:
  1. Restart the device.
- **Expected Outcome**: The yellow LED is on during initialization, and red/green LEDs reflect the GPIO state afterward.

#### 5.2 Toggle GPIO
- **Objective**: Test GPIO state changes via the web interface and physical switch.
- **Steps**:
  1. Toggle the GPIO state from the web interface.
  2. Press the physical switch.
- **Expected Outcome**: The GPIO state toggles correctly.

### 6. Web Interface Tests
#### 6.1 Endpoint Functionality
- **Objective**: Validate functionality of all endpoints.
- **Steps**:
  1. Test `/`, `/setup`, `/toggle`, and `/style.css` endpoints in a browser.
- **Expected Outcome**: Each endpoint responds correctly.

#### 6.2 Invalid Requests
- **Objective**: Ensure the server handles invalid or malformed requests gracefully.
- **Steps**:
  1. Send invalid requests to the server.
- **Expected Outcome**: The server returns a 400 or 404 error.

### 7. Settings File Tests
#### 7.1 Load Settings
- **Objective**: Test loading of valid and invalid settings files.
- **Steps**:
  1. Provide a valid settings file and restart the device.
  2. Provide an invalid settings file and restart the device.
- **Expected Outcome**: The valid file loads correctly, and the invalid file triggers an error.

#### 7.2 Save Settings
- **Objective**: Ensure settings are saved correctly.
- **Steps**:
  1. Modify settings via the setup page.
  2. Restart the device.
- **Expected Outcome**: The changes persist after the restart.

### 8. NTP Synchronization Tests
#### 8.1 Successful Synchronization
- **Objective**: Test successful NTP synchronization.
- **Steps**:
  1. Connect the device to the internet.
  2. Check the device’s system time.
- **Expected Outcome**: The system time matches the NTP server time.

#### 8.2 Error Handling
- **Objective**: Validate behavior when the NTP server is unreachable.
- **Steps**:
  1. Disconnect the device from the internet.
  2. Attempt NTP synchronization.
- **Expected Outcome**: The device logs an error.

### 9. Error Handling Tests
#### 9.1 Missing Files
- **Objective**: Ensure the server handles missing files gracefully.
- **Steps**:
  1. Delete a template or static file.
  2. Access the corresponding endpoint.
- **Expected Outcome**: The server returns a 404 error.

#### 9.2 Hardware Failures
- **Objective**: Test behavior during hardware failures (e.g., GPIO initialization failure).
- **Steps**:
  1. Simulate hardware failure.
- **Expected Outcome**: The device logs an error and continues operation where possible.

## Instructions for Running Tests

### Prerequisites
- Ensure Python 3.x is installed on your machine.
- Install dependencies using:
  ```bash
  pip install requests
  ```

### Test Execution

1. **Navigate to the Project Directory**:
   Open a terminal and navigate to the project root directory:
   ```bash
   cd /path/to/netPowerSwitch
   ```

2. **Run All Tests**:
   Use the `unittest` module to discover and execute all test cases:
   ```bash
   python -m unittest discover -s tests -p "test_*.py"
   ```

3. **Run Specific Test Script**:
   Execute a specific test script directly:
   ```bash
   python tests/test_netpowerswitch.py
   ```

4. **Review Output**:
   Examine the terminal output for test results. Look for any failed or errored tests and debug as needed.

### Logging and Debugging
- Use logs to verify internal states and outputs during test execution.
- Check the server logs for detailed error messages during manual testing.

This test plan ensures comprehensive coverage of all functionality in the `netPowerSwitch` project.
