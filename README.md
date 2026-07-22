# Pi_VNC_KZLauncher

A fully GUI-based Windows app that launches a **TigerVNC Viewer** session
to your Raspberry Pi, adds a real **F11 fullscreen toggle**, and
**automatically closes itself** once the Pi goes offline.

## Why?

Most VNC viewers don't have a simple fullscreen hotkey, and none of them
close themselves when the remote machine shuts down. KZLauncher wraps
[TigerVNC Viewer](https://github.com/TigerVNC/tigervnc) — a free, open
source VNC client with no accounts or subscriptions required — and adds
both, all through a clean graphical interface with no console window.

## Features

- 🖥️ **F11** toggles true borderless fullscreen for TigerVNC Viewer
- 🔌 Automatically closes the viewer when the Pi stops responding to ping
  (e.g. when you shut it down)
- 🖱️ Fully GUI-based — no console window at all, just a small app window
- ⚙️ **Settings screen**: change the VNC viewer path, ping interval, fail
  threshold, and fullscreen hotkey without touching any code
- 🌗 **Dark / Light theme**, switchable anytime
- 💾 Remembers your last-used Raspberry Pi IP address between sessions
- 🛡️ Input validation on the IP/hostname field before it's ever passed to
  a subprocess
- 🔔 Checks GitHub Releases on startup and **notifies** you if a newer
  version is available (does not download or install anything
  automatically — you choose when and how to update)

## Requirements

- Windows
- Python 3 (only needed if running from source — not required if you use
  a built `.exe` / installer)
- [TigerVNC Viewer](https://github.com/TigerVNC/tigervnc) installed on your
  PC — free and open source, no account or subscription needed
- A VNC server running on your Raspberry Pi (e.g. TigerVNC server, RealVNC
  Server, etc.)

## Installation

### Option A: Installer / prebuilt .exe

Check the [Releases page](../../releases) for the latest installer or
portable `.exe`.

> **Note:** Since this is an independent open-source tool without a paid
> code-signing certificate, Windows SmartScreen or your antivirus may show
> an "Unknown publisher" warning the first time you run it. This is normal
> for small unsigned open-source utilities, not a sign of malware — you can
> inspect the full source code in this repository. Click "More info → Run
> anyway" if you trust the source.

You'll still need TigerVNC Viewer installed (see Requirements above).

### Option B: Run from source (Python)

1. Install Python 3 from [python.org](https://python.org) (check **"Add
   Python to PATH"** during setup).
2. Install the required packages:
   ```
   pip install pywin32 keyboard
   ```
3. Download `PI_VNC_KZLauncher.pyw` from this repo.
4. Double-click it, or run from cmd:
   ```
   pythonw PI_VNC_KZLauncher.pyw
   ```
   (`.pyw` files run without a console window on Windows.)

## Usage

1. Open the app. If TigerVNC Viewer isn't found at the default path, fix
   it from the Settings screen (gear icon).
2. Enter your Raspberry Pi's IP address (found on the Pi with
   `hostname -I`) and click **CONNECT**. The app remembers this IP for
   next time.
3. TigerVNC Viewer opens and connects. Press **F11** anytime to toggle
   fullscreen.
4. Click **DISCONNECT**, or just turn off the Pi — either way KZLauncher
   closes the VNC Viewer window automatically.

## Settings screen

Click the ⚙ icon on the Connect screen to configure:

| Setting | Description |
|---|---|
| VNC viewer path | Where TigerVNC Viewer is installed (browse button available) |
| Ping interval (seconds) | How often to check if the Pi is still online |
| Fail threshold | Consecutive failed pings before the Pi is considered offline |
| Fullscreen hotkey | Which key toggles fullscreen (default: F11) |
| Theme | Dark or Light |

Settings and your last-used IP are stored in `kzlauncher_config.json`,
created next to the app on first run.

## How it works

- Fullscreen is achieved by removing the window's borders and resizing it
  to cover the current monitor (a common "borderless fullscreen" trick),
  so it works independently of TigerVNC Viewer's own UI.
- The Pi's online status is checked via a simple ICMP ping loop in a
  background thread; after enough consecutive failures, the viewer
  process is terminated.
- On startup, the app checks the GitHub Releases API in the background
  (never blocking the UI) to see if a newer version exists. If so, it
  shows a small notification with a link to the release page — nothing
  is downloaded or installed without you clicking through to GitHub
  yourself.

## Reporting issues

Found a bug or have a feature idea? Please open an issue — this repo
has issue templates to help you include the right details:
[Open an issue](../../issues/new/choose)

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues and pull requests are welcome — this started as a small personal
tool, so there's plenty of room for improvement (Linux/macOS support,
connection history for multiple Pis, system tray support, etc.).
