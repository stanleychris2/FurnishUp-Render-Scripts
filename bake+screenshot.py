import bpy

# config
output_path =    "_baked.js"
output_texture = "_baked.png"
obj_out =        "_baked.obj"

preobj_out =     ".obj"
blendpath =      ".blend"

"""
def remove_all():
    # delete anything currently imported
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]
    for object_name in candidate_list:
      bpy.data.objects[object_name].select = True
    bpy.ops.object.delete()
    for item in bpy.data.meshes:
      bpy.data.meshes.remove(item)
  
remove_all()
  
# import obj
bpy.ops.import_scene.obj(filepath=file_path)
"""

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

# select (threejs needs this)
bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.objects.active = bpy.context.selected_objects[0]
main_object = bpy.context.scene.objects.active

#export pre-bake obj/mtl
bpy.ops.export_scene.obj(filepath=preobj_out, axis_forward='-Z', axis_up='Y')
bpy.ops.wm.save_as_mainfile(filepath= blendpath)

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
bpy.context.scene.world.light_settings.ao_factor = 0.1
bpy.context.scene.world.light_settings.use_environment_light = True
bpy.context.scene.world.light_settings.environment_energy = 1.0
bpy.context.scene.world.light_settings.samples = 15


# bake it
bpy.context.scene.objects.active = main_object
bpy.ops.object.select_all(action='DESELECT')
main_object.select = True
    
# ref: http://blenderartists.org/forum/archive/index.php/t-222391.html
bpy.ops.mesh.uv_texture_add() 
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project( angle_limit = 66, island_margin = 0.9 ) 
image = bpy.data.images.new( name='atlas', width = 256, height = 256, )
bpy.data.screens['UV Editing'].areas[1].spaces[0].image = image # Set the new image to the new UV texture 
bpy.ops.object.editmode_toggle()
bpy.context.scene.render.bake_type = 'FULL' # Set to bake all 
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
mtex = mat.texture_slots.add()
mtex.texture = tex
mtex.texture_coords = 'UV'
main_object.data.materials.append(mat)
bpy.context.object.active_material.diffuse_color = (1, 1, 1)
bpy.context.object.active_material.diffuse_intensity = 1


# delete plane
bpy.ops.object.select_all(action='SELECT')
main_object.select = False
bpy.ops.object.delete()

# export threejs
bpy.ops.export.threejs(filepath=output_path)

#export objs
bpy.ops.export_scene.obj(filepath=obj_out, axis_forward='-Z', axis_up='Y')

#add camera
bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(-125, -350, 100), rotation=(1.403,0,-0.3398), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.context.object.data.clip_end = 900

#add whitebackground
bpy.context.scene.world.use_sky_paper = True
bpy.context.scene.world.horizon_color = (1, 1, 1)

# draw a plane
dim = bpy.context.scene.objects.active.dimensions
plane_radius = 10 * max(dim[0], dim[1])
bpy.ops.mesh.primitive_plane_add(radius=1000, view_align=False, enter_editmode=False, location=(0, 0, 0))
plane = bpy.context.scene.objects.active
pmat = bpy.data.materials.new('plane_mat')
plane.data.materials.append(pmat)
bpy.context.object.active_material.use_transparency = False
bpy.context.object.active_material.raytrace_mirror.use = False
bpy.context.object.active_material.diffuse_color = (1, 1, 1)
bpy.context.object.active_material.diffuse_intensity = 1







s