# 🚗 Drift Dancer (Desktop Buddy)



A lightweight, cross-platform desktop buddy for car enthusiasts. Brings a drifting BMW directly to your desktop, complete with dynamic smoke particles, "Always on Top" functionality, and car culture memes. 

Built with Python and PyQt6 for maximum performance and perfect transparency across Windows, macOS, and Linux (including Ubuntu/Wayland).

<img src="./frames/frame_08.png" alt="drawing" style="width:200px;"/>

## ✨ Features
* **Cross-Platform:** Runs flawlessly on Windows 10/11, macOS, and Linux.
* **Wayland/X11 Support:** Bypasses strict Linux window managers to remain sticky across all virtual desktops.
* **Lightweight:** Low RAM and CPU footprint thanks to delta-time frame animation.
* **Custom UI:** Frosted glass text bubbles with car culture/drift memes.

## 🚀 How to Run from Source

1. Clone the repository:
   ```bash
   git clone [https://github.com/ac999/drift_dancer.git](https://github.com/ac999/drift_dancer.git)
   cd drift_dancer

```

2. Install the required dependencies:
```bash
pip install -r requirements.txt

```


3. Run the app:
```bash
python main.py

```



## 📦 How to Build Standalone Executables (Releases)

To build a standalone executable (`.exe`, `.app`, or Linux binary) so users don't need Python installed, use **PyInstaller**.

**For Windows:**

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "frames;frames" main.py

```

**For macOS / Linux:**

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "frames:frames" main.py

```

*Note the use of `:` instead of `;` for Unix-based systems.*

The compiled executable will be located in the `dist/` folder.

## ⌨️ Controls

* **Close App:** Press `Escape` while the application is focused.

