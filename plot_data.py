import csv
import matplotlib.pyplot as plt

CSV_FILE = "sensor_log.csv"


def load_data(filepath):
    elapsed_time = []
    temperature = []
    humidity = []
    distance = []

    with open(filepath, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                elapsed = float(row["Elapsed_Time_s"])
            except (ValueError, TypeError, KeyError):
                continue

            elapsed_time.append(elapsed)

            for column, target in [
                ("Temperature_C", temperature),
                ("Humidity_Pct", humidity),
                ("Distance_cm", distance),
            ]:
                try:
                    val = row[column]
                    target.append(float(val) if val not in ("", None) else None)
                except (ValueError, TypeError, KeyError):
                    target.append(None)

    return elapsed_time, temperature, humidity, distance


def plot_sensor(elapsed_time, values, title, ylabel, filename):
    valid_points = [
        (elapsed_time[i], values[i])
        for i in range(len(values))
        if values[i] is not None
    ]

    if not valid_points:
        print(f"No valid data available to plot: {title}")
        return

    x_vals, y_vals = zip(*valid_points)

    plt.figure(figsize=(9, 4.5))
    plt.plot(x_vals, y_vals, marker="o", markersize=4, linestyle="-", linewidth=1.5)
    plt.title(title)
    plt.xlabel("Elapsed Time (s)")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Saved {filename}")


def main():
    elapsed, temp, hum, dist = load_data(CSV_FILE)
    plot_sensor(elapsed, temp, "Temperature Over Time", "Temperature (°C)", "temperature_plot.png")
    plot_sensor(elapsed, hum, "Relative Humidity Over Time", "Relative Humidity (%)", "humidity_plot.png")
    plot_sensor(elapsed, dist, "Distance Over Time", "Distance (cm)", "distance_plot.png")
    plt.show()


if __name__ == "__main__":
    main()
