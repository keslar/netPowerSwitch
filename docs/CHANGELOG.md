
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - Initial Release

### Added
- GPIO control via web interface with on/off button.
- Dynamic serving of HTML templates (`login.html`, `control.html`, and `setup.html`).
- CSS styling with `style.css` served via the `/style.css` endpoint.
- Support for network configuration (DHCP and static IP).
- Authentication mechanism with session management.
- NTP synchronization for accurate time settings.
- LED indicators for system state (yellow for initialization, red/green for GPIO state).
- Physical switch for toggling GPIO state.
