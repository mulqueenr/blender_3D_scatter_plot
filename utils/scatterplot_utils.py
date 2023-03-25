#1. import modules
import bpy
import math
import time
import bmesh
import os, sys
import addon_utils
import csv
import numpy

addon_path=[mod.__file__ for mod in addon_utils.modules() if "blender_3D_scatter_plot" in mod.__file__] #get a list of all add-ons and return this one
test_data_path = addon_path[0].replace("__init__.py","test_data/test.tsv") #replace init file with test data directory and file


#use this for import https://github.com/simonbroggi/blender_spreadsheet_import/blob/main/__init__.py
def set_camera():
  """Move the camera and rotate."""
  bpy.data.objects["Camera"].location=(40, -40, 38)
  bpy.data.objects["Camera"].rotation_euler=(1, 0.0, 0.8)


def set_render_and_scene():
  """Automate setting up high quality render and scene."""
  #set up render engine and scene
  bpy.context.scene.render.engine="CYCLES" #set render engine to CYCLES
  bpy.data.scenes["Scene"].cycles.samples=512 #this is a whole lotta sampling
  bpy.context.scene.render.image_settings.color_depth = '16' #more color channels!
  bpy.context.scene.render.resolution_x = 3840 #up the resolution
  bpy.context.scene.render.resolution_y = 2160
  bpy.data.lights["Light"].energy = 10000 # increase light wattage
  bpy.data.lights["Light"].shadow_soft_size= 1
  bpy.data.objects["Light"].location=(5,-5,10) #location and rotation i deteremined manually and just set up here for convenience

################################ UPDATED v1.1 ###################################################################

def read_tsv(file_path):
    '''Read in TSV file, this is from Erindale https://www.youtube.com/watch?v=xWwoWi_vPTg&t=1737s'''
    with open(file_path,'r') as f:
        reader=csv.reader(f,delimiter="\t")
        data=list(reader)
        return(data)

def tsv_column(data,col):
    '''Parse TSV data by index as array
    This is from Erindale https://www.youtube.com/watch?v=xWwoWi_vPTg&t=1737s'''
    array=[]
    for y, row in enumerate(data):
        if y==0:
            continue
        array.append(row[col])
    return(array)

def color_splitter(array_in):
    '''Parse hex color code to split out r g and b for colors'''
    array=[]
    r_array=[]
    g_array=[]
    b_array=[]
    for i in array_in:
        hexcode=i.lstrip("#")
        rgb=[int(hexcode[i:i+2], 16) for i in (0, 2, 4)]
        r_array.append(float(rgb[0])/255) #color of spheres, blender uses 0-1 scale
        g_array.append(float(rgb[1])/255)
        b_array.append(float(rgb[2])/255)
    array=[r_array,g_array,b_array]
    return(array)

def create_object(mesh, name):
    """ https://github.com/simonbroggi/blender_spreadsheet_import/blob/main/__init__.py"""
    # Create new object
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

def set_up_stage():
    """Set up stage by cutting up the default cube vertices and smoothing it."""
    if "Cube" not in [i.name for i in list(bpy.data.objects)]:
        bpy.ops.mesh.primitive_cube_add()
    obj_cube=bpy.data.objects["Cube"]
    obj_cube.scale=(30,30,30) #scale up the cube
    #this is to cut out a vertex to make an open box
    bpy.context.view_layer.objects.active = obj_cube
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")  # Switch to edge select mode
    bm = bmesh.from_edit_mesh(obj_cube.data)  # Create bmesh object for easy mesh evaluation
    bm.verts.ensure_lookup_table()
    bm.verts.remove(bm.verts[2]) # Write the mesh back
    bmesh.update_edit_mesh(obj_cube.data)  # Update the mesh in edit mode
    bpy.ops.object.mode_set(mode='OBJECT') #switch back to object mode when done
    bpy.ops.object.modifier_add(type='SUBSURF') #make it smooth
    bpy.data.objects["Cube"].modifiers["Subdivision"].render_levels=6
    bpy.data.objects["Cube"].location=(-4,4.3,17.725) #change the location for more dramatic shadows
  
def run_3dscatterplot(file_in,file_out_dir,file_out_name):
    """This is the main function, which wraps all others. Reads in file, assigns space based on file data, and assigns a material per cluster"""
    #Read in file and separate out columns to lists
    #file_in="/Users/rmulqueen/Library/Application Support/Blender/3.4/scripts/addons/blender_3D_scatter_plot-main/test_data/test.tsv"
    dat=read_tsv(file_in)
    n_points=len(dat)
    grouping=tsv_column(data=dat,col=0)
    cellid=tsv_column(data=dat,col=1)
    x=[float(i) for i in tsv_column(data=dat,col=2)]
    y=[float(i) for i in tsv_column(data=dat,col=3)]
    z=[float(i) for i in tsv_column(data=dat,col=4)]
    #Split out colors to rgb components
    color_in=tsv_column(data=dat,col=5)
    color_in=color_splitter(array_in=color_in)
    r=color_in[0]
    g=color_in[1]
    b=color_in[2]
    a=[0.9 for x in color_in[0]]
    color_in=[]
    for i in range(0,len(r)-1):
         color_in.append(float(r[i]))
         color_in.append(float(g[i]))
         color_in.append(float(b[i]))
         color_in.append(float(a[i]))
    set_render_and_scene()   #set up render engine and scene
    set_up_stage()   #set up stage by cutting up the default cube vertices and smoothing it
    set_camera()  #move the camera and rotate
    #Instance a new object and add attributes
    mesh = bpy.data.meshes.new(name="csv_data")
    mesh.vertices.add(n_points)
    mesh.update() 
    object_name = bpy.path.display_name("Scatterplot")
    create_object(mesh, object_name)
    #Set position per vertex
    for i in range(0,n_points-1):
        mesh.vertices[i].co = (x[i],y[i],z[i])
    #Set color per vertex
    colattr = bpy.data.meshes[mesh.name].attributes.new("color","FLOAT_COLOR","POINT")
    for i in range(0,n_points-1):
        colattr.data[i].color = [r[i], g[i], b[i], 1]
    obj=bpy.data.objects["Scatterplot"]
    #Initiate a geometry nodes modifier
    obj.modifiers.new("make_vertices","NODES")
    geo_nodes=obj.modifiers["make_vertices"]
    #bpy.data.node_groups.new("make_vertices","GeometryNodeTree")
    #Initialize geometry nodes
    bpy.ops.node.new_geometry_node_group_assign()
    bpy.data.node_groups[0].name="make_vertices"
    geo_nodes.node_group = bpy.data.node_groups["make_vertices"]
    #Add group input
    nodetree=geo_nodes.node_group #fix this. doesnt properly initialize nodes
    #Add geo nodes and link
    inNode=nodetree.nodes['Group Input']
    outNode=nodetree.nodes['Group Output']
    pointsnode=nodetree.nodes.new(type="GeometryNodeInstanceOnPoints") #add points node
    icosnode=nodetree.nodes.new(type="GeometryNodeMeshIcoSphere") #add ico
    icosnode.inputs['Radius'].default_value=0.05
    icosnode.inputs['Subdivisions'].default_value=4
    scenetimenode=nodetree.nodes.new(type="GeometryNodeInputSceneTime") #add scene time
    setpositionnode=nodetree.nodes.new(type="GeometryNodeSetPosition") #add set position
    setmaterialnode=nodetree.nodes.new(type="GeometryNodeSetMaterial") #add set material
    voroninode=nodetree.nodes.new(type="ShaderNodeTexVoronoi") #add voroni texture
    voroninode.voronoi_dimensions = '4D'
    voroninode.inputs['Scale'].default_value = 1
    #add subdivision icosphere
    pointsnode.location=(-100,-300) #move points node
    icosnode.location=(-300,-500)
    scenetimenode.location=(-100,100)
    voroninode.location=(0,400)
    setpositionnode.location=(100,100)
    setmaterialnode.location=(300,300)
    outNode.location=(500,100)
    bpy.data.node_groups["make_vertices"].nodes["Voronoi Texture"].name
    nodetree.links.new(inNode.outputs['Geometry'], pointsnode.inputs['Points']) #link input counts to points
    nodetree.links.new(icosnode.outputs['Mesh'], pointsnode.inputs['Instance']) #link input positions to points
    nodetree.links.new(pointsnode.outputs['Instances'], setpositionnode.inputs['Geometry']) #link input positions to points
    nodetree.links.new(pointsnode.outputs['Instances'], setpositionnode.inputs['Geometry']) #link input positions to points
    nodetree.links.new(scenetimenode.outputs['Seconds'], voroninode.inputs['W']) #link scene time to random value to animate
    nodetree.links.new(voroninode.outputs['Distance'], setpositionnode.inputs['Offset']) #link random distance to offset to move points
    nodetree.links.new(setpositionnode.outputs['Geometry'], setmaterialnode.inputs['Geometry']) #link input positions to points
    nodetree.links.new(setmaterialnode.outputs['Geometry'], outNode.inputs['Geometry']) #link input positions to points
    #Initialize shader nodes
    # Get material
    mat = bpy.data.materials.get("scattermat")
    if mat is None:
        mymat=bpy.data.materials.new("scattermat")     # create material
    mymat.use_nodes = True
    # Assign it to object
    if obj.data.materials:
        obj.data.materials[0] = mymat    # assign to 1st material slot
    else:
        obj.data.materials.append(mymat)     # no slots
    shadernodes = mymat.node_tree.nodes
    attr_node = shadernodes.new('ShaderNodeAttribute')
    bsdf_node=shadernodes['Principled BSDF']
    attr_node.location=(-300,-300) #move points node
    attr_node.attribute_type = 'INSTANCER'
    attr_node.attribute_name = "color"
    mymat.node_tree.links.new(attr_node.outputs['Color'], bsdf_node.inputs['Base Color']) #link input counts to points
    setmaterialnode.inputs['Material'].default_value = bpy.data.materials["scattermat"] #assign this scattermat material to the geonode attribute
