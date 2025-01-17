import time
import Adafruit_ADS1x15




class Joystick:
    """
    https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
    ADS1115 ADC: https://cdn-shop.adafruit.com/datasheets/ads1115.pdf
    Example code: https://github.com/adafruit/Adafruit_Python_ADS1x15/blob/master/examples/simpletest.py
    """
    def __init__(self):
        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1115(busnum=1)

        # Note you can change the I2C address from its default (0x48), and/or the I2C
        # bus by passing in these optional parameters:
        #adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        self.GAIN = 1

        # ADC channels
        self.joy_btn_adc = 0
        self.joy_y_adc = 1
        self.joy_x_adc = 2

    def map_to_100(self, value, input_min, input_max):
        # Ensure the input is within the specified range
        if input_min == input_max:
            raise ValueError("input_min and input_max must be different values.")
        # Map the value to the 0-100 range
        mapped_value = (value - input_min) / (input_max - input_min) * 100
        # Ensure the result is within the 0-100 range
        return int(max(0, min(100, mapped_value)))
    

    def print_adc_values(self):
        print('Reading ADS1x15 values, press Ctrl-C to quit...')
        # Print nice channel column headers.
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        print('-' * 37)
        # Main loop.
        while True:
            # Read all the ADC channel values in a list.
            values = [0]*4
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                values[i] = self.adc.read_adc(i, gain=self.GAIN)
                # Note you can also pass in an optional data_rate parameter that controls
                # the ADC conversion time (in samples/second). Each chip has a different
                # set of allowed data rate values, see datasheet Table 9 config register
                # DR bit values.
                #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
                # Each value will be a 12 or 16 bit signed integer value depending on the
                # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
            # Print the ADC values.
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
            # Pause for half a second.
            time.sleep(0.5)

    def read_joy_btn(self):
        BTN_THRES = 200
        value = self.adc.read_adc(self.joy_btn_adc, gain=self.GAIN)
        if value < BTN_THRES:
            # Button pressed
            return True
        return False
    
    def read_joy_x(self):
        JOY_X_MIN = 100
        JOY_X_MAX = 26000
        value = self.adc.read_adc(self.joy_x_adc, gain=self.GAIN)
        value = self.map_to_100(value, JOY_X_MIN, JOY_X_MAX)
        return value
    
    def read_joy_y(self):
        JOY_Y_MIN = 100
        JOY_Y_MAX = 26000
        value = self.adc.read_adc(self.joy_y_adc, gain=self.GAIN)
        value = self.map_to_100(value, JOY_Y_MIN, JOY_Y_MAX)
        return value

if __name__ == "__main__":
    joystick = Joystick()

    while True:
        print("BTN:", joystick.read_joy_btn(), end=" | ")
        print("X:", joystick.read_joy_x(), end=" | ")
        print("Y:", joystick.read_joy_y())


        time.sleep(0.5)