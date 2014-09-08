import bpy

# config
file_path = "/Users/petershaw/Documents/test_models/BESTA-Bench_with_legs_black-browm.obj"
output_path = "/Users/petershaw/Documents/output.js"

# delete anything currently imported
candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]
for object_name in candidate_list:
  bpy.data.objects[object_name].select = True
bpy.ops.object.delete()
for item in bpy.data.meshes:
  bpy.data.meshes.remove(item)
  
# import obj
bpy.ops.import_scene.obj(filepath=file_path)

# select (threejs needs this)
bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.objects.active = bpy.context.selected_objects[0]

# export threejs
bpy.ops.export.threejs(filepath=output_path)
