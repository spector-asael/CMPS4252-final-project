import csv
import os

CSV_HEADERS = [
    "Timestamp",
    "Elapsed_Time_s",
    "Temperature_C",
    "Humidity_Pct",
    "Distance_cm",
]


def init_csv(filepath):
    """Create the CSV file with headers if it does not already exist or is empty."""
    needs_header = not os.path.exists(filepath) or os.path.getsize(filepath) == 0
    if needs_header:
        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)


def log_measurement(filepath, timestamp, elapsed_s, temp_c, humidity, dist_cm):
    """Append one sensor record to CSV and close immediately to persist data."""
    row = [
        timestamp,
        elapsed_s,
        "" if temp_c is None else temp_c,
        "" if humidity is None else humidity,
        "" if dist_cm is None else dist_cm,
    ]
    with open(filepath, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)
