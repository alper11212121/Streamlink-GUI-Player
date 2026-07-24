# Streamlink-GUI-Player
A lightweight dark-themed GUI for Streamlink
# 📺 Streamlink Dark GUI Player

A lightweight, dark-themed GUI player for **Streamlink** built with Python (Tkinter). Features 5 fully customizable quick-access favorite slots, multi-language support (English & Turkish), and seamless stream launching.

---

## ✨ Features
- 🌙 **Dark Mode GUI:** Modern, clean, and eye-friendly dark user interface.
- ⚡ **Quick Launch:** Paste a stream URL and press `Enter` to start watching instantly.
- ⭐️ **5 Quick Access Favorites:** Save your most-watched channels or streams and launch them with a single click.
- ⚙️ **In-App Preset Editor:** Easily update favorite button labels and URLs directly from the UI.
- 🔕 **Silent Execution:** Runs background processes cleanly without triggering extra CMD/console windows.
- 📁 **Clean Single Executable:** Stores user preferences safely in Windows AppData (`%APPDATA%`), keeping your workspace clutter-free.
- 🌐 **Multi-Language Support:** Includes both English and Turkish builds/source files.

---

## 📋 Prerequisites
Before using this player, ensure you have the following installed on your system:
- **Windows OS**
- **[Streamlink](https://streamlink.github.io/)**
- **[VLC Media Player](https://www.videolan.org/vlc/)** (or your default media player associated with Streamlink)

---

## 🚀 How to Run

### Option 1: Standalone `.exe` (Recommended)
1. Navigate to the **[Releases](../../releases)** section on the right panel.
2. Download your preferred language version:
   - `StreamlinkGUI.exe` (English)
   - `StreamlinkGUI_TR.exe` (Turkish / Türkçe)
3. Run the executable, paste a stream link, select quality, and press **Enter**!

### Option 2: Running from Source
```bash
# English Version
python StreamlinkGUI.py

# Turkish Version
python StreamlinkGUI_TR.py

MIT License

Copyright (c) 2026 Alper Bahçıvan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
