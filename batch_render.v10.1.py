# Commandline Blender render script

# Author:   Mike Schmitt

# updates Mar14, 2022
# - changed output dir structure and naming convention to reduce number of subdirectories and added colorspace name to file for ACES
# - output goes to ../rndr/blender/[scene]/[scene].[viewLayer].[res_x x res_y].[colorspace].#####.exr

# Usage:

# blender --background <scene_name>.blend --python /viz/home/mschmitt/dev/blender/python/batch_render.py -- <frame_start> <frame_end> <frame_step> <threads>



import bpy
import sys
import os

# Ignore args before "--"
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
print(argv)

# Set number of cpus
from multiprocessing import cpu_count

cores_use = int(argv[3])

cores_available = cpu_count()
cores_enabled = min(cores_use, cores_available)

for scene in bpy.data.scenes:
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = cores_enabled

#if len(sys.argv) < 3:
#    sys.exit('Usage: %s <frame_start> <frame_end> <frame_step>' % sys.argv[0])

# Resolution
res_x = bpy.context.scene.render.resolution_x
res_y = bpy.context.scene.render.resolution_y
res_per = bpy.context.scene.render.resolution_percentage
res_x = res_x * res_per/100
res_y = res_y * res_per/100

# Frame Range
#fs = bpy.context.scene.frame_start
#fe = bpy.context.scene.frame_end
#fstep = bpy.context.scene.frame_step
fs = int(argv[0])
fe = int(argv[1])
fstep = int(argv[2])

# Store Original Output filename
fp = bpy.context.scene.render.filepath

# Make a record of all Enabled render layers, then Deactivate all render layers

#rl = bpy.context.scene.render.layers    # list of all render layers in Blender 2.79
rl = bpy.context.scene.view_layers

el_index = [i for i in range(len(rl)) if rl[i].use == True]     # create index list of Enabled layers

# Deactivate all render layers first - they will be reactivated one by one later
for l in rl:
    l.use = False

# Cycle through frame range.  Run this loop first in order to render all enabled render layers per frame

for f in range(fs, fe + 1, fstep):

    # Set Current Frame

    bpy.context.scene.frame_set(f)

    # Cycle through list of Enabled Render Layers, enable one at a time

    for i in el_index:

        # Enable active layer

        rl[i].use = True

        # Get file name

        basename = bpy.path.basename(bpy.context.blend_data.filepath)

        # Remove .blend extension

        basename = os.path.splitext(basename)[0]

        # build render file path with render layer in the name

        # ACES color space
        out_colorspace = "ACEScg"

        #filename = "//../rndr/blender/" + basename + "/" + rl[i].name + "/" + str(int(res_x)) + "x" + str(int(res_y)) + "/" + basename + "." + rl[i].name + "." + out_colorspace + ".%05d." % f
        filename = "//../rndr/blender/" + basename + "/" + basename + "." + rl[i].name + "." + str(int(res_x)) + "x" + str(int(res_y)) + "." + out_colorspace + ".%05d." % f

        # set output file path

        bpy.context.scene.render.filepath = filename

        # RENDER

        bpy.context.scene.frame_start = f
        bpy.context.scene.frame_end = f
        bpy.ops.render.render(write_still=True)

        # Deactivate layer

        rl[i].use = False

# Reset enabled layers

for i in el_index:
    rl[i].use = True

# Reset file path

bpy.context.scene.render.filepath = fp
