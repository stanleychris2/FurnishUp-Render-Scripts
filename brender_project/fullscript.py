import urllib
import urllib.request
import sys
import json
import io, bpy
from urllib import request


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
		item_import_url(item['model_url'])
		#select object
		bpy.ops.object.select_all(action='SELECT')
		bpy.context.scene.objects.active = bpy.context.selected_objects[0]
		main_object = bpy.context.scene.objects.active
		#center object if not already
		center_active()
		#x-axis, xpos
		bpy.context.object.location[0] = item['xpos']
		#y-axis, zpos
		bpy.context.object.location[1] = item['zpos']
		#z-axis, ypos
		bpy.context.object.location[2] = item['ypos']




def item_import_url(item_url):
    tmp_filename = "/tmp/temp.js"
    request.urlretrieve(item_url, tmp_filename)
    bpy.ops.__getattr__('import').threejs(filepath=tmp_filename)

def center_active():
    object = bpy.context.scene.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    def get_pos(object, axis):
        return (object.bound_box[0][axis] + object.bound_box[1][axis] + 
                object.bound_box[2][axis] + object.bound_box[3][axis] + 
                object.bound_box[4][axis] + object.bound_box[5][axis] +
                object.bound_box[6][axis] + object.bound_box[7][axis]) / 8
    xpos = get_pos(object, 0)
    ypos = get_pos(object, 1)
    zpos = get_pos(object, 2)
    object.location = (-xpos, -ypos, -zpos + (object.dimensions[2]/2))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)



#import for xpos/zpos/ypos.... y needs to be a negative value b/c top left is origin for FU and bottom left is origin for blender... 
#also need to find out what to do w/ finding center of item to place z value... its slightly off if you 'set geometry to origin'



jsonImport(jsonurl)