import psutil
import time
import sys

def display_cpu_usage_fast():
    """
    Display real-time CPU usage monitor with FAST mode.
    Uses interval=0 for maximum responsiveness (no CPU averaging).
    """
    try:
        # Initialize CPU percent (first call, non-blocking)
        psutil.cpu_percent(interval=0)
        
        while True:
            # Get CPU usage with no interval (instant, may be less accurate)
            cpu_usage = psutil.cpu_percent(interval=0)
            
            # Validate CPU usage value
            if cpu_usage < 0 or cpu_usage > 100:
                cpu_usage = 0
            
            # Clear the terminal screen using escape codes
            sys.stdout.write('\033[2J\033[H')
            sys.stdout.flush()
            
            # Create a simple visual bar
            bar_length = 20
            filled_length = int(bar_length * cpu_usage / 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            print("=== CPU Monitor (FAST MODE) ===")
            print(f"Usage: [{bar}] {cpu_usage:.1f}%")
            print("Press Ctrl+C to stop.")
            
            # Small delay to prevent excessive CPU usage from polling
            time.sleep(0.01)
            
    except ImportError:
        print("Error: psutil is not installed. Install it with: pip install psutil")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def display_cpu_usage_balanced():
    """
    Display real-time CPU usage monitor with BALANCED mode (default).
    Uses adaptive intervals for responsive startup and accurate readings.
    """
    try:
        # Initialize CPU percent (first call, non-blocking)
        psutil.cpu_percent(interval=0)
        
        update_count = 0
        
        while True:
            # First 3 updates use faster interval (0) for snappier UI response
            # After that, use 0.1s for CPU averaging
            interval = 0 if update_count < 3 else 0.1
            
            cpu_usage = psutil.cpu_percent(interval=interval)
            
            # Validate CPU usage value
            if cpu_usage < 0 or cpu_usage > 100:
                cpu_usage = 0
            
            # Clear the terminal screen using escape codes
            sys.stdout.write('\033[2J\033[H')
            sys.stdout.flush()
            
            # Create a simple visual bar
            bar_length = 20
            filled_length = int(bar_length * cpu_usage / 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            print("=== CPU Monitor (BALANCED MODE) ===")
            print(f"Usage: [{bar}] {cpu_usage:.1f}%")
            print("Press Ctrl+C to stop.")
            
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
    if len(sys.argv) > 1 and sys.argv[1] == "--fast":
        print("Starting CPU Monitor in FAST mode (updates every ~10ms)...")
        time.sleep(0.5)
        display_cpu_usage_fast()
    else:
        print("Starting CPU Monitor in BALANCED mode...")
        time.sleep(0.5)
        display_cpu_usage_balanced()
