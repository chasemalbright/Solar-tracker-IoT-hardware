# import flask module
from flask import Flask
from flask_cors import CORS
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time

# instance of flask application
app = Flask(__name__)
CORS(app)

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



# home route that returns below text
# when root url is accessed
@app.route("/")
def get_voltage():
    evaluateSensorValue()
    return str(channel_0.voltage)

if __name__ == '__main__':
	app.run(debug=True, port=8001)
    