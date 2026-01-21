bl_info = {
    "name": "Driver Sliders with Safe Reset (Matrix-Based)",
    "author": "Santosh Wagle",
    "version": (1, 3),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Driver Tools",
    "description": "Driver sliders with FK→IK reset + optional NLA strip driver binding",
    "category": "Animation",
}

import bpy


# ------------------------------------------------
# DRIVER SLIDER PROPERTIES
# ------------------------------------------------
def register_props():
    bpy.types.Scene.ik_fk_switch = bpy.props.FloatProperty(
        name="IK/FK Switch",
        min=0.0, max=1.0,
        default=0.0
    )

    bpy.types.Scene.slider_2 = bpy.props.FloatProperty(
        name="Fk_to_IK",
        min=0.0, max=1.0,
        default=1.0
    )

    bpy.types.Scene.slider_3 = bpy.props.FloatProperty(
        name="Extra",
        min=0.0, max=1.0,
        default=0.0
    )

    bpy.types.Scene.slider_4 = bpy.props.FloatProperty(
        name="Elephant",
        min=-100.0, max=100.0,
        default=0.0
    )

    bpy.types.Scene.slider_5 = bpy.props.FloatProperty(
        name="Snake",
        min=-100.0, max=100.0,
        default=0.0
    )

    bpy.types.Scene.slider_6 = bpy.props.FloatProperty(
        name="Frog",
        min=-100.0, max=100.0,
        default=0.0
    )

    bpy.types.Scene.slider_7 = bpy.props.FloatProperty(
        name="Ant",
        min=-100.0, max=100.0,
        default=0.0
    )


def unregister_props():
    del bpy.types.Scene.ik_fk_switch
    del bpy.types.Scene.slider_2
    del bpy.types.Scene.slider_3
    del bpy.types.Scene.slider_4
    del bpy.types.Scene.slider_5
    del bpy.types.Scene.slider_6
    del bpy.types.Scene.slider_7


# ------------------------------------------------
# SAFE RESET OPERATOR (UNCHANGED)
# ------------------------------------------------
class DRIVER_OT_reset_slider_2_safe(bpy.types.Operator):
    bl_idname = "driver.reset_slider_2_safe"
    bl_label = "Reset FK→IK (Safe)"
    bl_description = "Reset FK→IK slider without changing pose"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'ARMATURE' and context.mode == 'POSE'

    def execute(self, context):
        scene = context.scene
        obj = context.object

        bone_matrices = {
            pb.name: pb.matrix.copy()
            for pb in obj.pose.bones
        }

        scene.slider_2 = 0.0
        context.view_layer.update()

        for pb in obj.pose.bones:
            mat = bone_matrices.get(pb.name)
            if mat:
                pb.matrix = mat

        context.view_layer.update()
        return {'FINISHED'}


# ------------------------------------------------
# 🆕 NLA DRIVER BIND OPERATOR (ADDED)
# ------------------------------------------------
class DRIVER_OT_bind_nla_strip(bpy.types.Operator):
    bl_idname = "driver.bind_nla_strip"
    bl_label = "Bind Selected NLA Strips"
    bl_description = "Bind selected NLA strip influence to slider_2"

    def execute(self, context):
        obj = context.object
        if not obj or not obj.animation_data:
            return {'CANCELLED'}

        for track in obj.animation_data.nla_tracks:
            for strip in track.strips:
                if strip.select:
                    fcurve = strip.driver_add("influence")
                    driver = fcurve.driver
                    driver.type = 'SCRIPTED'
                    driver.expression = "var"

                    var = driver.variables.new()
                    var.name = "var"
                    var.type = 'SINGLE_PROP'
                    target = var.targets[0]
                    target.id_type = 'SCENE'
                    target.id = context.scene
                    target.data_path = "slider_2"

        return {'FINISHED'}


# ------------------------------------------------
# UI PANEL
# ------------------------------------------------
class VIEW3D_PT_driver_slider_panel(bpy.types.Panel):
    bl_label = "Driver Sliders"
    bl_idname = "VIEW3D_PT_driver_slider_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Driver Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "ik_fk_switch", slider=True)

        row = layout.row(align=True)
        row.prop(scene, "slider_2", slider=True)
        row.operator("driver.reset_slider_2_safe", text="", icon='LOOP_BACK')

        layout.prop(scene, "slider_3", slider=True)

        layout.separator()
        layout.label(text="Extra Sliders")

        layout.prop(scene, "slider_4", slider=True)
        layout.prop(scene, "slider_5", slider=True)
        layout.prop(scene, "slider_6", slider=True)
        layout.prop(scene, "slider_7", slider=True)

        layout.separator()
        layout.operator("driver.bind_nla_strip", icon='NLA')


# ------------------------------------------------
# REGISTER
# ------------------------------------------------
classes = (
    VIEW3D_PT_driver_slider_panel,
    DRIVER_OT_reset_slider_2_safe,
    DRIVER_OT_bind_nla_strip,
)


def register():
    register_props()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_props()


if __name__ == "__main__":
    register()
