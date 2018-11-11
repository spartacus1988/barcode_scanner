#!/usr/bin/python
import sys
import requests
import json
from twilio.rest import Client


def extract_api_key(pathfile):
	with open(pathfile, 'r') as f:
		for line in f:
			api_key = line.strip().split(' ')
		return api_key[0]


#api_key = "" #https://upcdatabase.org/
#api_key = extract_api_key('api_key.txt')
#print(api_key)


def extract_sms_credentials(pathfile):
	with open(pathfile, 'r') as f:
		for line in f:
			account, token = line.strip().split(':')
		return account, token


#api_key = "" #https://upcdatabase.org/
api_key = extract_api_key('api_key.txt')
print(api_key)



def barcode_reader():
	"""Barcode code obtained from 'brechmos' 
	https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
	hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
		   17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
		   29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
		   45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

	hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
			17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
			29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
			45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

	fp = open('/dev/hidraw0', 'rb')

	ss = ""
	shift = False

	done = False

	while not done:

		## Get the character from the HID
		buffer = fp.read(8)
		for c in buffer:
			if ord(c) > 0:

				##  40 is carriage return which signifies
				##  we are done looking for characters
				if int(ord(c)) == 40:
					done = True
					break;

				##  If we are shifted then we have to
				##  use the hid2 characters.
				if shift:

					## If it is a '2' then it is the shift key
					if int(ord(c)) == 2:
						shift = True

					## if not a 2 then lookup the mapping
					else:
						ss += hid2[int(ord(c))]
						shift = False

				##  If we are not shifted then use
				##  the hid characters

				else:

					## If it is a '2' then it is the shift key
					if int(ord(c)) == 2:
						shift = True

					## if not a 2 then lookup the mapping
					else:
						ss += hid[int(ord(c))]
	return ss

def UPC_lookup(api_key,upc):
	'''V3 API'''

	url = "https://api.upcdatabase.org/product/%s/%s" % (upc, api_key)

	headers = {
		'cache-control': "no-cache",
	}

	response = requests.request("GET", url, headers=headers)

	print("-----" * 5)
	print(upc)
	print(json.dumps(response.json(), indent=2))
	print("-----" * 5 + "\n")

if __name__ == '__main__':
	try:
		while True:
			#UPC_lookup(api_key,barcode_reader())
			upc = '072311130127'
			api_key = extract_api_key('api_key.txt')
			print(upc)
			print(api_key)
			#UPC_lookup(api_key,upc)
			#UPC_lookup(api_key,barcode_reader())
			response = {
						  "category": "", 
						  "rate/up": "0", 
						  "upcnumber": "072311130127", 
						  "description": "Dos Equis Special Lager", 
						  "newupc": "072311130127", 
						  "title": "Dos Equis Special Lager", 
						  "color": "", 
						  "gender": "", 
						  "brand": "", 
						  "alias": "", 
						  "st0s": "72311130127", 
						  "status": 200, 
						  "msrp": "0.00", 
						  "error": "false", 
						  "rate/down": "0", 
						  "type": "", 
						  "age": "", 
						  "unit": "&quot;One (1) bo", 
						  "size": ""
						}
			print(json.dumps(response, indent=2))

			account, token = extract_sms_credentials('sms_credentials.txt')
			print(account)
			print(token)

			client = Client(account, token)

			message = client.messages.create(to="+12316851234", from_="+15555555555",
								 body="Hello there!")
			print(message.sid)



			break
	except KeyboardInterrupt:
		pass