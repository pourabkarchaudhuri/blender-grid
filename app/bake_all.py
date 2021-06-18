# Blender v2.8x +
import bpy
import os
import sys
import shutil
import argparse
import time

print("SYS.ARGV[-1]: " + sys.argv[-1])
# import dependencies

# Write argparse to fetch the parameters from command line
# Ideal command should be, blender {PROJECT_FILE_NAME} -b -P {SCRIPT_NAME.py} --extension {EXTENSION}
start_time = time.time()

DIRECTORY_PATH = os.path.join(os.getcwd(), 'jobs')
PROJECT_NAME = bpy.path.basename(bpy.data.filepath)
JOB_PATH = os.path.join(DIRECTORY_PATH, PROJECT_NAME)
BAKED_TEXTURES_PATH = os.path.join(JOB_PATH, 'baked_textures')
RENDERS_PATH = os.path.join(JOB_PATH, 'renders')
EXTENSION = 'png'

for card in bpy.context.preferences.addons['cycles'].preferences.devices:
    print("Card Name : ", card.name)

# bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'CUDA'
prefs.devices[0].use = True

# Set the device and feature set
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.feature_set = "SUPPORTED"

if not os.path.exists(DIRECTORY_PATH):
    os.makedirs(DIRECTORY_PATH)
if not os.path.exists(JOB_PATH):
    os.makedirs(JOB_PATH)
if not os.path.exists(BAKED_TEXTURES_PATH):
    os.makedirs(BAKED_TEXTURES_PATH)
if not os.path.exists(RENDERS_PATH):
    os.makedirs(RENDERS_PATH)
scene = bpy.context.scene

for obj in scene.objects:
    obj.select_set(False)

collection = bpy.data.collections["Exports"]
cameras = bpy.data.collections["Cameras"]
print("Collection Name to be processed : {}".format(collection.name))

# for obj in scene.objects:
for obj in collection.all_objects:
    if obj.type != 'MESH':
        continue
    print("Selected Object name :", obj.name)
    print("Number of Materials attached : ",len(obj.data.materials))
    if(len(obj.data.materials) == 0):
        print("No material")
        continue
    else:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        print("Mat Name : ", obj.data.materials)
        img = bpy.data.images.new(obj.name + '_BakedTexture', 1024, 1024)
        
        for mat in obj.data.materials:
            mat.use_nodes = True #Here it is assumed that the materials have been created with nodes, otherwise it would not be possible to assign a node for the Bake, so this step is a bit useless
            nodes = mat.node_tree.nodes
            texture_node =nodes.new('ShaderNodeTexImage')
            texture_node.name = 'Bake_node'
            texture_node.select = True
            nodes.active = texture_node
            texture_node.image = img #Assign the image to the node

            bpy.ops.object.bake(type='COMBINED', save_mode='INTERNAL')
            filename = obj.name + '_' + mat.name + '_baked' + '.' + EXTENSION
            img.save_render(filepath=os.path.join(BAKED_TEXTURES_PATH, filename))
            
            baked_image = bpy.data.images.load(os.path.join(BAKED_TEXTURES_PATH, filename))

            texture_node.image = baked_image

        # for mat in obj.data.materials:
        #     mat.use_nodes = True #Here it is assumed that the materials have been created with nodes, otherwise it would not be possible to assign a node for the Bake, so this step is a bit useless
        #     nodes = mat.node_tree.nodes
        #     links = mat.node_tree.links
        #     emission_node = nodes.new(type='ShaderNodeEmission')
        #     emission_node.name = 'Emission_node'
        #     emission_node.select = True
        #     nodes.active = emission_node
        #     # emission_node.image = img #Assign the image to the node
            
        #     # Create a link between Bake node and emission
        #     texture_node = nodes["Bake_node"]
        #     bake2emission_link = links.new(texture_node.outputs[0], emission_node.inputs[0])
            
        #     material_node = nodes["Material Output"]
        #     emission2material_link = links.new(emission_node.outputs[0], material_node.inputs[0])

        obj.select_set(False)
       

for obj in cameras.all_objects:
    # print("Selected Camera name :", obj.name)
    # bpy.context.view_layer.objects.active = camera
    # obj.select_set(True)
    if obj.type == 'CAMERA':
        bpy.context.scene.camera = obj
        print('Set camera %s' % obj.name )
        filename = obj.name + '_render' + '.' + EXTENSION
        # file = os.path.join("C:/tmp", obj.name )
        bpy.context.scene.render.filepath = os.path.join(RENDERS_PATH, filename)
        bpy.ops.render.render( write_still=True )
    else:
        print("No Cameras in this collection")
    # camera.select_set(False)

execution_time = (time.time() - start_time)
print("Total Job Execution time for baking and rendering : {0:.2f}s".format(round(execution_time,2)))
bpy.ops.file.autopack_toggle()
#------------
# bpy.ops.wm.save_as_mainfile(filepath=os.path.join(JOB_PATH, PROJECT_NAME))

# # Now baking is done and nodes are saved as a project are all done. Time to unlink and reroute bsdf
for obj in scene.objects:
    obj.select_set(False)

for obj in collection.all_objects:
    if obj.type != 'MESH':
        continue
    if(len(obj.data.materials) == 0):
        print("No material")
        continue
    else:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
                
        for mat in obj.data.materials:
            mat.use_nodes = True #Here it is assumed that the materials have been created with nodes, otherwise it would not be possible to assign a node for the Bake, so this step is a bit useless
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
       
            # Create a link between Bake node and emission
            texture_node = nodes["Bake_node"]

            # links.remove(texture_node.outputs[0].links[0])
            material_node = nodes["Material Output"]

            #Create this
            principal_BSDF_node = nodes.new('ShaderNodeBsdfPrincipled')
            if(principal_BSDF_node):
                print("principal_BSDF_node exists")
            else:
                print("principal_BSDF_node not present")
            texture2BSFD_link = links.new(texture_node.outputs[0], principal_BSDF_node.inputs[0])
            BSDF2material_output_link = links.new(principal_BSDF_node.outputs[0], material_node.inputs[0])
        obj.select_set(False)

# select collection items only.
for obj in collection.all_objects:
    obj.select_set(True)

print("Only Collection items to be exported are selected")

# Time to export
MODEL_ASSET_PATH = os.path.join(JOB_PATH, 'models')
if not os.path.exists(MODEL_ASSET_PATH):
    os.makedirs(MODEL_ASSET_PATH)

bpy.ops.export_scene.fbx(filepath=os.path.join(MODEL_ASSET_PATH, PROJECT_NAME + '.fbx'), use_selection=True, apply_scale_options='FBX_SCALE_ALL', path_mode='COPY', embed_textures=True)
# bpy.ops.export_scene.fbx(filepath=os.path.join(MODEL_ASSET_PATH, PROJECT_NAME + '.fbx'), use_selection=True, apply_scale_options='FBX_SCALE_ALL', path_mode='COPY', embed_textures=True)
bpy.ops.export_scene.gltf(filepath=os.path.join(MODEL_ASSET_PATH, PROJECT_NAME + '.glb'), export_format='GLB', export_selected=True )
shutil.make_archive(JOB_PATH, 'zip', JOB_PATH)
print("{} : Zipped and Archived at : {}".format(PROJECT_NAME, JOB_PATH))


# Call function to send the zip as mail