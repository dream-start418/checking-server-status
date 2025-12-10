#!/usr/bin/env python3
"""
Server Status Checker - GUI Application
Monitors URLs and sends alerts when servers are down or fail.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
from server_status_checker import ServerStatusChecker


class ServerStatusCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Status Checker")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Check for win10toast availability
        self.check_notifications_available()
        
        # Initialize checker
        self.checker = ServerStatusChecker()
        self.monitoring = False
        self.monitoring_thread = None
        
        # Create GUI
        self.create_widgets()
        
        # Load URLs into listbox
        self.refresh_url_list()
        
        # Start auto-refresh if monitoring
        self.auto_refresh()
    
    def check_notifications_available(self):
        """Check if Windows notifications are available and show warning if not."""
        try:
            from win10toast import ToastNotifier
            # Test if it can be instantiated
            test_notifier = ToastNotifier()
        except ImportError:
            from tkinter import messagebox
            messagebox.showwarning(
                "Notifications Unavailable",
                "win10toast is not installed. Windows notifications will be disabled.\n\n"
                "To enable notifications, install it with:\n"
                "pip install win10toast\n\n"
                "Or if using a virtual environment:\n"
                "venv\\Scripts\\pip install win10toast"
            )
        except Exception as e:
            # Other errors (like pywin32 issues)
            from tkinter import messagebox
            messagebox.showwarning(
                "Notifications Unavailable",
                f"Windows notifications may not work properly.\n\n"
                f"Error: {e}\n\n"
                f"Try installing/reinstalling:\n"
                f"pip install --upgrade win10toast pywin32"
            )
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Server Status Monitor", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL Management Section
        url_frame = ttk.LabelFrame(main_frame, text="URL Management", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        # Add URL
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=(0, 5), sticky=(tk.W, tk.E))
        self.url_entry.bind('<Return>', lambda e: self.add_url())
        
        add_btn = ttk.Button(url_frame, text="Add URL", command=self.add_url)
        add_btn.grid(row=0, column=2, padx=(0, 5))
        
        remove_btn = ttk.Button(url_frame, text="Remove Selected", command=self.remove_url)
        remove_btn.grid(row=0, column=3)
        
        # URL List
        list_frame = ttk.Frame(url_frame)
        list_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.url_listbox = tk.Listbox(list_frame, height=6, yscrollcommand=scrollbar.set)
        self.url_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.url_listbox.yview)
        
        # Control Buttons Section
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_btn = ttk.Button(control_frame, text="Start Monitoring", 
                                    command=self.start_monitoring, width=20)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="Stop Monitoring", 
                                   command=self.stop_monitoring, width=20, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        check_once_btn = ttk.Button(control_frame, text="Check Once", 
                                   command=self.check_once, width=20)
        check_once_btn.grid(row=0, column=2)
        
        # Status indicator
        self.status_label = ttk.Label(control_frame, text="Status: Stopped", 
                                      foreground="gray")
        self.status_label.grid(row=0, column=3, padx=(20, 0))
        
        # Log/Status Display Section
        log_frame = ttk.LabelFrame(main_frame, text="Status Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, 
                                                  wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colors
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("info", foreground="blue")
        self.log_text.tag_config("warning", foreground="orange")
        
        # Clear log button
        clear_btn = ttk.Button(log_frame, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=1, column=0, pady=(10, 0))
    
    def log_message(self, message: str, tag: str = ""):
        """Add a message to the log display."""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear the log display."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def refresh_url_list(self):
        """Refresh the URL listbox with current URLs."""
        self.url_listbox.delete(0, tk.END)
        for url in self.checker.urls:
            self.url_listbox.insert(tk.END, url)
    
    def add_url(self):
        """Add a URL from the entry field."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
        
        if self.checker.add_url(url):
            self.url_entry.delete(0, tk.END)
            self.refresh_url_list()
            self.log_message(f"Added URL: {url}", "info")
        else:
            messagebox.showinfo("Info", f"URL already exists: {url}")
    
    def remove_url(self):
        """Remove selected URL from the list."""
        selection = self.url_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a URL to remove")
            return
        
        url = self.url_listbox.get(selection[0])
        if url in self.checker.urls:
            self.checker.urls.remove(url)
            self.checker.save_urls()
            self.refresh_url_list()
            self.log_message(f"Removed URL: {url}", "info")
    
    def check_urls_threaded(self):
        """Check all URLs in a separate thread."""
        if not self.checker.urls:
            self.log_message("No URLs to check. Please add URLs first.", "warning")
            return
        
        self.log_message(f"Checking {len(self.checker.urls)} URL(s)...", "info")
        
        for url in self.checker.urls:
            result = self.checker.check_url(url)
            self.checker.log_status(result)
            
            # Update GUI with result
            if result['status'] == 'success':
                status_msg = (f"✓ {url} - Status: {result['status']} | "
                            f"Code: {result['status_code']} | "
                            f"Time: {result['response_time']}s")
                self.log_message(status_msg, "success")
            else:
                status_msg = (f"✗ {url} - Status: {result['status']} | "
                            f"Code: {result['status_code'] or 'N/A'} | "
                            f"Time: {result['response_time'] or 'N/A'}s")
                if result['error_message']:
                    status_msg += f" | Error: {result['error_message']}"
                self.log_message(status_msg, "error")
                
                # Send notification
                self.checker.send_notification(
                    result['url'],
                    result['status'],
                    result['error_message']
                )
    
    def check_once(self):
        """Check all URLs once."""
        if not self.checker.urls:
            messagebox.showwarning("Warning", "Please add at least one URL first")
            return
        
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=self.check_urls_threaded, daemon=True)
        thread.start()
    
    def start_monitoring(self):
        """Start continuous monitoring."""
        if not self.checker.urls:
            messagebox.showwarning("Warning", "Please add at least one URL first")
            return
        
        if self.monitoring:
            return
        
        self.monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring...", foreground="green")
        
        self.log_message("Monitoring started (checking every 1 minute)", "info")
        
        # Start monitoring in separate thread
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        if not self.monitoring:
            return
        
        self.monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", foreground="gray")
        
        self.log_message("Monitoring stopped", "info")
    
    def monitoring_loop(self):
        """Main monitoring loop (runs in separate thread)."""
        while self.monitoring:
            # Check all URLs
            self.check_urls_threaded()
            
            # Wait 1 minute (60 seconds)
            for _ in range(60):
                if not self.monitoring:
                    break
                time.sleep(1)
            
            if self.monitoring:
                self.log_message("Waiting 1 minute until next check...", "info")
    
    def auto_refresh(self):
        """Auto-refresh function for status updates."""
        # This can be used for real-time updates if needed
        self.root.after(1000, self.auto_refresh)


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    app = ServerStatusCheckerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

