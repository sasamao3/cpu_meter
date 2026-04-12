import tkinter as tk
from tkinter import ttk
import psutil
import threading
import json
import os

class CPUMeterApp:
    CONFIG_FILE = os.path.expanduser("~/.cpu_meter_config.json")
    
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Meter")
        self.root.configure(bg='#000000')
        self.root.minsize(307, 354)  # Prevent window from getting too small
        
        self.running = True
        self.update_thread = None
        self.is_topmost = False
        self.last_width = 400  # For font scaling detection
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#000000', foreground='#FFFFFF')
        style.configure('TFrame', background='#000000')
        style.configure('TCheckbutton', background='#000000', foreground='#FFFFFF')
        style.configure('TScale', background='#000000')
        
        # Configure progressbar color to green
        style.configure('green.Horizontal.TProgressbar', foreground='#06A77D', background='#06A77D')
        
        # Main frame with weight configuration for resizing
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        for i in range(8):
            main_frame.rowconfigure(i, weight=0)
        main_frame.rowconfigure(1, weight=1)  # CPU label expands
        
        # Title
        self.title_label = ttk.Label(main_frame, text="CPU Usage Monitor", 
                               font=("Arial", 14, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # CPU percentage label (with value and % symbol)
        cpu_frame = tk.Frame(main_frame, bg='#000000')
        cpu_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.cpu_label = tk.Label(cpu_frame, text="0", 
                                   font=("Arial", 48, "bold"), 
                                   foreground="#2E86AB", bg='#000000')
        self.cpu_label.pack(side=tk.LEFT)
        
        self.cpu_percent_label = tk.Label(cpu_frame, text="%", 
                                           font=("Arial", 24, "bold"), 
                                           foreground="#2E86AB", bg='#000000')
        self.cpu_percent_label.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=350, mode='determinate', style='green.Horizontal.TProgressbar')
        self.progress.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Monitoring...", 
                                     font=("Arial", 10))
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Always on Top Frame
        topmost_frame = ttk.Frame(main_frame)
        topmost_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        topmost_label = ttk.Label(topmost_frame, text="Always on Top:", font=("Arial", 9))
        topmost_label.pack(side=tk.LEFT)
        
        self.topmost_var = tk.BooleanVar(value=False)
        topmost_check = ttk.Checkbutton(topmost_frame, variable=self.topmost_var,
                                       command=self.toggle_topmost)
        topmost_check.pack(side=tk.LEFT, padx=5)
        
        # Transparency Frame
        transparency_frame = ttk.Frame(main_frame)
        transparency_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        transparency_label = ttk.Label(transparency_frame, text="Transparency:", 
                                      font=("Arial", 9))
        transparency_label.pack(side=tk.LEFT)
        
        self.transparency_var = tk.DoubleVar(value=100)
        transparency_slider = ttk.Scale(transparency_frame, from_=20, to=100, 
                                       variable=self.transparency_var,
                                       command=self.update_transparency,
                                       orient=tk.HORIZONTAL)
        transparency_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.transparency_value_label = ttk.Label(transparency_frame, text="100%", 
                                                 font=("Arial", 9), width=4)
        self.transparency_value_label.pack(side=tk.LEFT, padx=5)
        
        # Spacer
        spacer = ttk.Frame(main_frame, height=10)
        spacer.grid(row=6, column=0, columnspan=2)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Start/Stop button
        self.toggle_button = ttk.Button(button_frame, text="Stop", 
                                       command=self.toggle_monitoring)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        exit_button = ttk.Button(button_frame, text="Quit", 
                                command=self.on_closing)
        exit_button.pack(side=tk.LEFT, padx=5)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Load previous settings
        self.load_config()
        
        # Bind resize event for font scaling
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Start monitoring
        self.is_running = True
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start the CPU monitoring thread."""
        # Initialize CPU percent (non-blocking)
        psutil.cpu_percent(interval=None)
        
        self.is_running = True
        self.update_thread = threading.Thread(target=self.monitor_cpu, daemon=True)
        self.update_thread.start()
        self.toggle_button.config(text="Stop")
    
    def stop_monitoring(self):
        """Stop the CPU monitoring thread."""
        self.is_running = False
        self.toggle_button.config(text="Start")
    
    def toggle_monitoring(self):
        """Toggle between start and stop."""
        if self.is_running:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def toggle_topmost(self):
        """Toggle Always on Top."""
        self.is_topmost = self.topmost_var.get()
        self.root.attributes('-topmost', self.is_topmost)
    
    def update_transparency(self, value):
        """Update window transparency."""
        alpha = float(value) / 100
        self.root.attributes('-alpha', alpha)
        self.transparency_value_label.config(text=f"{int(float(value))}%")
    
    def on_window_resize(self, event):
        """Update font sizes when window is resized."""
        if event.widget == self.root:
            width = event.width
            # Only update if width actually changed significantly
            if abs(width - self.last_width) > 20:
                self.last_width = width
                self.update_font_sizes(width)
    
    def update_font_sizes(self, width):
        """Dynamically scale font sizes based on window width."""
        # Calculate font sizes proportional to window width
        # Base sizes at 400px width
        title_size = max(12, int((width - 40) / 400 * 14))
        cpu_size = max(36, int((width - 40) / 400 * 48))
        cpu_percent_size = max(18, int((width - 40) / 400 * 24))  # Half of cpu_size
        
        # Update fonts
        self.title_label.config(font=("Arial", title_size, "bold"))
        self.cpu_label.config(font=("Arial", cpu_size, "bold"))
        self.cpu_percent_label.config(font=("Arial", cpu_percent_size, "bold"))
    
    def monitor_cpu(self):
        """Monitor CPU usage in a separate thread."""
        try:
            while self.is_running and self.running:
                # Get CPU usage
                cpu_usage = psutil.cpu_percent(interval=0.5)
                
                # Validate value
                cpu_usage = max(0, min(100, cpu_usage))
                
                # Update GUI (thread-safe)
                self.root.after(0, self.update_gui, cpu_usage)
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(
                text=f"Error: {e}"))
    
    def update_gui(self, cpu_usage):
        """Update GUI with CPU usage data."""
        # Update percentage label (only the number)
        self.cpu_label.config(text=f"{cpu_usage:.1f}")
        
        # Update progress bar
        self.progress['value'] = cpu_usage
        
        # Update status with color coding
        if cpu_usage < 30:
            status = "Low"
            color = "#06A77D"
        elif cpu_usage < 70:
            status = "Medium"
            color = "#F77F00"
        else:
            status = "High"
            color = "#D62828"
        
        self.status_label.config(text=f"Status: {status}", foreground=color)
        self.cpu_label.config(foreground=color)
        self.cpu_percent_label.config(foreground=color)
    
    def on_closing(self):
        """Handle window closing."""
        self.running = False
        self.is_running = False
        self.save_config()
        self.root.destroy()
    
    def save_config(self):
        """Save window state to configuration file."""
        try:
            config = {
                "geometry": self.root.geometry(),
                "topmost": self.topmost_var.get(),
                "transparency": self.transparency_var.get()
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f)
            print(f"✓ Config saved: {config}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_config(self):
        """Load and apply previous window state."""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                print(f"✓ Config loaded: {config}")
                
                # Restore geometry
                if "geometry" in config:
                    self.root.geometry(config["geometry"])
                else:
                    self.root.geometry("400x300")
                
                # Restore Always on Top
                if "topmost" in config:
                    self.topmost_var.set(config["topmost"])
                    self.toggle_topmost()
                
                # Restore Transparency
                if "transparency" in config:
                    self.transparency_var.set(config["transparency"])
                    self.update_transparency(config["transparency"])
            else:
                print(f"✓ No previous config found, using defaults")
                self.root.geometry("400x300")
        except Exception as e:
            print(f"Error loading config: {e}")
            self.root.geometry("400x300")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUMeterApp(root)
    root.mainloop()
