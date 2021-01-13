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
from random import uniform as ru
import numpy as np


class RandomColorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Random Color Panel"
    bl_idname = "OBJECT_PT_RandomColor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Let's make a random-color!")

        row = layout.row()
        row.label(text="Active object is: " + obj.name)

        row = layout.row()
        row.prop(context.scene, "input_frequency_rcolor") 
        
        row = layout.row()
        row.operator("shader.rcolor_operator", icon='COLORSET_02_VEC')
        
class RandomLocationPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Random Location Panel"
    bl_idname = "OBJECT_PT_RandomLocation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Let's random location!")

        row = layout.row()
        row.label(text="Active object is: " + obj.name)

        row = layout.row()
        row.operator("mesh.clear_location_operator", icon='TRASH')

        row = layout.row()
        row.label(text='Location:')
        row = layout.row()
        row.prop(context.scene, "input_location_x_min") 
        row.prop(context.scene, "input_location_x_max") 
        row = layout.row()
        row.prop(context.scene, "input_location_y_min") 
        row.prop(context.scene, "input_location_y_max") 
        row = layout.row()
        row.prop(context.scene, "input_location_z_min") 
        row.prop(context.scene, "input_location_z_max")
        
        row = layout.row()
        row.prop(context.scene, "input_frequency_rlocation") 

        row = layout.row()
        row = layout.row()
        row.operator("mesh.rlocation_operator", icon='EMPTY_DATA')
        
class RandomScalePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Random Scale Panel"
    bl_idname = "OBJECT_PT_RandomScale"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Let's random scale!")

        row = layout.row()
        row.label(text="Active object is: " + obj.name)

        row = layout.row()
        row.operator("mesh.clear_scale_operator", icon='TRASH')

        row = layout.row()
        row.label(text='Scale:')
        row = layout.row()
        row.prop(context.scene, "input_scale_x_min") 
        row.prop(context.scene, "input_scale_x_max") 
        row = layout.row()
        row.prop(context.scene, "input_scale_y_min") 
        row.prop(context.scene, "input_scale_y_max") 
        row = layout.row()
        row.prop(context.scene, "input_scale_z_min") 
        row.prop(context.scene, "input_scale_z_max")
        
        row = layout.row()
        row.prop(context.scene, "input_frequency_rscale") 

        row = layout.row()
        row = layout.row()
        row.operator("mesh.rscale_operator", icon='OBJECT_HIDDEN')

class SHADER_RANDOM_COLOR(bpy.types.Operator):
    bl_label = "Add Random Color Material"
    bl_idname = "shader.rcolor_operator"
    bl_description = "Create a new animated material with different color at every keyframe"
    bl_options = {"REGISTER", 'UNDO'}
    
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
        
        for i in np.arange(bpy.context.scene.frame_start, bpy.context.scene.frame_end, 
        context.scene.input_frequency_rscale):
            material_p_bsdf.inputs[0].keyframe_insert("default_value", frame=i)  # Base Color
            material_p_bsdf.inputs[0].default_value = (r(), r(), r(), 1) # Base Color
        
        
        tree.links.new(material_p_bsdf.outputs[0], material_output.inputs[0]) # Connect the shaders if not already
        
        bpy.context.object.active_material = material_rcolor
        return {'FINISHED'}
    
class OBJECT_RANDOM_LOCATION(bpy.types.Operator):
    bl_label = "Add Random Location Animation"
    bl_idname = "mesh.rlocation_operator"
    bl_description = "Create an animation to change the location of the selected object at every keyframe"
    bl_options = {"REGISTER", 'UNDO'}
    
    def execute(self, context):
        ob = bpy.context.active_object
        sc = bpy.context.scene
        d = ob.dimensions
        location_x = ob.location[0]
        location_y = ob.location[1]
        location_z = ob.location[2]
        for i in np.arange(bpy.context.scene.frame_start, bpy.context.scene.frame_end, 
        sc.input_frequency_rlocation):
            ob.keyframe_insert(data_path="location", frame=i)
            ob.location[0] = location_x + ru(sc.input_location_x_min, sc.input_location_x_max)
            ob.location[1] = location_y + ru(sc.input_location_y_min, sc.input_location_y_max)
            ob.location[2] = location_z + ru(sc.input_location_z_min, sc.input_location_z_max)            
        return {'FINISHED'}

    
class OBJECT_RANDOM_SCALE(bpy.types.Operator):
    bl_label = "Add Random Scale Animation"
    bl_idname = "mesh.rscale_operator"
    bl_description = "Create an animation to change the scale of the selected object at every keyframe"
    bl_options = {"REGISTER", 'UNDO'}
    
    def execute(self, context):
        ob = bpy.context.active_object
        sc = bpy.context.scene
        d = ob.dimensions
        scale_x = ob.scale[0]
        scale_y = ob.scale[1]
        scale_z = ob.scale[2]
        for i in np.arange(bpy.context.scene.frame_start, bpy.context.scene.frame_end, 
        sc.input_frequency_rscale):
            ob.keyframe_insert(data_path="scale", frame=i)
            ob.scale[0] = scale_x * ru(sc.input_scale_x_min, sc.input_scale_x_max)
            ob.scale[1] = scale_y * ru(sc.input_scale_y_min, sc.input_scale_y_max)
            ob.scale[2] = scale_z * ru(sc.input_scale_z_min, sc.input_scale_z_max)            
        return {'FINISHED'}

class OBJECT_DEFAULT_LOCATION(bpy.types.Operator):
    bl_label = "Clear location keyframes"
    bl_idname = "mesh.clear_location_operator"
    bl_description = "Remove all the location-keyframes" # and move to '3D cursor'"
    bl_options = {"REGISTER", 'UNDO'}
    
    def execute(self, context):
        ob = bpy.context.active_object
        ad = ob.animation_data

        if ad:
            action = ad.action
            if action:
                remove_types = ["location"]
                # select all that have datapath above
                fcurves = [fc for fc in action.fcurves
                        for type in remove_types
                        if fc.data_path.startswith(type)
                        ]
                # remove fcurves
                while(fcurves):
                    fc = fcurves.pop()
                    action.fcurves.remove(fc)
#        ob.location = [0, 0, 0]
#        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

        return {'FINISHED'}

class OBJECT_DEFAULT_SCALE(bpy.types.Operator):
    bl_label = "Clear scale keyframes"
    bl_idname = "mesh.clear_scale_operator"
    bl_description = "Remove all the Scale-keyframes make the default scale to 1"
    bl_options = {"REGISTER", 'UNDO'}
    
    def execute(self, context):
        ob = bpy.context.active_object
        ad = ob.animation_data

        if ad:
            action = ad.action
            if action:
                remove_types = ["scale"]
                # select all that have datapath above
                fcurves = [fc for fc in action.fcurves
                        for type in remove_types
                        if fc.data_path.startswith(type)
                        ]
                # remove fcurves
                while(fcurves):
                    fc = fcurves.pop()
                    action.fcurves.remove(fc)
        ob.scale = [1, 1, 1]
        return {'FINISHED'}



def register_input_variables():
    bpy.types.Scene.input_frequency_rcolor = bpy.props.IntProperty(
        name = "Frequency",
        description = "Change color after how many frames?",
        default = 1,
        min = 1,
        max = 10000
    )
    bpy.types.Scene.input_frequency_rlocation = bpy.props.IntProperty(
        name = "Frequency",
        description = "Change location after how many frames?",
        default = 1,
        min = 1,
        max = 10000
    )
    bpy.types.Scene.input_location_x_min = bpy.props.FloatProperty(
        name = "X min",
        description = "Set location x min",
        default = -1.0,
        min = -10000.0,
        max = 10000.0
    )
    bpy.types.Scene.input_location_x_max = bpy.props.FloatProperty(
        name = "X max",
        description = "Set location x max",
        default = 1.0,
        min = -10000.0,
        max = 10000.0
    )
    bpy.types.Scene.input_location_y_min = bpy.props.FloatProperty(
        name = "Y min",
        description = "Set location y min",
        default = -1.0,
        min = -10000.0,
        max = 10000.0
    )
    bpy.types.Scene.input_location_y_max = bpy.props.FloatProperty(
        name = "Y max",
        description = "Set location y max",
        default = 1.0,
        min = -10000.0,
        max = 10000.0
    )
    bpy.types.Scene.input_location_z_min = bpy.props.FloatProperty(
        name = "Z min",
        description = "Set location z min",
        default = -1.0,
        min = -10000.0,
        max = 10000.0
    )
    bpy.types.Scene.input_location_z_max = bpy.props.FloatProperty(
        name = "Z max",
        description = "Set location z max",
        default = 1.0,
        min = -10000.0,
        max = 10000.0
    )
    
    bpy.types.Scene.input_frequency_rscale = bpy.props.IntProperty(
        name = "Frequency",
        description = "Change scale after how many frames?",
        default = 1,
        min = 1,
        max = 10000
    )
    bpy.types.Scene.input_scale_x_min = bpy.props.FloatProperty(
        name = "X min",
        description = "Set scale x min",
        default = 0.9,
        min = 0.0,
        max = 10000.0
    )
    bpy.types.Scene.input_scale_x_max = bpy.props.FloatProperty(
        name = "X max",
        description = "Set scale x max",
        default = 1.1,
        min = 0.0,
        max = 10000.0
    )
    bpy.types.Scene.input_scale_y_min = bpy.props.FloatProperty(
        name = "Y min",
        description = "Set scale y min",
        default = 0.9,
        min = 0.0,
        max = 10000.0
    )
    bpy.types.Scene.input_scale_y_max = bpy.props.FloatProperty(
        name = "Y max",
        description = "Set scale y max",
        default = 1.1,
        min = 0.0,
        max = 10000.0
    )
    bpy.types.Scene.input_scale_z_min = bpy.props.FloatProperty(
        name = "Z min",
        description = "Set scale z min",
        default = 0.9,
        min = 0.0,
        max = 10000.0
    )
    bpy.types.Scene.input_scale_z_max = bpy.props.FloatProperty(
        name = "Z max",
        description = "Set scale z max",
        default = 1.1,
        min = 0.0,
        max = 10000.0
    )
    

def unregister_input_variables():
    del bpy.types.Scene.input_frequency_rcolor
    del bpy.types.Scene.input_frequency_rlocation
    del bpy.types.Scene.input_location_x_min
    del bpy.types.Scene.input_location_x_max
    del bpy.types.Scene.input_location_y_min
    del bpy.types.Scene.input_location_y_max
    del bpy.types.Scene.input_location_z_min
    del bpy.types.Scene.input_location_z_max
    del bpy.types.Scene.input_frequency_rscale
    del bpy.types.Scene.input_scale_x_min
    del bpy.types.Scene.input_scale_x_max
    del bpy.types.Scene.input_scale_y_min
    del bpy.types.Scene.input_scale_y_max
    del bpy.types.Scene.input_scale_z_min
    del bpy.types.Scene.input_scale_z_max

def register():
    bpy.utils.register_class(RandomColorPanel)
    bpy.utils.register_class(SHADER_RANDOM_COLOR)
    bpy.utils.register_class(RandomLocationPanel)
    bpy.utils.register_class(OBJECT_RANDOM_LOCATION)
    bpy.utils.register_class(OBJECT_DEFAULT_LOCATION)
    bpy.utils.register_class(RandomScalePanel)
    bpy.utils.register_class(OBJECT_RANDOM_SCALE)
    bpy.utils.register_class(OBJECT_DEFAULT_SCALE)
#    bpy.utils.register_class(OBJECT_DEFAULT_COLOR)
    register_input_variables()

def unregister():
    bpy.utils.unregister_class(RandomColorPanel)
    bpy.utils.unregister_class(SHADER_RANDOM_COLOR)
    bpy.utils.unregister_class(RandomLocationPanel)
    bpy.utils.unregister_class(OBJECT_RANDOM_LOCATION)
    bpy.utils.unregister_class(OBJECT_DEFAULT_LOCATION)
    bpy.utils.unregister_class(RandomScalePanel)
    bpy.utils.unregister_class(OBJECT_RANDOM_SCALE)
    bpy.utils.unregister_class(OBJECT_DEFAULT_SCALE)
#    bpy.utils.unregister_class(OBJECT_DEFAULT_COLOR)
    unregister_input_variables()


if __name__ == "__main__":
    register()
