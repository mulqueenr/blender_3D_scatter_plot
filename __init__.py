bl_info = {
    "name": "3D Scatter Plots",
    "author": "Ryan Mulqueen",
    "version": (0, 1),
    "blender": (3, 2, 2),
    "location": "View3D",
    "description": "Adds a menu to upload points for a easy-to-initiate 3D Scatter Plot.",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
}

#1. import modules
import bpy
import math
import time
import bmesh
from .3d_scatterplot_utils import *
import os, sys


class MESH_OT_3D_SCATTERPLOT(bpy.types.Operator):
    """Build out DNA molecules"""
    bl_idname="mesh.3d_scatterplot"
    bl_label="3D Scatterplot"
    bl_options={'REGISTER','UNDO'}

    filepath_3dfile: bpy.props.StringProperty(
        name="File input:",
        subtype='FILE_PATH',
    )
    fileout_dir: bpy.props.StringProperty(
        name="Path for output:",
        subtype='FILE_PATH',
    )
    file_name_out: bpy.props.StringProperty(
        name="File Output Name",
    )

    def excecute(self,context):
        run_3dscatterplot(file_in=self.filepath_3dfile,
          file_out_dir=self.fileout_dir,
          file_out_name=self.file_name_out)
        
        return {'FINISHED'}


class VIEW3D_PT_3D_SCATTERPLOT(bpy.types.Panel):
    """Panel for DNA Molecule Builder"""
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="3D Scatterplot"
    bl_label="Add Scatterplot"

    def draw(self,context):
        self.layout.operator('mesh.3d_scatterplot')
        pass


def register():
    print("Registered DNA Builder")
    bpy.utils.register_class(MESH_OT_3d_scatterplot)
    bpy.utils.register_class(VIEW3D_PT_3d_scatterplot)

def unregister():
    print("Unregistered DNA Builder")
    bpy.utils.unregister_class(MESH_OT_3d_scatterplot)
    bpy.utils.unregister_class(VIEW3D_PT_3d_scatterplot)



#some last minute tweaks, here are some convenience functions if you want to change things. I also encourage you to play around with lighting and camera positioning to get some interesting views of your data.
#to adjust size of points
#for clust in annot.keys():
#  for i in bpy.data.collections[clust].objects:
#    i.scale=(0.8,0.8,0.8)


#to adjust alpha value and translucence of material properties
#for clust in annot.keys():
#  bpy.data.materials[clust].node_tree.nodes["RGB"].outputs[0].default_value[3] = 0.3
#  bpy.data.materials[clust].node_tree.nodes["Volume Absorption"].inputs[1].default_value = 0.1


