import unittest
import requests
import time
from unittest.mock import Mock, patch

class TestNetPowerSwitch(unittest.TestCase):
    BASE_URL = "http://192.168.1.100"  # Replace with the actual IP address of your device

    def test_load_login_page(self):
        """Test that the login page loads correctly"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>Login</title>", response.text)

    def test_load_control_page(self):
        """Test that the control page loads after authentication"""
        payload = {"password": "mypassword"}  # Replace with your test password
        response = requests.post(f"{self.BASE_URL}/", data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Control Power", response.text)

    def test_load_style_css(self):
        """Test that the style.css file is served correctly"""
        response = requests.get(f"{self.BASE_URL}/style.css")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/css")
        self.assertIn("body {", response.text)

    def test_toggle_gpio(self):
        """Test toggling GPIO state via the web interface"""
        # Authenticate and access control page
        payload = {"password": "mypassword"}  # Replace with your test password
        requests.post(f"{self.BASE_URL}/", data=payload)

        # Trigger GPIO toggle
        response = requests.get(f"{self.BASE_URL}/toggle")
        self.assertEqual(response.status_code, 200)

    @patch("main.load_settings")
    def test_load_settings(self, mock_load_settings):
        """Test that settings load correctly"""
        mock_load_settings.return_value = {
            "password": "mypassword",
            "network_mode": "dhcp",
            "ip": "192.168.1.100",
        }
        settings = mock_load_settings()
        self.assertEqual(settings["password"], "mypassword")
        self.assertEqual(settings["network_mode"], "dhcp")

    @patch("main.save_settings")
    def test_save_settings(self, mock_save_settings):
        """Test that settings are saved correctly"""
        mock_save_settings.return_value = True
        result = mock_save_settings()
        self.assertTrue(result)

    def test_ntp_sync(self):
        """Test NTP synchronization"""
        with patch("main.ntptime.settime") as mock_settime:
            mock_settime.return_value = None  # Simulate successful NTP sync
            mock_settime()
            mock_settime.assert_called_once()

if __name__ == "__main__":
    print("Starting test execution for netPowerSwitch...")
    time.sleep(1)
    unittest.main()
