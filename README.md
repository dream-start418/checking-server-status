# Server Status Checker

A Python application for monitoring server status and sending alerts when servers are down or fail. Designed for server management engineers.

## Features

- ✅ **GUI Application** - User-friendly graphical interface
- ✅ Monitor multiple URLs simultaneously
- ✅ Automatic status checking every 1 minute
- ✅ Save URLs to `urls.txt` file
- ✅ Log all checks to SQLite database (`status_log.db`)
- ✅ Windows 10/11 desktop notifications for failures
- ✅ Real-time status display with color-coded logs
- ✅ Command-line interface (also available)
- ✅ Tracks response times and error messages
- ✅ **Standalone .exe file** - No Python installation required for end users

## Installation

### Step 1: Install Python

Make sure you have Python 3.7 or higher installed. You can download it from [python.org](https://www.python.org/downloads/).

### Step 2: Create Virtual Environment (Recommended)

It's recommended to use a virtual environment to isolate project dependencies.

**On Windows (PowerShell):**
```powershell
# Navigate to project directory
cd D:\Work\Self\checking-server-status

# Create virtual environment
# Try 'python' first, if it doesn't work, use 'py' instead
python -m venv venv
# OR if python command not found:
py -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
# Navigate to project directory
cd D:\Work\Self\checking-server-status

# Create virtual environment
# Try 'python' first, if it doesn't work, use 'py' instead
python -m venv venv
# OR if python command not found:
py -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

**Note:** If you get "Python was not found" error, use `py` instead of `python`. The `py` launcher is the Python launcher for Windows and should work if Python is installed.

**Note:** If you get an execution policy error in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

Once the virtual environment is activated (you'll see `(venv)` in your prompt), install the required packages:

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

You can verify everything is working by running the GUI:
```bash
python server_status_checker_gui.py
```

Or the command-line version:
```bash
python server_status_checker.py
```

### Deactivating Virtual Environment

When you're done working, you can deactivate the virtual environment:
```bash
deactivate
```

**Note:** You'll need to activate the virtual environment each time you open a new terminal session to work on this project.

## Usage

### GUI Application (Recommended)

Run the graphical user interface:

```bash
python server_status_checker_gui.py
```

**GUI Features:**
- **Add URLs**: Enter a URL in the text field and click "Add URL"
- **Remove URLs**: Select a URL from the list and click "Remove Selected"
- **Start Monitoring**: Click "Start Monitoring" to begin automatic checks every 1 minute
- **Stop Monitoring**: Click "Stop Monitoring" to pause automatic checks
- **Check Once**: Click "Check Once" to manually check all URLs immediately
- **Status Log**: View real-time status updates with color-coded messages:
  - 🟢 Green = Success
  - 🔴 Red = Error/Failure
  - 🔵 Blue = Info messages
  - 🟠 Orange = Warnings

### Command-Line Interface

#### Interactive Mode

Run the script without arguments to enter interactive mode:

```bash
python server_status_checker.py
```

**Available Commands:**
- `add <url>` - Add a URL to monitor (e.g., `add https://example.com`)
- `list` - List all monitored URLs
- `remove <url>` - Remove a URL from monitoring
- `check` - Check all URLs once
- `start` - Start continuous monitoring (checks every 1 minute)
- `quit` - Exit the application

#### Command Line Mode

```bash
# Add a URL
python server_status_checker.py add https://example.com

# Check all URLs once
python server_status_checker.py check

# Start continuous monitoring
python server_status_checker.py start
```

## Building Executable (.exe file)

To create a standalone `.exe` file that doesn't require Python installation:

### Step 1: Install PyInstaller

Make sure PyInstaller is installed (it's in requirements.txt):

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

**Option A: Using the build script (Recommended)**

```bash
python build_exe.py
```

**Option B: Using PyInstaller directly**

```bash
pyinstaller --name=ServerStatusChecker --onefile --windowed server_status_checker_gui.py
```

### Step 3: Find Your Executable

After building, the executable will be located at:
```
dist\ServerStatusChecker.exe
```

You can now distribute this `.exe` file to anyone - they don't need Python installed!

**Note:** The first time you run the `.exe`, Windows Defender might show a warning. This is normal for unsigned executables. You can click "More info" and then "Run anyway".

### Windows Notifications in .exe File

The build script now properly includes all pywin32 dependencies needed for notifications. If notifications don't work in the .exe:

1. **Check Windows Notification Settings:**
   - Go to: Settings > System > Notifications & actions
   - Make sure notifications are enabled
   - Look for "ServerStatusChecker" in the list and enable it

2. **First Run:**
   - Windows may ask for permission to show notifications on first run
   - Click "Allow" when prompted

3. **Fallback:**
   - If toast notifications fail, the app will show a MessageBox as a fallback
   - This ensures you're always notified of server failures

## File Structure

- `server_status_checker.py` - Core checker module (used by both CLI and GUI)
- `server_status_checker_gui.py` - GUI application
- `build_exe.py` - Script to build .exe file
- `requirements.txt` - Python dependencies
- `urls.txt` - Stores all monitored URLs (created automatically)
- `status_log.db` - SQLite database with all status check logs

## Database Schema

The `status_logs` table contains:
- `id` - Auto-increment primary key
- `url` - The checked URL
- `status_code` - HTTP status code (if available)
- `response_time` - Response time in seconds
- `status` - Status: 'success', 'failed', 'timeout', 'connection_error', or 'error'
- `error_message` - Error details (if any)
- `timestamp` - When the check was performed

## Windows Notifications

When a server fails to respond or returns an error, a Windows 10/11 desktop notification will appear with:
- Alert title
- Server URL
- Error message

## Example Workflow

1. Run `python server_status_checker.py`
2. Type `add https://google.com` to add a URL
3. Type `add https://github.com` to add another URL
4. Type `list` to see all URLs
5. Type `start` to begin continuous monitoring
6. The application will check every 1 minute and send notifications on failures

## Troubleshooting

### Windows Notifications Not Working

If you see the warning: `"Warning: win10toast not available. Windows notifications will be disabled."`

**Solution 1: Install win10toast**

If using a virtual environment:
```bash
# Activate your virtual environment first
.\venv\Scripts\Activate.ps1  # PowerShell
# or
venv\Scripts\activate.bat    # Command Prompt

# Then install
pip install win10toast
```

If using system Python:
```bash
pip install win10toast
# or
py -m pip install win10toast
```

**Solution 2: Use the helper script**

Run the installation helper:
```bash
python install_notifications.py
```

This will:
- Check if win10toast is installed
- Install it if missing
- Verify it works with a test notification

**Solution 3: Verify installation**

Test if win10toast works:
```bash
py -c "from win10toast import ToastNotifier; ToastNotifier().show_toast('Test', 'Notifications work!')"
```

### Virtual Environment Issues

If you're using a virtual environment but packages aren't found:
1. Make sure the virtual environment is activated (you should see `(venv)` in your prompt)
2. Install packages while the venv is active: `pip install -r requirements.txt`
3. Run the script from the same terminal where the venv is activated

## Notes

- URLs without `http://` or `https://` will automatically use `https://`
- Request timeout is set to 10 seconds
- All logs are stored in SQLite database for historical analysis
- Press `Ctrl+C` to stop continuous monitoring
- Windows notifications require `win10toast` package to be installed
