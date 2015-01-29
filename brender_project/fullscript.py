import urllib
import urllib.request
import sys
import json
import io, bpy
from urllib import request


jsonurl = "http://www.furnishup.com/rooms/2L4ievon.json"

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
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

def item_select(counter):
    if counter >= 1:
        item_name = "temp.00"+str(counter)
    else:
        item_name = "temp"
    bpy.data.objects[item_name].select = True

def jsonImport(url):
	global json
	req = urllib.request.Request(url)
	opener = urllib.request.build_opener()
	f = opener.open(req)
	str_response = f.readall().decode('utf-8')
	json = json.loads(str_response)
	
	room_items = (json['room_items'])
	
	counter = 0

	for item in room_items:
		item_import_url(item['model_url'])
		
		#select object 		
		item_select(counter)
		bpy.context.scene.objects.active = bpy.context.selected_objects[0]


		bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')


		#scale object
		bpy.context.object.scale[0] = item['scale_x']
		bpy.context.object.scale[2] = item['scale_y']
		bpy.context.object.scale[1] = item['scale_z']

		bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

		center_active()

		#x-axis, xpos
		bpy.context.object.location[0] = item['xpos']
		#y-axis, zpos
		bpy.context.object.location[1] = (-1*item['zpos'])
		#z-axis, ypos
		bpy.context.object.location[2] = item['ypos']
		#set item scale 
		bpy.ops.transform.rotate(value= item['rotation'], axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		#deselect all to get ready for next object
		bpy.ops.object.select_all(action='DESELECT')


		counter += 1

#import for xpos/zpos/ypos.... y needs to be a negative value b/c top left is origin for FU and bottom left is origin for blender... 
#also need to find out what to do w/ finding center of item to place z value... its slightly off if you 'set geometry to origin'



jsonImport(jsonurl)