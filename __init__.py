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

#1. import modules
import bpy
import math
import time
import bmesh
import os, sys
import addon_utils

addon_path=[mod.__file__ for mod in addon_utils.modules() if "blender_3D_scatter_plot" in mod.__file__] #get a list of all add-ons and return this one
test_data_path = addon_path[0].replace("__init__.py","test_data/test.tsv") #replace init file with test data directory and file

#2. Utilities for 3D Scatter Plot Making
#Update in future for readability. Move functions to new folder
from .utils.scatterplot_utils import *


#3. Properties for scene
PROPS = [
    ("filepath_3dfile",bpy.props.StringProperty(
        name="File input",
        subtype='FILE_PATH',
        default=test_data_path)),
    ("fileout_dir",bpy.props.StringProperty(
        name="Path for output",
        subtype='FILE_PATH',
        default="/Users/rmulqueen/Desktop/")),
    ("file_name_out",bpy.props.StringProperty(
        name="Output file prefix",
        default="test"))
]

#4. Classes
class MESH_OT_3d_scatterplot(bpy.types.Operator):
    """Take a tsv input and make 3D Scatter Plot."""
    bl_idname = "mesh.scatterplot_3d"
    bl_label = "3D Scatterplot"
    bl_options = {'REGISTER','UNDO'}
    def execute(self, context):
        props=context.scene
        run_3dscatterplot(file_in=props.filepath_3dfile,
            file_out_dir=props.fileout_dir,
            file_out_name=props.file_name_out)
        return {'FINISHED'}


class VIEW3D_PT_3d_scatterplot(bpy.types.Panel):
    """Panel for DNA Molecule Builder"""
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="3D Scatterplot"
    bl_label="Add Scatterplot"
    def draw(self,context):
        layout = self.layout
        #Initial default option for messing with gDNA
        col = layout.row()
        layout.label(text="Input")
        for prop_name in ["filepath_3dfile"]:
            col = layout.row()
            col.prop(context.scene, prop_name)
        col = layout.row()
        layout.label(text="Output")
        for prop_name in ["fileout_dir","file_name_out"]:
            col = layout.row()
            col.prop(context.scene, prop_name)
        col =layout.row()
        col.operator('mesh.scatterplot_3d',
            text="Generate 3D Plot",
            icon="RNA")

#5. Register
CLASSES = [
    MESH_OT_3d_scatterplot,
    VIEW3D_PT_3d_scatterplot
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
