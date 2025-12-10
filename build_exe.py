#!/usr/bin/env python3
"""
Build script for creating .exe file using PyInstaller
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable file."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if spec file exists, use it for better pywin32 support
    spec_file = os.path.join(script_dir, 'ServerStatusChecker.spec')
    
    if os.path.exists(spec_file):
        print("Using ServerStatusChecker.spec for build...")
        print("This ensures win10toast and pywin32 are properly bundled.")
        options = [spec_file, '--clean']
    else:
        # Fallback to command-line options
        print("Building with command-line options...")
        options = [
            'server_status_checker_gui.py',  # Main script
            '--name=ServerStatusChecker',     # Name of the executable
            '--onefile',                      # Create a single executable file
            '--windowed',                     # No console window (GUI only)
            '--hidden-import=win10toast',     # Include win10toast
            '--hidden-import=win32api',      # pywin32 - Windows API
            '--hidden-import=win32gui',       # pywin32 - GUI functions
            '--hidden-import=win32con',        # pywin32 - Constants
            '--hidden-import=win32process',   # pywin32 - Process functions
            '--hidden-import=pywintypes',      # pywin32 - Python types
            '--collect-submodules=win32api',  # Collect all win32api submodules
            '--collect-submodules=win32gui',  # Collect all win32gui submodules
            '--hidden-import=requests',       # Include requests
            '--hidden-import=sqlite3',         # Include sqlite3
            '--hidden-import=server_status_checker',  # Include checker module
            '--clean',                        # Clean cache before building
        ]
    
    print("Building executable...")
    print("This may take a few minutes...")
    print(f"Working directory: {script_dir}")
    
    try:
        PyInstaller.__main__.run(options)
        print("\n" + "="*60)
        print("✓ Build completed successfully!")
        print("="*60)
        print(f"\nExecutable location:")
        print(f"  {os.path.join(script_dir, 'dist', 'ServerStatusChecker.exe')}")
        print(f"\nYou can now distribute this .exe file!")
        print("\nNote: If notifications don't work, check Windows notification settings:")
        print("  Settings > System > Notifications & actions")
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()

