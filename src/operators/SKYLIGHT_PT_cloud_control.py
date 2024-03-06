import bpy

from ... import dependencies, utils

from .SKYLIGHT_OT_select_cloud_layer import SKYLIGHT_OT_select_cloud_layer
from .SKYLIGHT_OT_add_cloud_layer import SKYLIGHT_OT_add_cloud_layer


class SKYLIGHT_PT_cloud_control(bpy.types.Panel):
    """Allows the user to import and manage Skylight cloud layers."""
    bl_label = "Cloud Controller"
    bl_category = "Skylight"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    @classmethod
    def poll(self, context):
        return dependencies.satisfied() \
            and utils.CONST_WORLD_NAME in bpy.data.worlds


    def draw(self, context):
        layout = self.layout
        layout.operator(SKYLIGHT_OT_add_cloud_layer.bl_idname)
        layout.operator_menu_enum(SKYLIGHT_OT_select_cloud_layer.bl_idname, 'cloud_layers',
            text=bpy.data.worlds[utils.CONST_WORLD_NAME]["ui_selected_cloud_layer"] or "None Selected")
        selected = bpy.data.worlds[utils.CONST_WORLD_NAME]["ui_selected_cloud_layer"]
        if selected:
            cloud = bpy.data.objects[selected]
            layout.prop(cloud, '["altitude"]')
            layout.prop(cloud, '["clear_patch_size"]')
            layout.prop(cloud, '["cloud_size"]')
            layout.prop(cloud, '["coverage"]')
            layout.prop(cloud, '["density"]')
            layout.prop(cloud, '["distance_scaling"]')
            layout.prop(cloud, '["offset_x"]')
            layout.prop(cloud, '["offset_y"]')
            layout.prop(cloud, '["opacity"]')
            layout.prop(cloud, '["rotation"]')
            layout.prop(cloud, '["seed"]')
            layout.prop(cloud, '["world_radius"]')
