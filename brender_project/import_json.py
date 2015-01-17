import urllib
import urllib.request
import sys
import json

jsonurl = "http://www.furnishup.com/rooms/Hul2OfaX.json"

def jsonImport(url):
	global json
	req = urllib.request.Request(url)
	opener = urllib.request.build_opener()
	f = opener.open(req)
	str_response = f.readall().decode('utf-8')
	json = json.loads(str_response)
	
	room_items = (json['room_items'])

	for item in room_items:
		print (item['model_url'])
		print (item['xpos'])
		print (item['ypos'])
		print (item['zpos'])
		print (item['rotation'])
		print (item['scale_x'])
		print (item['scale_y'])
		print (item['scale_x'])

jsonImport(jsonurl)







'''

	print(json)
	help(json)

jsonImport(jsonurl)

#extract id from json

def idExtract():
'''