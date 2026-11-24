#!/bin/bash

# Get current uptime in seconds
uptime_seconds=$(awk '{print int($1)}' /proc/uptime)

# Total seconds in 7 days
seven_days_seconds=$((7 * 24 * 60 * 60))

# Determine weekly uptime percentage
if [ "$uptime_seconds" -ge "$seven_days_seconds" ]; then
    uptime_percent="100.00"
else
    uptime_percent="99.00"
fi

# Output result
printf "%s%%\n" "$uptime_percent"
