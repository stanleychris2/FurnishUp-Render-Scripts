import bpy

# config
file_path = "/Users/petershaw/Documents/IKEA_Models/HEMNES TV storage combination, black-brown/HEMNES_tv_storage_combination_black-brown.obj"
output_path = "/Users/petershaw/Documents/blueprint-viewer/models/output.js"
output_texture = "/Users/petershaw/Documents/blueprint-viewer/textures/atlas.png"

def remove_all():
    # delete anything currently imported
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]
    for object_name in candidate_list:
      bpy.data.objects[object_name].select = True
    bpy.ops.object.delete()
    for item in bpy.data.meshes:
      bpy.data.meshes.remove(item)
  
remove_all()

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
  
# import obj
bpy.ops.import_scene.obj(filepath=file_path)

# select (threejs needs this)
bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.objects.active = bpy.context.selected_objects[0]
main_object = bpy.context.scene.objects.active

# join and center
bpy.ops.object.join()
center_active()

# draw a plane
dim = bpy.context.scene.objects.active.dimensions
plane_radius = 10 * max(dim[0], dim[1])
bpy.ops.mesh.primitive_plane_add(radius=1000, view_align=False, enter_editmode=False, location=(0, 0, 0))
plane = bpy.context.scene.objects.active

# lighting
bpy.context.scene.world.light_settings.use_ambient_occlusion = True
bpy.context.scene.world.light_settings.ao_factor = 1.0
bpy.context.scene.world.light_settings.use_environment_light = True
bpy.context.scene.world.light_settings.environment_energy = 0.5

# bake it
bpy.context.scene.objects.active = main_object
bpy.ops.object.select_all(action='DESELECT')
main_object.select = True
    
# ref: http://blenderartists.org/forum/archive/index.php/t-222391.html
bpy.ops.mesh.uv_texture_add() 
bpy.ops.object.editmode_toggle() 
bpy.ops.uv.smart_project( angle_limit = 66 ) 
image = bpy.data.images.new( name='atlas', width = 1024, height = 1024, )
bpy.data.screens['UV Editing'].areas[1].spaces[0].image = image # Set the new image to the new UV texture 
bpy.ops.object.editmode_toggle()
bpy.context.scene.render.bake_type = 'TEXTURE' # Set to bake texures only
bpy.ops.object.bake_image()

# save new image
image.filepath_raw = output_texture
image.file_format = 'PNG'
image.save()

# remove old textures
while len(main_object.data.materials) > 0: 
    bpy.ops.object.material_slot_remove() 
main_object.data.uv_textures[0].active = True 
bpy.ops.mesh.uv_texture_remove()

# create a new material and texture
tex = bpy.data.textures.new('bake_tex', type = 'IMAGE')
tex.image = image
mat = bpy.data.materials.new('bake_mat')
mat.diffuse_intensity = 1
mat.diffuse_color = (1, 1 ,1)
mtex = mat.texture_slots.add()
mtex.texture = tex
mtex.texture_coords = 'UV'
main_object.data.materials.append(mat)

# delete plane
bpy.ops.object.select_all(action='SELECT')
main_object.select = False
bpy.ops.object.delete()

# export threejs
bpy.ops.export.threejs(filepath=output_path)

