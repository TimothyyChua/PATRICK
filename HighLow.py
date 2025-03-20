import gpiod
import time

LED_PIN = 6
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

class six_out:
    
    def __init__(self):
        self.state = 1
        
    def on(self):
        if self.state == 0:
            led_line.set_value(1)
            self.state = 1
            print("GPIO 6 set to HIGH")
    
    def off(self):
        if self.state == 1:
            led_line.set_value(0)
            self.state = 0
            print("GPIO 6 set to LOW")
    
#led_line.release()
