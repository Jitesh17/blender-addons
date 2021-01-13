bl_info = {
    "name" : "Random",
    "author" : "Jitesh Gosar",
    "version" : (1, 0),
    "blender" : (2, 91, 0),
    "location" : "View3d",
    "warning" : "",
    "category" : "Material",
}
    


import bpy
from random import random as r
import numpy as np


class RandomColorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Random Color Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random Material"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Let's make a random-color material!", 
#        icon='COLORSET_08_VEC'
        )

        row = layout.row()
        row.label(text="Active object is: " + obj.name)

        row = layout.row()
        row.prop(obj, "Last Frame")

        row = layout.row()
        row.operator("shader.rcolor_operator", icon='COLORSET_02_VEC')

class SHADER_RANDOM_COLOR(bpy.types.Operator):
    bl_label = "Add Random Color Material"
    bl_idname = "shader.rcolor_operator"
    bl_options = {"REGISTER", 'UNDO'}
    
#    frameInterval: bpy.props.IntProperty(
#        name= "Frame Interval",
#        default = 1,
#        min = 1,
#        max = bpy.context.scene.frame_end,
#        description = "",
#    )
    
    def execute(self, context):
        material_rcolor = bpy.data.materials.new(name="RandomColor")
        material_rcolor.use_nodes = True
        
        tree = material_rcolor.node_tree
        
#        material_rcolor.node_tree.nodes.remove(material_rcolor.node_tree.nodes.get('Principled BSDF'))
#        material_p_bsdf = material_rcolor.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
#        material_p_bsdf = material_rcolor.node_tree.nodes.new('ShaderNodeEmission')
#        material_output = material_rcolor.node_tree.nodes.new('ShaderNodeOutputMaterial')
#        material_output.location = (400,0)

        material_p_bsdf = tree.nodes.get('Principled BSDF')
        material_output = tree.nodes.get('Material Output')
        material_p_bsdf.inputs[0].default_value = (1, 1, 1, 1) # Base Color
        
        for i in np.arange(bpy.context.scene.frame_start, bpy.context.scene.frame_end, 1):
            material_p_bsdf.inputs[0].keyframe_insert("default_value", frame=i)  # Base Color
            material_p_bsdf.inputs[0].default_value = (r(), r(), r(), 1) # Base Color
        
        
        tree.links.new(material_p_bsdf.outputs[0], material_output.inputs[0]) # Connect the shaders if not already
        
        bpy.context.object.active_material = material_rcolor
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RandomColorPanel)
    bpy.utils.register_class(SHADER_RANDOM_COLOR)


def unregister():
    bpy.utils.unregister_class(RandomColorPanel)
    bpy.utils.unregister_class(SHADER_RANDOM_COLOR)


if __name__ == "__main__":
    register()
