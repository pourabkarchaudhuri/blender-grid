# import bpy
# for card in bpy.context.preferences.addons['cycles'].preferences.devices:
#     print("Device: ", card.name)

# prefs = bpy.context.preferences.addons['cycles'].preferences
# prefs.compute_device_type = 'CUDA'
# prefs.devices[0].use = True

# bpy.ops.wm.save_userpref()

import bpy

device_type = "CUDA"
preferences = bpy.context.preferences
cycles_preferences = preferences.addons["cycles"].preferences
cuda_devices, opencl_devices = cycles_preferences.get_devices()

print("CUDA devices : ", cuda_devices)
print("CUDA devices : ", opencl_devices)
if device_type == "CUDA":
        devices = cuda_devices
elif device_type == "OPENCL":
    devices = opencl_devices
else:
    raise RuntimeError("Unsupported device type")

activated_gpus = []

for device in devices:
    if device.type == "CPU":
        device.use = False
    else:
        device.use = True
        activated_gpus.append(device.name)

cycles_preferences.compute_device_type = "CUDA"
bpy.context.scene.cycles.device = "GPU"
print("Activated GPUs : ", activated_gpus)

# Use 'CUDA' or 'OPENCL' for your preferred method of rendering
# nvidia-docker requires 'CUDA' for GPU rendering.
# enable_gpus("CUDA")