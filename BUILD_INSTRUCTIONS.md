# Building the Executable

## Quick Build Guide

### Prerequisites
1. Make sure you have Python installed
2. Activate your virtual environment
3. Install dependencies: `pip install -r requirements.txt`

### Build Methods

#### Method 1: Using the Build Script (Easiest)

```bash
python build_exe.py
```

#### Method 2: Using PyInstaller Directly

```bash
pyinstaller --name=ServerStatusChecker --onefile --windowed server_status_checker_gui.py
```

#### Method 3: Using PyInstaller with More Options

```bash
pyinstaller ^
  --name=ServerStatusChecker ^
  --onefile ^
  --windowed ^
  --hidden-import=win10toast ^
  --hidden-import=requests ^
  --hidden-import=sqlite3 ^
  --clean ^
  server_status_checker_gui.py
```

### Output Location

After building, find your executable at:
```
dist\ServerStatusChecker.exe
```

### File Size

The executable will be approximately 15-25 MB (includes Python runtime and all dependencies).

### Distribution

You can distribute the `.exe` file to anyone - no Python installation required!

**Note:** Windows may show a security warning for unsigned executables. This is normal. Users can click "More info" → "Run anyway".

