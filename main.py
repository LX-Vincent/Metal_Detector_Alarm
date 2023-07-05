# Import useful classes
import machine
import utime
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# Define the pins for the metal sensor,PIR sensor, and buzzer
sensor_metal = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)
sensor_pir = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(13, machine.Pin.OUT)

# Define SDA (Serial Data) and SCL (Serial Clock) pins for I2C communication
sda = machine.Pin(0)
scl = machine.Pin(1)

# Define the number of rows and columns for the LCD
i2c_num_rows = 2
i2c_num_cols = 16

# Initialize the 12C interface with the specified pins and communication frequency
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

# Scan for 12C devices and get the address of the LCD
i2c_addr = i2c.scan()[0]

# Initialize the LCO display using I2C communication
lcd = I2cLcd(i2c, i2c_addr, i2c_num_rows, i2c_num_cols)


# Set the handler for the PIR sensor interrupt
def pir_handler(pin):
    # If the IRO RISING signal is coming(motion detected)
    if pin.value():
        lcd.clear()
        lcd.putstr("Welcome!")  # Display welcome message
        lcd.putstr("Metal Checking..")  # Display metal checking message
        utime.sleep(3)  # Wait for 3 seconds
        if sensor_metal.value() == 0:  # If metal is detected by the metal sensor
            activate_alarm()  # Call the function to activate the alarm
        else:
            lcd.clear()
            lcd.putstr("No Metal,")  # Display message indicating no metal detected
            lcd.putstr("welcome!")  # Display welcome message


# Define the interrupt trigger as well as the handler for the PIR sensor
sensor_pir.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_handler)


# Function to activate the alarm when metal is detected
def activate_alarm():
    lcd.clear()
    lcd.putstr("Attention:")  # Display attention message
    lcd.putstr("Metal Detected!")  # Display metal detected message
    for i in range(10):
        if buzzer.value():
            buzzer.value(0)
        else:
            buzzer.value(1)
        utime.sleep(0.5)  # Wait for 8.5 seconds

