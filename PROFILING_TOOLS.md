# CPU Meter Profiling Tools

This directory contains several profiling scripts created for debugging startup performance.

## Available Tools

### 1. `profile_startup.py`
Basic Python startup profiling - measures import times
```bash
python profile_startup.py
```
Shows individual import times for psutil, time, and sys modules.

### 2. `analyze_startup.py`
Comprehensive performance analysis with multiple scenarios
```bash
python analyze_startup.py
```
Tests:
- All imports timing
- First cpu_percent call
- Warm calls with 0.1s interval
- Fast calls with 0 interval

Provides recommendations based on results.

### 3. `profile_cpu_meter.py`
Profiles actual cpu_meter.py execution
```bash
python profile_cpu_meter.py
```
Measures:
- Import time
- Initialization time
- First few iterations with real CPU readings

### 4. `measure_startup.py`
Subprocess-based process timing
```bash
python measure_startup.py
```
Measures actual system process startup from shell invocation.

## Quick Profiling Commands

```bash
# Time module imports
time python -c "import cpu_meter"

# Analyze startup in detail
python analyze_startup.py

# Compare optimization impact
python profile_cpu_meter.py
```

## Key Findings

From profiling analysis:
- **Import only**: 8-10ms
- **With psutil.cpu_percent(interval=0.1)**: 100-110ms per call
- **With psutil.cpu_percent(interval=0)**: <1ms per call

The 100ms comes from the intentional sleep in non-blocking interval calls.

## When to Re-profile

- After adding new imports
- When optimizing for different Python versions
- If building for different platforms
- When evaluating dependency changes
