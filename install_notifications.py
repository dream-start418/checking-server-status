#!/usr/bin/env python3
"""
Helper script to install and verify win10toast for Windows notifications
"""

import subprocess
import sys

def install_win10toast():
    """Install win10toast package."""
    print("Installing win10toast...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "win10toast"])
        print("✓ win10toast installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install win10toast: {e}")
        return False

def verify_installation():
    """Verify that win10toast can be imported and used."""
    print("\nVerifying installation...")
    try:
        from win10toast import ToastNotifier
        notifier = ToastNotifier()
        print("✓ win10toast imported successfully")
        print("✓ ToastNotifier created successfully")
        
        # Try to show a test notification
        print("\nSending test notification...")
        notifier.show_toast(
            "Test Notification",
            "Windows notifications are working!",
            duration=3
        )
        print("✓ Test notification sent!")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print("\nTry installing manually:")
        print(f"  {sys.executable} -m pip install win10toast")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nTry reinstalling:")
        print(f"  {sys.executable} -m pip install --upgrade win10toast pywin32")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Windows Notifications Setup")
    print("=" * 60)
    print(f"\nUsing Python: {sys.executable}")
    print()
    
    # Check if already installed
    try:
        from win10toast import ToastNotifier
        print("✓ win10toast is already installed")
        verify_installation()
    except ImportError:
        print("✗ win10toast is not installed")
        print()
        response = input("Do you want to install it now? (y/n): ").strip().lower()
        if response == 'y':
            if install_win10toast():
                verify_installation()
        else:
            print("\nTo install manually, run:")
            print(f"  {sys.executable} -m pip install win10toast")

