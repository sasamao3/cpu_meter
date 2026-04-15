#!/usr/bin/env python
"""
Detailed startup performance analysis of cpu_meter.py
Tests different startup scenarios
"""
import sys
import time

print("=== CPU Meter Startup Analysis ===\n")

# Test 1: Just imports
test1_start = time.time()
import psutil
import time as time_module
import sys as sys_module
test1_time = time.time() - test1_start
print(f"Test 1 - All imports: {test1_time*1000:.2f}ms")

# Test 2: First cpu_percent call (cold)
test2_start = time.time()
psutil.cpu_percent(interval=None)
test2_time = time.time() - test2_start
print(f"Test 2 - First cpu_percent(interval=None): {test2_time*1000:.2f}ms")

# Test 3: Subsequent cpu_percent calls (warm)
print("\nWarm calls (0.1s interval):")
for i in range(3):
    test3_start = time.time()
    result = psutil.cpu_percent(interval=0.1)
    test3_time = time.time() - test3_start
    print(f"  Call {i+1}: {test3_time*1000:.2f}ms (CPU: {result:.1f}%)")

# Test 4: Fast calls (interval=0)
print("\nFast calls (no interval):")
for i in range(3):
    test4_start = time.time()
    result = psutil.cpu_percent(interval=0)
    test4_time = time.time() - test4_start
    print(f"  Call {i+1}: {test4_time*1000:.2f}ms (CPU: {result:.1f}%)")

print("\n=== RECOMMENDATIONS ===")
print("The slow part appears to be the 0.1s interval in each loop iteration.")
print("Consider:")
print("1. Using interval=0 for faster updates (non-blocking)")
print("2. Lazy-loading psutil only when needed")
print("3. Using a background thread for CPU monitoring")
