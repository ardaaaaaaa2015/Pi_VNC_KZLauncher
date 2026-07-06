"""
Pi_VNC_KZLauncher 1.4.0
================
Launches a VNC Viewer connected to a Raspberry Pi, toggles true fullscreen
with F11, and automatically closes itself once the Pi goes offline
(stops responding to ping).

SETUP (Windows, one-time):
    1) If Python isn't installed: get it from https://python.org
       (check "Add Python to PATH" during installation).
    2) Open a command prompt and run:
         pip install pywin32 keyboard

CONFIGURATION:
    Edit the "SETTINGS" section below to match your setup.

USAGE:
    Double-click this file, or run from cmd:
         python pi_vnc_launcher.py
"""

import subprocess
import threading
import time
import sys
import os

import win32gui
import win32con
import win32process
import win32api
import keyboard

# ============ SETTINGS (edit these for your setup) ============

# The Pi's IP address is no longer hardcoded here -- you'll be asked
# for it each time you run the script (see main()).
PI_IP = None

# Full path to the installed VNC Viewer executable
# (default install location for TigerVNC Viewer)
VNC_VIEWER_PATH = r"C:\Program Files\TigerVNC\vncviewer.exe"

# How often (in seconds) to check whether the Pi is still online
PING_INTERVAL_SEC = 3

# Number of consecutive failed pings before the Pi is considered "offline"
PING_FAIL_THRESHOLD = 4

# Hotkey used to toggle fullscreen
HOTKEY = "f11"

# ================================================================

_fullscreen_state = {"on": False, "old_style": None, "old_rect": None}
_stop_event = threading.Event()


def find_window_by_pid(pid):
    """Finds the visible top-level window belonging to the given process id."""
    result = []

    def _enum_handler(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid and win32gui.GetWindowText(hwnd):
            result.append(hwnd)

    win32gui.EnumWindows(_enum_handler, None)
    return result[0] if result else None


def toggle_fullscreen(pid):
    hwnd = find_window_by_pid(pid)
    if not hwnd:
        print("VNC Viewer window not found (it may not be open yet).")
        return

    if not _fullscreen_state["on"]:
        # Save the current style and position
        _fullscreen_state["old_style"] = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        _fullscreen_state["old_rect"] = win32gui.GetWindowRect(hwnd)

        # Strip window borders/title bar
        new_style = _fullscreen_state["old_style"] & ~(
            win32con.WS_CAPTION | win32con.WS_THICKFRAME |
            win32con.WS_MINIMIZEBOX | win32con.WS_MAXIMIZEBOX | win32con.WS_SYSMENU
        )
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)

        # Get the full size of the monitor the window is currently on
        monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
        mi = win32api.GetMonitorInfo(monitor)
        left, top, right, bottom = mi["Monitor"]

        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOP, left, top, right - left, bottom - top,
            win32con.SWP_FRAMECHANGED
        )
        _fullscreen_state["on"] = True
        print("Fullscreen ON")
    else:
        # Restore the previous style and position
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, _fullscreen_state["old_style"])
        l, t, r, b = _fullscreen_state["old_rect"]
        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOP, l, t, r - l, b - t,
            win32con.SWP_FRAMECHANGED
        )
        _fullscreen_state["on"] = False
        print("Fullscreen OFF")


def ping_ok(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "1000", ip],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def monitor_pi(proc):
    """Periodically pings the Pi; closes the VNC Viewer after repeated failures."""
    fail_count = 0
    while not _stop_event.is_set():
        time.sleep(PING_INTERVAL_SEC)

        if proc.poll() is not None:
            # User already closed the VNC window manually
            break

        if ping_ok(PI_IP):
            fail_count = 0
        else:
            fail_count += 1
            print(f"No response from Pi ({fail_count}/{PING_FAIL_THRESHOLD})")
            if fail_count >= PING_FAIL_THRESHOLD:
                print("Pi is offline/unreachable. Closing VNC Viewer...")
                try:
                    proc.terminate()
                except Exception:
                    pass
                break

    _stop_event.set()


def main():
    global PI_IP

    if not os.path.exists(VNC_VIEWER_PATH):
        print(f"ERROR: VNC Viewer not found at: {VNC_VIEWER_PATH}")
        print("Please fix the VNC_VIEWER_PATH setting at the top of this script.")
        sys.exit(1)

    entered_ip = input("Enter your Raspberry Pi's IP address (e.g. 192.168.1.100): ").strip()
    if not entered_ip:
        print("No IP address entered. Exiting.")
        sys.exit(1)
    PI_IP = entered_ip

    print(f"Connecting to {PI_IP}...")
    proc = subprocess.Popen([VNC_VIEWER_PATH, PI_IP])

    # F11 toggles fullscreen
    keyboard.add_hotkey(HOTKEY, lambda: toggle_fullscreen(proc.pid))
    print(f"Ready. Press '{HOTKEY.upper()}' to toggle fullscreen.")
    print("This program will close automatically once the Pi is turned off.")

    monitor_thread = threading.Thread(target=monitor_pi, args=(proc,), daemon=True)
    monitor_thread.start()

    # Wait until either the VNC window is closed or the Pi becomes unreachable
    while proc.poll() is None and not _stop_event.is_set():
        time.sleep(0.5)

    _stop_event.set()
    keyboard.unhook_all_hotkeys()
    print("Program terminated.")


if __name__ == "__main__":
    main()