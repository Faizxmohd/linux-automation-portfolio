#!/bin/bash
# Captures count of threads containing 'ora' every run and writes to a logfile with timestamp.

#Declaring the logfile and its path
LOGFILE="/var/log/ora_threads.log"

# Create the directory if it does not exist
mkdir -p "$(dirname "$LOGFILE")"
touch "$LOGFILE"
chmod 0644 "$LOGFILE"

# Capture timestamp and thread count
TIMESTAMP=$(/bin/date '+%Y-%m-%d %H:%M:%S')

# Use grep pattern [o]ra to avoid matching the grep command itself
THREAD_COUNT=$(/bin/ps -eLf | /bin/grep -i '[o]ra' | /usr/bin/wc -l)

# Write to logfile
echo "$TIMESTAMP | ora_threads_count=$THREAD_COUNT" >> "$LOGFILE"
