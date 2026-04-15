import sys
import time

# Measure cpu_meter.py startup and first few iterations
profiling_data = []

start_time = time.time()

import psutil
time_after_import = time.time()

def display_cpu_usage():
    """Display real-time CPU usage monitor."""
    try:
        # Initialize CPU percent (first call, non-blocking)
        init_start = time.time()
        psutil.cpu_percent(interval=None)
        init_time = time.time() - init_start
        
        profiling_data.append(('psutil.cpu_percent init', init_time * 1000))
        
        # Show timing info
        print(f"Import time: {(time_after_import - start_time)*1000:.2f}ms")
        print(f"Init time: {init_time*1000:.2f}ms")
        print(f"Total startup: {(time.time() - start_time)*1000:.2f}ms\n")
        
        # First few iterations
        for i in range(3):
            iter_start = time.time()
            cpu_usage = psutil.cpu_percent(interval=0.1)
            iter_time = time.time() - iter_start
            print(f"Iteration {i+1}: {cpu_usage:.1f}% ({iter_time*1000:.2f}ms)")
        
        print("\n[Profiling complete - press Ctrl+C to continue to normal operation]")
        sys.exit(0)
        
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
