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

### Windows Notifications in .exe

The build script now properly includes all pywin32 dependencies needed for notifications. If notifications still don't work after building:

1. **Check Windows Notification Settings:**
   - Go to: Settings > System > Notifications & actions
   - Make sure notifications are enabled
   - Look for "ServerStatusChecker" or "Python" in the list and enable it

2. **First Run:**
   - The first time the .exe runs, Windows may ask for permission to show notifications
   - Click "Allow" when prompted

3. **Test Notifications:**
   - Add a test URL that will fail (e.g., `http://invalid-url-test-12345.com`)
   - Start monitoring and wait for it to fail
   - You should see a Windows notification

4. **If Still Not Working:**
   - The app will fall back to a MessageBox if toast notifications fail
   - Check Windows Event Viewer for any errors

