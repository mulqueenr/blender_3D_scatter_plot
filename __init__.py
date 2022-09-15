bl_info = {
    "name": "3D Scatter Plots",
    "author": "Ryan Mulqueen <RMulqueen@mdanderson.org",
    "version": (0, 2),
    "blender": (3, 2, 2),
    "location": "View3D",
    "description": "Adds a menu to upload points for a easy-to-initiate 3D Scatter Plot.",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
}

####I think maybe change the prop names? And try with all the functions in the same file??
#1. import modules
import bpy
import math
import time
import bmesh
from .utils.scatterplot_utils import *

import os, sys

class MESH_OT_3D_SCATTERPLOT(bpy.types.Operator):
    """Build out DNA molecules"""
    bl_idname="mesh.3d_scatterplot"
    bl_label="3D Scatterplot"
    bl_options={'REGISTER','UNDO'}
    def excecute(self,context):
        props=context.scene
        run_3dscatterplot(file_in=props.filepath_3dfile,
          file_out_dir=props.fileout_dir,
          file_out_name=props.file_name_out)  
        return {'FINISHED'}


class VIEW3D_PT_3D_SCATTERPLOT(bpy.types.Panel):
    """Panel for DNA Molecule Builder"""
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="3D Scatterplot"
    bl_label="Add Scatterplot"

    def draw(self,context):
        layout = self.layout
        obj =  context.active_object
        #Initial default option for messing with gDNA
        col = layout.row()
        for prop_name in ["filepath_3dfile","fileout_dir","file_name_out"]:
            col = layout.row()
            col.prop(context.scene, prop_name)
        col =layout.row()
        col.operator('mesh.3d_scatterplot',
            text="3D Plot",
            icon="RNA")

PROPS = [
    ("filepath_3dfile",bpy.props.StringProperty(
        name="File input",
        subtype='FILE_PATH')),
    ("fileout_dir",bpy.props.StringProperty(
        name="Path for output",
        subtype='FILE_PATH')),
    ("file_name_out",bpy.props.StringProperty(
        name="Output file prefix"))
]

CLASSES = [
    MESH_OT_3D_SCATTERPLOT,
    VIEW3D_PT_3D_SCATTERPLOT
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)
    for (prop_name, prop_value) in PROPS:
        delattr(bpy.types.Scene, prop_name)




#some last minute tweaks, here are some convenience functions if you want to change things. I also encourage you to play around with lighting and camera positioning to get some interesting views of your data.
#to adjust size of points
#for clust in annot.keys():
#  for i in bpy.data.collections[clust].objects:
#    i.scale=(0.8,0.8,0.8)


#to adjust alpha value and translucence of material properties
#for clust in annot.keys():
#  bpy.data.materials[clust].node_tree.nodes["RGB"].outputs[0].default_value[3] = 0.3
#  bpy.data.materials[clust].node_tree.nodes["Volume Absorption"].inputs[1].default_value = 0.1


