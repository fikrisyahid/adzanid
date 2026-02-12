# Jadwal Sholat Indonesia

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

The application features three main tabs:
- **Jadwal** - Displays current time and today's prayer schedule
- **Pengaturan** - Configure city, audio file, theme, and startup options
- **Tentang** - Application information and credits

## Requirements

- Python 3.10 or higher
- PyQt6
- requests library

## Installation

### Windows (Standalone Executable)

1. Download `JadwalSholat-v1.0.0-windows.zip` from the [Releases page](https://github.com/fikrisyahid/adzanid/releases)
2. Extract the ZIP file
3. Run `Jadwal Sholat.exe`

No Python installation required!

### macOS / Linux (Run from Source)

Since pre-built executables are only available for Windows, macOS and Linux users need to run from source:

```bash
# Clone the repository
git clone https://github.com/fikrisyahid/adzanid.git
cd adzanid

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Building Your Own Executable (macOS/Linux)

If you want to create your own executable:

```bash
pip install pyinstaller
pyinstaller --name "Adzanid" --windowed --icon=assets/icon.png --add-data "assets:assets" main.py
```

> Copy the `assets` folder into the `dist/Adzanid` directory.

The executable will be in the `dist/` directory.


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

The executable will be created in the `dist/` directory.

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
