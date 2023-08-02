import csv
import schedule
import time
import datetime
import random
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


# Create the SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# Create the mcp object
mcp = MCP.MCP3008(spi, cs)

# Create analog inputs connected to the input pins on the MCP3008.
channel_0 = AnalogIn(mcp, MCP.P0)

def evaluateSensorValue():
    # Read analog sensor values from the channel 0.
    sensor_value = channel_0.value
    # Get the channel voltage.
    channel_voltage = channel_0.voltage
    # Print the sensor value and the channel voltage.
    print('Analog Read: ' + str(sensor_value))
    print('Channel Voltage: ' + str(channel_voltage) + 'V')
    return channel_0.voltage



def write_to_csv(value):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('output.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, value])

def job():
    sensor_value = evaluateSensorValue()
    write_to_csv(sensor_value)
    print(f"Sensor value: {sensor_value}")

def run_scheduled_job():
    schedule.every(1).minutes.do(job)
    start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(6))
    end_time = datetime.datetime.combine(datetime.date.today(), datetime.time(21))

    while True:
        current_time = datetime.datetime.now()
        if start_time <= current_time <= end_time:
            schedule.run_pending()
        else:
            break
        time.sleep(1)

if __name__ == "__main__":
    run_scheduled_job()
