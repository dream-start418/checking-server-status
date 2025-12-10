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
    
    # PyInstaller options
    # Note: PyInstaller will automatically detect imports from server_status_checker.py
    options = [
        'server_status_checker_gui.py',  # Main script
        '--name=ServerStatusChecker',     # Name of the executable
        '--onefile',                      # Create a single executable file
        '--windowed',                     # No console window (GUI only)
        '--hidden-import=win10toast',     # Include win10toast
        '--hidden-import=requests',       # Include requests
        '--hidden-import=sqlite3',        # Include sqlite3
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
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()

