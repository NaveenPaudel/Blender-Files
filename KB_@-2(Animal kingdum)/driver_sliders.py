bl_info = {
    "name": "Driver Sliders with Safe Reset (Matrix-Based)",
    "author": "Santosh Wagle",
    "version": (1, 2),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Driver Tools",
    "description": "Driver sliders with FK→IK reset that preserves pose using matrix restore",
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

    # 🔹 NEW SLIDERS (-100 to +100)
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
# SAFE RESET OPERATOR (POSE PRESERVE ONLY)
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

        # Store evaluated pose matrices
        bone_matrices = {
            pb.name: pb.matrix.copy()
            for pb in obj.pose.bones
        }

        # Reset slider
        scene.slider_2 = 0.0
        context.view_layer.update()

        # Restore pose
        for pb in obj.pose.bones:
            mat = bone_matrices.get(pb.name)
            if mat:
                pb.matrix = mat

        context.view_layer.update()
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
        row.operator(
            "driver.reset_slider_2_safe",
            text="",
            icon='LOOP_BACK'
        )

        layout.prop(scene, "slider_3", slider=True)

        layout.separator()
        layout.label(text="Extra Sliders")

        layout.prop(scene, "slider_4", slider=True)
        layout.prop(scene, "slider_5", slider=True)
        layout.prop(scene, "slider_6", slider=True)
        layout.prop(scene, "slider_7", slider=True)


# ------------------------------------------------
# REGISTER
# ------------------------------------------------
classes = (
    VIEW3D_PT_driver_slider_panel,
    DRIVER_OT_reset_slider_2_safe,
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
