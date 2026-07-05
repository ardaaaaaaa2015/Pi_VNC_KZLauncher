# Pi_VNC_KZLauncher

A tiny Windows helper that launches a VNC Viewer session to your Raspberry Pi,
adds a real **F11 fullscreen toggle**, and **automatically closes itself**
once the Pi goes offline.

## Why?

Most VNC viewers don't have a simple fullscreen hotkey, and none of them
close themselves when the remote machine shuts down. This script wraps
your VNC viewer of choice and adds both.

## Features

- 🖥️ **F11** toggles true borderless fullscreen (works with any VNC viewer,
  not tied to a specific client's own shortcuts)
- 🔌 Automatically closes the viewer when the Pi stops responding to ping
  (e.g. when you shut it down)
- ⌨️ Asks for the Pi's IP address at startup — nothing hardcoded, nothing to
  edit for day-to-day use

## Requirements

- Windows
- Python 3
- A VNC viewer installed on your PC (tested with
  [TigerVNC Viewer](https://github.com/TigerVNC/tigervnc), free and open source)
- A VNC server running on your Raspberry Pi (e.g. TigerVNC server, RealVNC
  Server, etc.)

## Installation

1. Install Python 3 from [python.org](https://python.org) (check **"Add
   Python to PATH"** during setup).
2. Install the required packages:
pip install pywin32 keyboard
3. Download `pi_vnc_launcher.py` from this repo.
4. Open the script and check the `VNC_VIEWER_PATH` setting near the top
   points to your VNC viewer's `.exe` (default assumes TigerVNC Viewer).

## Usage

Run the script:
python pi_vnc_launcher.py
You'll be asked for your Raspberry Pi's IP address (find it on the Pi with
`hostname -I`). The VNC viewer opens automatically. Press **F11** at any
time to toggle fullscreen. When the Pi is turned off or becomes
unreachable, the viewer closes itself automatically.

## Configuration

All settings live at the top of `pi_vnc_launcher.py`:

| Setting | Description | Default |
|---|---|---|
| `VNC_VIEWER_PATH` | Path to your VNC viewer executable | `C:\Program Files\TigerVNC\vncviewer.exe` |
| `PING_INTERVAL_SEC` | How often to check if the Pi is alive | `3` |
| `PING_FAIL_THRESHOLD` | Consecutive failed pings before closing | `4` |
| `HOTKEY` | Fullscreen toggle key | `f11` |

## How it works

- Fullscreen is achieved by removing the window's borders and resizing it
  to cover the current monitor (a common "borderless fullscreen" trick),
  so it works regardless of what fullscreen support the VNC viewer itself
  has.
- The Pi's online status is checked via a simple ICMP ping loop in a
  background thread; after enough consecutive failures, the viewer
  process is terminated.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues and pull requests are welcome — this started as a small personal
tool, so there's plenty of room for improvement (Linux/macOS support,
a config file, systemd-style auto-start, etc.).
