# Adzanid - Jadwal Sholat Indonesia

<p align="center">
  <img src="assets/icon.png" alt="App Icon" width="128"/>
</p>

<p align="center">
  <strong>Desktop prayer times application for Indonesian cities</strong>
</p>

A simple, elegant desktop application built with Python and PyQt6 that displays real-time Islamic prayer schedules for major cities across Indonesia using the Aladhan API.

## Features

- 📅 **Real-Time Prayer Times** - Automatically fetches and displays today's prayer schedule (Subuh, Dzuhur, Ashar, Maghrib, Isya)
- 🕌 **100+ Indonesian Cities** - Covers all provincial capitals and major cities across Indonesia
- 🔔 **Audio Notifications** - Play adhan (call to prayer) at prayer times with customizable MP3 file
- 🎨 **Dark Mode** - Toggle between light and dark themes
- 💻 **System Tray Integration** - Minimize to system tray and receive prayer time notifications
- 🚀 **Auto-Start** - Run automatically at system startup (Windows, macOS, Linux)
- ⏰ **Live Clock** - Always-visible clock showing current time
- 🌐 **Multi-Platform** - Works on Windows, macOS, and Linux

## Screenshots

The application features three main tabs with light and dark theme support:

<table>
  <tr>
    <td align="center">
      <img src="assets/schedule_white.png" alt="Schedule Tab - Light Theme" width="200"/>
      <br/>
      <strong>Jadwal (Light)</strong>
      <br/>
      Prayer schedule display
    </td>
    <td align="center">
      <img src="assets/setting_white.png" alt="Settings Tab - Light Theme" width="200"/>
      <br/>
      <strong>Pengaturan (Light)</strong>
      <br/>
      Configuration options
    </td>
    <td align="center">
      <img src="assets/about_white.png" alt="About Tab - Light Theme" width="200"/>
      <br/>
      <strong>Tentang (Light)</strong>
      <br/>
      App information
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="assets/schedule_black.png" alt="Schedule Tab - Dark Theme" width="200"/>
      <br/>
      <strong>Jadwal (Dark)</strong>
      <br/>
      Prayer schedule display
    </td>
    <td align="center">
      <img src="assets/setting_black.png" alt="Settings Tab - Dark Theme" width="200"/>
      <br/>
      <strong>Pengaturan (Dark)</strong>
      <br/>
      Configuration options
    </td>
    <td align="center">
      <img src="assets/about_black.png" alt="About Tab - Dark Theme" width="200"/>
      <br/>
      <strong>Tentang (Dark)</strong>
      <br/>
      App information
    </td>
  </tr>
</table>

## Requirements

- Python 3.10 or higher
- PyQt6
- requests library

## Installation

### Windows (Standalone Executable)

1. Download and extract [Adzanid-Windows-v1.2.0.zip](https://github.com/fikrisyahid/adzanid/releases/download/v1.2.0/Adzanid-Windows-v1.2.0.zip)
2. **Windows SmartScreen Warning**: You may see a security warning
   - Click "More info"
   - Click "Run anyway"
   - This happens because the app isn't digitally signed (requires expensive certificate)
   - The app is safe - you can verify the source code on GitHub

3. Run `Adzanid.exe`

No Python installation required!

### macOS / Linux (Quick Installation)

Install Adzanid with a single command:

> [!IMPORTANT]
> Requires Python 3.10, 3.11, or 3.12 (not 3.13 or higher due to PyInstaller compatibility)

**Using curl:**
```bash
curl -fsSL https://raw.githubusercontent.com/fikrisyahid/adzanid/main/quick-install.sh | sudo -E bash
```

**Or using wget:**
```bash
wget -qO- https://raw.githubusercontent.com/fikrisyahid/adzanid/main/quick-install.sh | sudo -E bash
```

> [!TIP]
> If you're using conda or a virtual environment, the `-E` flag is **required** to preserve your Python environment. Without it, the script may not detect your Python 3.12 installation.

**What the installation does:**
- ✅ Validates Python installation and version
- ✅ Automatically installs system dependencies (python3-venv)
- ✅ Builds the application with all dependencies
- ✅ Installs to system directories:
  - **Linux**: `/opt/adzanid` with desktop entry
  - **macOS**: `/Applications/Adzanid.app`
- ✅ Creates command-line shortcut: `adzanid`
- ✅ Cleans up temporary files after installation

**After installation:**
- **Linux**: Find Adzanid in your application menu or run `adzanid` in terminal
- **macOS**: Find Adzanid in Applications folder or run `adzanid` in terminal

#### Alternative: Manual Installation

If you prefer to install manually from the cloned repository:

```bash
# Clone the repository
git clone https://github.com/fikrisyahid/adzanid.git
cd adzanid

# Make the install script executable
chmod +x install.sh

# Run the installation script with sudo -E (to preserve conda environment if active)
sudo -E ./install.sh
```

> [!TIP]
> The `-E` flag preserves environment variables. This is important if you're using conda or a virtual environment.

#### Alternative: Run from Source (Without Installation)

If you prefer to run without system installation:

```bash
# Clone the repository
git clone https://github.com/fikrisyahid/adzanid.git
cd adzanid

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Manual Build (Advanced Users)

If you want to build manually without installation:

```bash
# Ensure Python < 3.13
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller

# Build
pyinstaller --name "Adzanid" --windowed --icon=assets/icon.png --add-data "assets:assets" main.py

# Copy assets
cp -r assets dist/Adzanid/
```

The executable will be in the `dist/Adzanid/` directory.


## Uninstallation

### Windows

Simply delete the extracted `Adzanid` folder. If you enabled "Run at Startup", the app will automatically remove the startup entry when you close it.

### macOS / Linux

Uninstall Adzanid with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/fikrisyahid/adzanid/main/uninstall.sh | sudo bash
```

**Or using wget:**
```bash
wget -qO- https://raw.githubusercontent.com/fikrisyahid/adzanid/main/uninstall.sh | sudo bash
```

**Or from cloned repository:**
```bash
cd adzanid
chmod +x uninstall.sh
sudo ./uninstall.sh
```

> [!NOTE]
> The `--yes` flag automatically confirms the uninstallation when piping from curl/wget. When running the script directly, you'll be asked to confirm interactively.

**What the uninstallation removes:**
- ✅ Application files from `/opt/adzanid` (Linux) or `/Applications/Adzanid.app` (macOS)
- ✅ Command-line launcher from `/usr/local/bin/adzanid`
- ✅ Desktop entry (Linux only)
- ✅ User autostart entries (if enabled)

**User settings are preserved** and can be manually deleted if desired:
- **Linux**: `~/.config/Adzanid/`
- **macOS**: `~/Library/Application Support/Adzanid/` and `~/Library/Preferences/com.fikrisyahid.adzanid.plist`


## Usage

### Running the Application

```bash
python main.py
```

### First-Time Setup

1. **Select Your City** - Choose your city from the dropdown in the Settings tab
2. **Configure Audio** (Optional) - Browse and select your preferred adhan MP3 file
3. **Enable Features** (Optional):
   - Toggle Dark Mode for a darker theme
   - Enable "Minimize to Tray" to keep the app running in the background
   - Enable "Run at Startup" to launch automatically when your system boots

### Testing Audio

Click the "Test Suara Adzan" button in the Settings tab to preview your selected audio file.

## Project Structure

```
adzanid/
├── main.py                 # Application entry point
├── app/
│   ├── __init__.py
│   ├── constants.py        # App-wide constants and configuration
│   ├── services/          # Business logic services
│   │   ├── audio_service.py       # Audio playback
│   │   ├── prayer_time_service.py # API integration
│   │   ├── startup_service.py     # System startup management
│   │   └── theme_manager.py       # Theme switching
│   └── ui/                # User interface components
│       ├── main_window.py         # Main application window
│       ├── schedule_tab.py        # Prayer times display
│       ├── settings_tab.py        # User settings
│       ├── about_tab.py           # About information
│       └── system_tray.py         # System tray integration
└── assets/
    ├── icons.png          # Application icon
    └── adhan.mp3          # Default adhan audio
```

## API Reference

This application uses the [Aladhan API](https://aladhan.com/prayer-times-api) to fetch prayer times. The API is free and does not require authentication.

## Platform-Specific Notes

### Windows
- Uses Windows Registry for startup management
- System tray icon works out of the box

### macOS
- Creates LaunchAgent plist for startup management
- May need to grant permissions for notifications

### Linux
- Creates `.desktop` file in `~/.config/autostart/` for startup
- System tray support depends on your desktop environment

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Credits

- **Developer**: Fikri Syahid
- **Prayer Times API**: [Aladhan](https://aladhan.com/)
- **Framework**: [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)

## Acknowledgments

Special thanks to the Aladhan team for providing the free prayer times API that powers this application.

---

<p align="center">Made with ❤️ for the Muslim community in Indonesia</p>
