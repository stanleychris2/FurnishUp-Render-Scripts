import io, bpy
from urllib import request

#make a temp filename that is valid on your machine
tmp_filename = "/tmp/temp.js"

#fetch the model in this file
request.urlretrieve("https://blueprint-dev.s3.amazonaws.com/uploads/item_model/model/777/ReliaBilt_Panel_Hollow_Core_baked.js", tmp_filename)

#import three.js
bpy.ops.__getattr__('import').threejs(filepath=tmp_filename)



'''

import urllib
import urllib.request
import sys
import json
import io, bpy
from urllib import request



item_url = "https://blueprint-dev.s3.amazonaws.com/uploads/item_model/model/777/ReliaBilt_Panel_Hollow_Core_baked.js"

def item_import_url(item_url):
    tmp_filename = "/tmp/temp.js"
    request.urlretrieve(item_url, tmp_filename)
    bpy.ops.__getattr__('import').threejs(filepath=tmp_filename)

item_import_url(item_url)




http://stackoverflow.com/questions/19076062/blender-material-from-url


import io, bpy
from urllib import request

def run(origin):
    # Load image file from url.    
    try:
        #make a temp filename that is valid on your machine
        tmp_filename = "/tmp/temp.png"
        #fetch the image in this file
        request.urlretrieve("https://www.google.com/images/srpr/logo4w.png", tmp_filename)
        #create a blender datablock of it
        img = bpy.data.images.load(tmp_filename)
        #pack the image in the blender file so...
        img.pack()
        #...we can delete the temp image
        os.remove(tmp_filename)
    except Exception as e:
        raise NameError("Cannot load image: {0}".format(e))
    # Create image texture from image
    cTex = bpy.data.textures.new('ColorTex', type='IMAGE')
    cTex.image = img
    # Create material
    mat = bpy.data.materials.new('TexMat')
    # Add texture slot for color texture
    mtex = mat.texture_slots.add()
    mtex.texture = cTex
    # Create new cube
    bpy.ops.mesh.primitive_cube_add()
    # Add material to created cube
    ob = bpy.context.object
    me = ob.data
    me.materials.append(mat)

run((0,0,0))


'''