#!/bin/bash

# Linux File Cleanup Script
# Removes files and empty directories older than the configured retention period.
# Supports dry-run mode:
# CLEANUP_DRY_RUN=1 ./linux_file_cleanup.sh

LOG_FILE="/var/log/file_cleanup.log"
TMP_DIR="/tmp"
BACKUP_DIR="/u01/app/backups"
RETENTION_DAYS=30
DRY_RUN="${CLEANUP_DRY_RUN:-0}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting cleanup (DRY_RUN=${DRY_RUN})..." >> "$LOG_FILE"

run_find() {
    local cmd="$1"

    if [ "$DRY_RUN" = "1" ]; then
        eval "$cmd -print"
    else
        eval "$cmd -delete"
    fi
}

# Clean files from /tmp older than the retention period.
# Stay within the same filesystem and exclude system-managed paths.
run_find "find '$TMP_DIR' -xdev -mindepth 1 \
-not -path '/tmp/systemd-private-*' \
-type f -mtime +${RETENTION_DAYS}"

# Clean empty directories from /tmp.
run_find "find '$TMP_DIR' -xdev -depth -mindepth 1 \
-not -path '/tmp/systemd-private-*' \
-type d -empty -mtime +${RETENTION_DAYS}"

# Clean aged backup files.
run_find "find '$BACKUP_DIR' -xdev -mindepth 1 \
-type f -mtime +${RETENTION_DAYS}"

# Clean aged empty backup directories.
run_find "find '$BACKUP_DIR' -xdev -depth -mindepth 1 \
-type d -empty -mtime +${RETENTION_DAYS}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleanup completed (DRY_RUN=${DRY_RUN})." >> "$LOG_FILE"
