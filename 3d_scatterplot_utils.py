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
