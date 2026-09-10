"""
generate_log.py
----------------
Writes a simple activity log to a timestamped .txt file.
Demonstrates basic File I/O from a standalone script.
"""

from datetime import datetime


def write_log(log_data):
    """Write each log entry to a new line in a timestamped file."""
    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, "w") as file:
        for entry in log_data:
            file.write(f"{entry}\n")
    return filename


if __name__ == "__main__":
    log_data = ["User logged in", "User updated profile", "Report exported"]
    filename = write_log(log_data)
    print(f"Log written to {filename}")