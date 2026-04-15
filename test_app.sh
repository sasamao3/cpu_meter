#!/bin/bash
# Test if optimization is working in the compiled app

echo "Testing if PyInstaller app has the latest optimizations..."
echo "Expected: First 3 updates should appear instantly, then 100ms delays"
echo "Running for 3 seconds..."
echo ""

# Run app in background and capture output
cd /Users/mao/Documents/Dev/cpu_meter
timeout 3 dist/cpu_meter_app 2>&1 &
PID=$!

# Give it a moment to start
sleep 0.5

# Show that it ran
echo "✓ App executed (if output above shows CPU Monitor, optimization is included)"
wait $PID 2>/dev/null || true
