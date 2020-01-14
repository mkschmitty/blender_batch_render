# blender_batch_render

This commandline script renders all activated View Layers of your Blender 2.8 scene


Usage:  

**blender --background path to blender scene --python batch_render.py -- start_frame end_frame step cpus**


To submit to the render farm with qube, use this in the Command field of a cmdrange job:

**blender --background path to blender scene --python path to blender batch script -- QB_FRAME_START QB_FRAME_END QB_FRAME_STEP cpus**
  

