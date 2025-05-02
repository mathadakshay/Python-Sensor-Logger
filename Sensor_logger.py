import time
import random
import csv
import os
import logging
import matplotlib.pyplot as plt
from collections import deque

# Ensure logs directory exists
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Setup logging
logging.basicConfig(
    filename=os.path.join(log_dir, "logger.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize deque for storing real-time data for plotting
temp_data = deque(maxlen=20)  # Store last 20 temperature readings
humidity_data = deque(maxlen=20)  # Store last 20 humidity readings
timestamps = deque(maxlen=20)  # Store last 20 timestamps

# Setup plot
plt.ion()  # Turn on interactive mode for real-time plotting
fig, ax = plt.subplots(figsize=(8, 6))
line_temp, = ax.plot([], [], label="Temperature (°C)", color='tab:red')
line_humidity, = ax.plot([], [], label="Humidity (%)", color='tab:blue')
ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend()

# Set plot limits
ax.set_ylim(15, 35)  # Temperature range
ax.set_xlim(0, 19)  # 20 data points will be displayed

try:
    with open(os.path.join(log_dir, "sensor_data.csv"), mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header if file is empty
        if os.stat(os.path.join(log_dir, "sensor_data.csv")).st_size == 0:
            writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)"])
            logging.info("CSV header written.")

        while True:
            temperature = round(random.uniform(20, 30), 2)
            humidity = round(random.uniform(40, 70), 2)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Log data and update CSV
            writer.writerow([timestamp, temperature, humidity])
            file.flush()

            # Update real-time data for plotting
            temp_data.append(temperature)
            humidity_data.append(humidity)
            timestamps.append(timestamp)

            # Update the plot
            line_temp.set_data(range(len(temp_data)), temp_data)
            line_humidity.set_data(range(len(humidity_data)), humidity_data)
            ax.set_xticks(range(len(timestamps)))
            ax.set_xticklabels(list(timestamps), rotation=45)

            plt.draw()  # Force the plot to update
            plt.pause(2)  # Pause to update the plot and prevent it from freezing

            # Logging the data
            logging.info(f"Data logged: Temp={temperature}, Humidity={humidity}")
            print(f"{timestamp} → Temp: {temperature}°C, Humidity: {humidity}%")

except Exception as e:
    logging.error(f"Logging failed: {e}")
    print("An error occurred. Check logs/logger.log for details.")
finally:
    plt.ioff()  # Turn off interactive mode once done
    plt.show()  # Display the final plot
