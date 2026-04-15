#!/usr/bin/env python
import subprocess
import time
import sys

# Measure actual process startup time
start = time.time()

# Start the process
proc = subprocess.Popen(
    ['/Users/mao/Documents/Dev/cpu_meter/venv_build/bin/python', 'cpu_meter.py'],
    cwd='/Users/mao/Documents/Dev/cpu_meter',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for first output
try:
    # Try to read first line of output
    while proc.poll() is None:
        # Check if process is running and has produced output
        if proc.stdout is not None or time.time() - start > 5:
            break
        time.sleep(0.01)
    
    elapsed = time.time() - start
    print(f"Process started and first output appeared in: {elapsed*1000:.2f}ms")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    proc.terminate()
    proc.wait(timeout=1)
