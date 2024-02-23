import bpy

from ... import dependencies, utils

from .SKYLIGHT_OT_rebuild_world import SKYLIGHT_OT_rebuild_world
from .SKYLIGHT_OT_update_world import SKYLIGHT_OT_update_world


class SKYLIGHT_PT_main(bpy.types.Panel):
    """Allows the user to update time and space coordinates and recalculate properties used by Skylight's world shader."""
    bl_label = "Skylight Environment Builder"
    bl_category = "Skylight"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    @classmethod
    def poll(self, context):
        return dependencies.satisfied()


    def draw(self, context):
        layout = self.layout
        layout.operator(SKYLIGHT_OT_rebuild_world.bl_idname)
        if context.scene.world:
            layout.prop(context.scene.world, '["date_time"]')
            layout.prop(context.scene.world, '["latitude"]')
            layout.prop(context.scene.world, '["longitude"]')
            layout.prop(context.scene.world, '["elevation"]')
            layout.prop(context.scene.world, '["heading"]')
        layout.operator(SKYLIGHT_OT_update_world.bl_idname)
