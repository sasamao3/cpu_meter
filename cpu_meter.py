import psutil
import time
import sys

def display_cpu_usage():
    """Display real-time CPU usage monitor."""
    try:
        # Initialize CPU percent (first call, non-blocking)
        psutil.cpu_percent(interval=None)
        
        while True:
            # Get CPU usage percentage (non-blocking for speed)
            cpu_usage = psutil.cpu_percent(interval=0.1)
            
            # Validate CPU usage value
            if cpu_usage < 0 or cpu_usage > 100:
                cpu_usage = 0
            
            # Clear the terminal screen using escape codes (faster than os.system)
            sys.stdout.write('\033[2J\033[H')
            sys.stdout.flush()
            
            # Create a simple visual bar
            bar_length = 20
            filled_length = int(bar_length * cpu_usage / 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            print("=== CPU Monitor ===")
            print(f"Usage: [{bar}] {cpu_usage:.1f}%")
            print("Press Ctrl+C to stop.")
            
    except ImportError:
        print("Error: psutil is not installed. Install it with: pip install psutil")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    display_cpu_usage()
