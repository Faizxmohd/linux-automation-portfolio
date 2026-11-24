#!/usr/bin/env python3

"""Monitor a private password input file and run an Ansible playbook.

Expected private input format:

    server01.example.com PasswordValue
    server02.example.com PasswordValue

The input and generated CSV files must never be committed to Git.
"""

import csv
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

from inotify_simple import INotify, flags


SCRIPT_DIR = Path(__file__).resolve().parent

INPUT_FILE = SCRIPT_DIR / "inp_passwords.txt"
CSV_FILE = SCRIPT_DIR / "passwd.csv"
PLAYBOOK_FILE = SCRIPT_DIR / "root_password_reset.yml"
LOG_FILE = SCRIPT_DIR / "password_reset_watcher.log"

SSH_USER = os.getenv("PASSWORD_RESET_SSH_USER", "")
PRIVATE_KEY = os.getenv("PASSWORD_RESET_PRIVATE_KEY", "")

WATCH_FLAGS = flags.CLOSE_WRITE | flags.DELETE_SELF | flags.MOVE_SELF


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def secure_file_permissions(file_path: Path) -> None:
    """Restrict a sensitive file to its owner."""

    file_path.chmod(0o600)


def validate_runtime_configuration() -> bool:
    """Validate required files and environment variables."""

    if not PLAYBOOK_FILE.is_file():
        logging.error("Required Ansible playbook is missing.")
        return False

    if not INPUT_FILE.is_file():
        logging.error("Private password input file is missing.")
        return False

    if not SSH_USER:
        logging.error(
            "PASSWORD_RESET_SSH_USER environment variable is not set."
        )
        return False

    if not PRIVATE_KEY:
        logging.error(
            "PASSWORD_RESET_PRIVATE_KEY environment variable is not set."
        )
        return False

    private_key_path = Path(PRIVATE_KEY).expanduser()

    if not private_key_path.is_file():
        logging.error("Configured SSH private key does not exist.")
        return False

    secure_file_permissions(INPUT_FILE)
    return True


def convert_input_to_csv() -> bool:
    """Validate private input and create the temporary CSV file."""

    valid_entries = []
    seen_hosts = set()

    try:
        with INPUT_FILE.open("r", encoding="utf-8") as input_handle:
            for line_number, raw_line in enumerate(input_handle, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.split(maxsplit=1)

                if len(parts) != 2:
                    logging.warning(
                        "Skipped invalid input on line %s.",
                        line_number,
                    )
                    continue

                hostname, password = parts

                if hostname in seen_hosts:
                    logging.warning(
                        "Skipped duplicate hostname on line %s.",
                        line_number,
                    )
                    continue

                if not hostname or not password:
                    logging.warning(
                        "Skipped incomplete entry on line %s.",
                        line_number,
                    )
                    continue

                seen_hosts.add(hostname)
                valid_entries.append((hostname, password))

        if not valid_entries:
            logging.error("No valid input entries were found.")
            return False

        with CSV_FILE.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as output_handle:
            writer = csv.writer(output_handle)
            writer.writerow(["Hostname", "Password"])
            writer.writerows(valid_entries)

        secure_file_permissions(CSV_FILE)

        logging.info(
            "Created temporary CSV with %s validated entries.",
            len(valid_entries),
        )
        return True

    except OSError:
        logging.exception("Unable to process the private input file.")
        return False


def remove_temporary_csv() -> None:
    """Remove the temporary CSV containing passwords."""

    try:
        if CSV_FILE.exists():
            CSV_FILE.unlink()
            logging.info("Removed temporary password CSV.")
    except OSError:
        logging.exception("Unable to remove temporary password CSV.")


def run_ansible_playbook() -> bool:
    """Execute the password-reset playbook."""

    command = [
        "ansible-playbook",
        str(PLAYBOOK_FILE),
        "--private-key",
        str(Path(PRIVATE_KEY).expanduser()),
        "--user",
        SSH_USER,
    ]

    logging.info("Starting the Ansible password-reset playbook.")

    try:
        result = subprocess.run(
            command,
            cwd=SCRIPT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

        if result.returncode == 0:
            logging.info("Ansible playbook completed successfully.")
            return True

        logging.error(
            "Ansible playbook failed with return code %s.",
            result.returncode,
        )
        return False

    except FileNotFoundError:
        logging.error("The ansible-playbook executable was not found.")
        return False
    except OSError:
        logging.exception("Unable to execute the Ansible playbook.")
        return False


def process_input_file() -> None:
    """Convert the input file, run Ansible, and remove temporary data."""

    if not validate_runtime_configuration():
        return

    try:
        if convert_input_to_csv():
            run_ansible_playbook()
    finally:
        remove_temporary_csv()


def wait_for_input_file() -> None:
    """Wait until the private input file exists."""

    while not INPUT_FILE.exists():
        logging.warning("Input file is unavailable; waiting for recreation.")
        time.sleep(2)


def main() -> int:
    """Monitor the private input file for completed updates."""

    logging.info("Password-reset watcher started.")

    if not validate_runtime_configuration():
        return 1

    inotify = INotify()

    while True:
        wait_for_input_file()

        try:
            secure_file_permissions(INPUT_FILE)

            watch_descriptor = inotify.add_watch(
                str(INPUT_FILE),
                WATCH_FLAGS,
            )

            logging.info("Watching the private password input file.")
            recreate_watch = False

            while not recreate_watch:
                for event in inotify.read():
                    event_flags = flags.from_mask(event.mask)

                    if flags.CLOSE_WRITE in event_flags:
                        logging.info("Completed input-file update detected.")
                        time.sleep(1)
                        process_input_file()

                    if (
                        flags.DELETE_SELF in event_flags
                        or flags.MOVE_SELF in event_flags
                    ):
                        logging.warning(
                            "Input file was deleted or replaced."
                        )
                        recreate_watch = True
                        break

            try:
                inotify.rm_watch(watch_descriptor)
            except OSError:
                pass

        except KeyboardInterrupt:
            logging.info("Password-reset watcher stopped.")
            return 0
        except Exception:
            logging.exception("Unexpected watcher error.")
            time.sleep(2)


if __name__ == "__main__":
    sys.exit(main())
