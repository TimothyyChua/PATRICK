import serial
import time

import Telegram
import Speaker
import Popup
import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('Config.JSON')


class SensorHandler:
	def __init__(self, parent):
		self.parent = parent
		self.ser = serial.Serial(config["port"], config["baud"], timeout = 1.0)
		time.sleep(2)
		self.ser.reset_input_buffer()
		self.heartrate = 0
		self.breathrate = 0
		#print("Serial OK")
		self.telegram = Telegram.TelegramBot()
		self.popup = Popup.PopupWindow(parent)
		self.bg_sound = Speaker.AudioPlayer(config["sounds"]["bg_sound"], 1000, 0.9)
		self.ayo_sound = Speaker.AudioPlayer(config["sounds"]["ayo_sound"], 1000)
	
	def parse_line(self, line):
		if line.startswith("Heartrate:") and "Breathrate:" in line:
			parts = line.split(",")
			hr = parts[0].split(":")[1]
			br = parts[1].split(":")[1]
			return hr, br
		return None, None
		
	
	def read_line(self):
		if not self.bg_sound.is_playing():
			self.bg_sound.play()
		if self.ser.in_waiting >0:
			line = self.ser.readline().decode('utf-8').strip()
			print(line)
			hr, br = self.parse_line(line)
			print(hr, br)
			if hr and br:
				print(f"Heartrate: {hr}, Breathrate: {br}")
				self.heartrate = float(hr)
				self.breathrate = float(br)
				self.telegram.send_message(f"Heartrate: {hr}, Breathrate: {br}")

				if self.heartrate > 170 and self.heartrate <= 0:
					self.ayo_sound.play()
					self.popup.show()
				return hr, br
	
	def stop(self):
		self.ser.close()
		self.bg_sound.stop()
		self.ayo_sound.stop()
	
#try:
#    while True:
#        time.sleep(0.01)
#        if ser.in_waiting >0:
#            line = ser.readline().decode('utf-8').strip()
#            if parse_line(line):
#                print(line)
#except KeyboardInterrupt:
#    print("Close Serial Communication")
#    ser.close()
