import psutil
import time
import sys

def display_cpu_usage():
    """Display real-time CPU usage monitor with optimized startup."""
    try:
        # Initialize CPU percent (first call, non-blocking)
        # Use interval=0 for instant response, then switch to 0.1 for smoother updates
        psutil.cpu_percent(interval=0)
        
        update_count = 0
        
        while True:
            # First 3 updates use faster interval (0) for snappier UI response
            # After that, use 0.1s for CPU averaging
            interval = 0 if update_count < 3 else 0.1
            
            cpu_start = time.time()
            cpu_usage = psutil.cpu_percent(interval=interval)
            cpu_elapsed = time.time() - cpu_start
            
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
            sys.stdout.flush()
            
            update_count += 1
            
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
