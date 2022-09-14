#Utilities for 3D Scatter Plot Making
def make_master_shader():
  """Set up master shader (named mymat) to be used on all data points."""
  #set up a master shader material
  mat = bpy.data.materials.new(name='mymat')
  mat.use_nodes = True #use node trees, these can be seen by switching a panel to the shader editor if you want. It will look like the above shader, just not nicely placed.
  mat_nodes = mat.node_tree.nodes
  mat_links = mat.node_tree.links
  mat = bpy.data.materials['mymat'] #Get the material you want 
  node_to_delete =  mat.node_tree.nodes['Principled BSDF'] #Get the node in its node tree (replace the name below)
  mat.node_tree.nodes.remove( node_to_delete ) #Remove it
  #add all the nodes, using col_node as variable of each node as it is being made. then using that to modify default value fields
  col_node=mat_nodes.new('ShaderNodeRGB')
  col_node=mat_nodes.new('ShaderNodeFresnel')
  bpy.data.materials["mymat"].node_tree.nodes['Fresnel'].inputs[0].default_value = 1.33
  col_node=mat_nodes.new('ShaderNodeHueSaturation')
  bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value"].inputs[0].default_value = 1
  bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value"].inputs[1].default_value = 0.7
  bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value"].inputs[2].default_value = 2
  bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value"].inputs[3].default_value = 0
  col_node=mat_nodes.new('ShaderNodeMath')
  bpy.data.materials["mymat"].node_tree.nodes["Math"].operation = 'MULTIPLY'
  col_node=mat_nodes.new('ShaderNodeBsdfRefraction')
  bpy.data.materials["mymat"].node_tree.nodes["Refraction BSDF"].inputs[1].default_value = 1
  col_node=mat_nodes.new('ShaderNodeBsdfGlossy')
  bpy.data.materials["mymat"].node_tree.nodes["Glossy BSDF"].inputs[1].default_value = 1
  col_node=mat_nodes.new('ShaderNodeHueSaturation')
  bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value.001"].inputs[0].default_value = 1
  bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value.001"].inputs[1].default_value = 0.4
  bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value.001"].inputs[2].default_value = 2
  col_node=mat_nodes.new('ShaderNodeMixShader')
  col_node=mat_nodes.new('ShaderNodeVolumeAbsorption')
  bpy.data.materials["mymat"].node_tree.nodes["Volume Absorption"].inputs[1].default_value = 0.3
  col_node=mat_nodes.new('ShaderNodeBsdfTranslucent')
  col_node=mat_nodes.new('ShaderNodeLightPath')
  col_node=mat_nodes.new('ShaderNodeMixShader')
  #build node tree links (going from left most inputs)
  #sorry this is a monstrosity
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes['RGB'].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value"].inputs[4])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes['RGB'].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value.001"].inputs[4])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes['RGB'].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Volume Absorption"].inputs[0])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes['Fresnel'].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Math"].inputs[0])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes['Hue Saturation Value'].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Refraction BSDF"].inputs[0])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes['Hue Saturation Value'].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Glossy BSDF"].inputs[0])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Math"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Mix Shader"].inputs[0])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Refraction BSDF"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Mix Shader"].inputs[1])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Glossy BSDF"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Mix Shader"].inputs[2])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Hue Saturation Value.001"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Translucent BSDF"].inputs[0])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Volume Absorption"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Material Output"].inputs[1])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Translucent BSDF"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Mix Shader.001"].inputs[2])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Mix Shader"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Mix Shader.001"].inputs[1])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Light Path"].outputs[1], bpy.data.materials["mymat"].node_tree.nodes["Mix Shader.001"].inputs[0])
  mat_links.new(bpy.data.materials["mymat"].node_tree.nodes["Mix Shader.001"].outputs[0], bpy.data.materials["mymat"].node_tree.nodes["Material Output"].inputs[0])

  
def set_render_and_scene():
  """Automate setting up high quality render and scene."""
  #set up render engine and scene
  bpy.context.scene.render.engine="CYCLES" #set render engine to CYCLES
  bpy.data.scenes["Scene"].cycles.denoiser="NLM" #set denoiser for render
  bpy.data.scenes["Scene"].cycles.samples=512 #this is a whole lotta sampling
  bpy.context.scene.render.image_settings.color_depth = '16' #more color channels!
  bpy.context.scene.render.resolution_x = 3840 #up the resolution
  bpy.context.scene.render.resolution_y = 2160
  bpy.data.objects["Sphere"].hide_render = True # hide sphere in render
  bpy.data.objects["Sphere"].hide_viewport=True
  bpy.data.lights["Light"].energy = 100000 # increase light wattage
  bpy.data.lights["Light"].shadow_soft_size= 1
  bpy.data.objects["Light"].location=(5,-5,10) #location and rotation i deteremined manually and just set up here for convenience

def set_up_stage():
  """Set up stage by cutting up the default cube vertices and smoothing it."""
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
  
  
def set_camera():
  """Move the camera and rotate."""
  bpy.data.objects["Camera"].location=(34.61997604370117, -40.53969955444336, 25.66326904296875)
  bpy.data.objects["Camera"].rotation_euler=(1.1093189716339111, 0.0, 0.8149281740188599)

  
def add_data_point(input_dat):
    """Copy data points and link them to the master spheres. 
    Also places the copies into nice cluster named collections for easier navigation."""
    line=input_dat
    line=line.replace('\n','')
    l=line.split('\t')
    #print(line)
    x=float(l[2]) #location of spheres
    y=float(l[3])
    z=float(l[4])
    name=str(l[1])
    clust=str(l[0])
    my_new_obj = bpy.data.objects.new(name,master_sphere[clust])
    my_new_obj.location = (x,y,z)       
    my_new_obj.hide_viewport=False
    my_new_obj.hide_render=False
    bpy.data.collections[clust].objects.link(my_new_obj)
