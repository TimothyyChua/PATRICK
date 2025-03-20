import requests
import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('Config.JSON')

class TelegramBot:
	def __init__(self):
		self.TOKEN = "" #Enter telegram bot token
		self.chat_id = config["chat_id"]
		#self.chat_id = "" #Enter chat id
		self.message = "INITIALISED"
		self.url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.chat_id}&text={self.message}"
		
	def send_message(self, msg):
		if msg:
			self.message = str(msg)
			self.url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.chat_id}&text={self.message}"
		requests.get(self.url).json()

#test = TelegramBot()
#test.send_message("fall_detected")
#requests.get(test.url).json() # this sends the message



