import bpy
import os

from ... import dependencies, utils

available_cloud_types = [
    ('0', "Altocumulus", "Altocumulus"),
    ('1', "Altostratus", "Altostratus"),
    ('2', "Cirrocumulus", "Cirrocumulus"),
    ('3', "Cirrostratus", "Cirrostratus"),
    ('4', "Cirrus", "Cirrus"),
    ('5', "Cumulonimbus", "Cumulonimbus"),
    ('6', "Cumulus", "Cumulus"),
    ('7', "Nimbostratus", "Nimbostratus"),
    ('8', "Stratocumulus", "Stratocumulus"),
    ('9', "Stratus", "Stratus"),
    ]


class SKYLIGHT_OT_add_cloud_layer(bpy.types.Operator):
    """Adds a new cloud layer to the current scene."""
    bl_idname = 'skylight.add_cloud_layer'
    bl_label = "Add Cloud Layer"
    bl_description = "Click to add a new Skylight-managed cloud layer to the current scene"
    bl_options = {'REGISTER'}

    cloud_types: bpy.props.EnumProperty(items=available_cloud_types, name="Cloud Types")


    @classmethod
    def poll(self, context):
        return bpy.data.filepath != str(utils.get_blend_path().resolve())


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):
        if not utils.CONST_CLOUD_COLLECTION_NAME in bpy.data.collections:
            clouds = bpy.data.collections.new(utils.CONST_CLOUD_COLLECTION_NAME)
            bpy.context.scene.collection.children.link(clouds)
        view_layer = context.view_layer
        view_layer.active_layer_collection = \
            utils.find_collection(view_layer.layer_collection, utils.CONST_CLOUD_COLLECTION_NAME)
        file_path = utils.get_blend_path()
        inner_path = "Object"
        object_name = self.get_selected_type(context)
        utils.logger.warning(file_path)
        utils.logger.warning(inner_path)
        utils.logger.warning(object_name)
        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
            )
        return {'FINISHED'}


    def get_selected_type(self, context):
        return available_cloud_types[int(self.cloud_types)][1]


    def draw(self, context):
        layout = self.layout
        layout.prop_menu_enum(self, 'cloud_types', text=self.get_selected_type(context))
