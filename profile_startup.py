import sys
import time

# Measure total startup time
start_time = time.time()

# Measure import times
print("=== Startup Performance Analysis ===\n")

import_start = time.time()
import psutil
import_time = time.time() - import_start
print(f"psutil import time: {import_time*1000:.2f}ms")

import_start = time.time()
import time as time_module
import_time = time.time() - import_start
print(f"time import time: {import_time*1000:.2f}ms")

import_start = time.time()
import sys as sys_module
import_time = time.time() - import_start
print(f"sys import time: {import_time*1000:.2f}ms")

# Measure psutil.cpu_percent initialization
print("\n--- Initialization Operations ---")

init_start = time.time()
psutil.cpu_percent(interval=None)
init_time = time.time() - init_start
print(f"psutil.cpu_percent(interval=None): {init_time*1000:.2f}ms")

# Total startup time
total_time = time.time() - start_time
print(f"\n--- Total Time ---")
print(f"Total import + init time: {total_time*1000:.2f}ms")
