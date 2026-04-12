# CPU Meter

A sleek, real-time CPU monitoring application with a customizable GUI.

## Features

- 📊 **Real-time CPU Usage Monitoring** - Live CPU percentage display with visual progress bar
- 🎨 **Dark Theme** - Professional dark background with green progress indicator
- 🔝 **Always on Top** - Keep the window on top of other windows
- 👻 **Transparency Control** - Adjust window opacity from 20% to 100%
- 📐 **Responsive Design** - Dynamically scales text and UI elements with window resizing
- 💾 **State Persistence** - Saves window size, position, and settings on exit
- 🚀 **Standalone Executable** - Built with PyInstaller for easy distribution

## Installation & Usage

### Python Version
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python cpu_meter_gui.py
```

### macOS App Bundle
```bash
# Launch the built app
open dist/CPU\ Meter.app
```

## Requirements

- Python 3.10+
- tkinter (usually included with Python)
- psutil

## Building

To build a standalone macOS app:

```bash
pip install pyinstaller pillow
pyinstaller cpu_meter_gui.spec --clean -y
```

## Configuration

Settings are automatically saved to `~/.cpu_meter_config.json` when you quit the app.

## Controls

- **Always on Top**: Toggle window to stay on top of other applications
- **Transparency**: Adjust window opacity with the slider
- **Stop**: Pause CPU monitoring
- **Quit**: Close the application

## License

MIT
