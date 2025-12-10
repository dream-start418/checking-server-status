#!/usr/bin/env python3
"""
Server Status Checker
Monitors URLs and sends alerts when servers are down or fail.
"""

import requests
import time
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import List, Dict, Optional
try:
    from win10toast import ToastNotifier
    WINDOWS_NOTIFICATIONS_AVAILABLE = True
except ImportError as e:
    WINDOWS_NOTIFICATIONS_AVAILABLE = False
    # Only show warning if running from command line (not GUI)
    import sys
    if not sys.argv[0].endswith('server_status_checker_gui.py'):
        print(f"Warning: win10toast not available. Windows notifications will be disabled.")
        print(f"Install it with: pip install win10toast")
        print(f"Or run: python install_notifications.py")
        print(f"Error details: {e}")


class ServerStatusChecker:
    def __init__(self, urls_file: str = "urls.txt", db_file: str = "status_log.db"):
        self.urls_file = Path(urls_file)
        self.db_file = Path(db_file)
        self.urls: List[str] = []
        self.session = requests.Session()
        self.session.timeout = 10  # 10 second timeout
        
        # Initialize database
        self._init_database()
        
        # Initialize Windows notifier
        if WINDOWS_NOTIFICATIONS_AVAILABLE:
            self.notifier = ToastNotifier()
        else:
            self.notifier = None
        
        # Load URLs
        self.load_urls()
    
    def _init_database(self):
        """Initialize SQLite database for logging."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create table for status logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                status_code INTEGER,
                response_time REAL,
                status TEXT NOT NULL,
                error_message TEXT,
                timestamp DATETIME NOT NULL
            )
        ''')
        
        # Create index on timestamp for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON status_logs(timestamp)
        ''')
        
        conn.commit()
        conn.close()
    
    def load_urls(self):
        """Load URLs from urls.txt file."""
        if self.urls_file.exists():
            with open(self.urls_file, 'r', encoding='utf-8') as f:
                self.urls = [line.strip() for line in f if line.strip()]
            print(f"Loaded {len(self.urls)} URL(s) from {self.urls_file}")
        else:
            print(f"No {self.urls_file} file found. Please add URLs first.")
    
    def add_url(self, url: str):
        """Add a URL to the list and save to file."""
        url = url.strip()
        if not url:
            return False
        
        # Add http:// if no scheme is provided
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if url not in self.urls:
            self.urls.append(url)
            self.save_urls()
            print(f"Added URL: {url}")
            return True
        else:
            print(f"URL already exists: {url}")
            return False
    
    def save_urls(self):
        """Save URLs to urls.txt file."""
        with open(self.urls_file, 'w', encoding='utf-8') as f:
            for url in self.urls:
                f.write(url + '\n')
    
    def check_url(self, url: str) -> Dict:
        """Check a single URL and return status information."""
        start_time = time.time()
        result = {
            'url': url,
            'status_code': None,
            'response_time': None,
            'status': 'unknown',
            'error_message': None,
            'timestamp': datetime.now()
        }
        
        try:
            response = self.session.get(url, timeout=10)
            response_time = time.time() - start_time
            
            result['status_code'] = response.status_code
            result['response_time'] = round(response_time, 3)
            
            if response.status_code == 200:
                result['status'] = 'success'
            else:
                result['status'] = 'failed'
                result['error_message'] = f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            result['error_message'] = 'Request timeout (10s)'
            result['response_time'] = round(time.time() - start_time, 3)
            
        except requests.exceptions.ConnectionError:
            result['status'] = 'connection_error'
            result['error_message'] = 'Connection failed'
            result['response_time'] = round(time.time() - start_time, 3)
            
        except requests.exceptions.RequestException as e:
            result['status'] = 'error'
            result['error_message'] = str(e)
            result['response_time'] = round(time.time() - start_time, 3)
        
        return result
    
    def log_status(self, result: Dict):
        """Log status check result to database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO status_logs 
            (url, status_code, response_time, status, error_message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            result['url'],
            result['status_code'],
            result['response_time'],
            result['status'],
            result['error_message'],
            result['timestamp']
        ))
        
        conn.commit()
        conn.close()
    
    def send_notification(self, url: str, status: str, error_message: Optional[str] = None):
        """Send Windows notification for failed checks."""
        if not self.notifier:
            return
        
        title = "Server Status Alert"
        if status in ['timeout', 'connection_error', 'error', 'failed']:
            message = f"Server failed: {url}"
            if error_message:
                message += f"\nError: {error_message}"
            
            try:
                # Try to send notification
                self.notifier.show_toast(
                    title,
                    message,
                    duration=10,
                    threaded=True
                )
            except Exception as e:
                # If notification fails in bundled exe, try alternative method
                try:
                    # Try using win32api directly as fallback
                    import win32api
                    import win32con
                    win32api.MessageBox(
                        0,
                        message,
                        title,
                        win32con.MB_OK | win32con.MB_ICONWARNING
                    )
                except:
                    # If all else fails, just log it (silent failure)
                    pass
    
    def check_all_urls(self):
        """Check all URLs and log results."""
        if not self.urls:
            print("No URLs to check. Please add URLs first.")
            return
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking {len(self.urls)} URL(s)...")
        
        for url in self.urls:
            result = self.check_url(url)
            self.log_status(result)
            
            # Print status
            status_icon = "✓" if result['status'] == 'success' else "✗"
            print(f"  {status_icon} {url}")
            print(f"    Status: {result['status']} | "
                  f"Code: {result['status_code'] or 'N/A'} | "
                  f"Time: {result['response_time'] or 'N/A'}s")
            
            if result['error_message']:
                print(f"    Error: {result['error_message']}")
            
            # Send notification if failed
            if result['status'] != 'success':
                self.send_notification(
                    result['url'],
                    result['status'],
                    result['error_message']
                )
    
    def run_continuous(self, interval_minutes: int = 1):
        """Run continuous monitoring with specified interval."""
        interval_seconds = interval_minutes * 60
        
        print(f"\nStarting continuous monitoring (checking every {interval_minutes} minute(s))...")
        print("Press Ctrl+C to stop.\n")
        
        try:
            while True:
                self.check_all_urls()
                print(f"\nWaiting {interval_minutes} minute(s) until next check...\n")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user.")


def interactive_mode():
    """Interactive mode for adding URLs."""
    checker = ServerStatusChecker()
    
    print("=" * 60)
    print("Server Status Checker - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  add <url>     - Add a URL to monitor")
    print("  list          - List all URLs")
    print("  remove <url>  - Remove a URL")
    print("  check         - Check all URLs once")
    print("  start         - Start continuous monitoring (every 1 minute)")
    print("  quit          - Exit")
    print("\n" + "=" * 60 + "\n")
    
    while True:
        try:
            command = input("> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                print("Goodbye!")
                break
            
            elif command == 'list':
                if checker.urls:
                    print("\nMonitored URLs:")
                    for i, url in enumerate(checker.urls, 1):
                        print(f"  {i}. {url}")
                else:
                    print("No URLs added yet.")
                print()
            
            elif command.startswith('add '):
                url = command[4:].strip()
                checker.add_url(url)
            
            elif command.startswith('remove '):
                url = command[7:].strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                if url in checker.urls:
                    checker.urls.remove(url)
                    checker.save_urls()
                    print(f"Removed URL: {url}")
                else:
                    print(f"URL not found: {url}")
            
            elif command == 'check':
                checker.check_all_urls()
                print()
            
            elif command == 'start':
                checker.run_continuous(interval_minutes=1)
                break
            
            else:
                print("Unknown command. Type 'quit' to exit.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        checker = ServerStatusChecker()
        
        if sys.argv[1] == 'add' and len(sys.argv) > 2:
            checker.add_url(sys.argv[2])
        elif sys.argv[1] == 'check':
            checker.check_all_urls()
        elif sys.argv[1] == 'start':
            checker.run_continuous(interval_minutes=1)
        else:
            print("Usage:")
            print("  python server_status_checker.py              # Interactive mode")
            print("  python server_status_checker.py add <url>    # Add URL")
            print("  python server_status_checker.py check        # Check once")
            print("  python server_status_checker.py start         # Start monitoring")
    else:
        # Interactive mode
        interactive_mode()

