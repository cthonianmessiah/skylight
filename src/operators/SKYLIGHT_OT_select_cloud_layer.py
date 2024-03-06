import bpy

from ... import dependencies, utils

class SKYLIGHT_OT_select_cloud_layer(bpy.types.Operator):
    """Changes the selected cloud layer in the cloud controller panel."""
    bl_idname = 'skylight.select_cloud_layer'
    bl_label = "Select Cloud Layer"
    bl_description = "Select the cloud layer to edit"
    bl_options = {'REGISTER', 'INTERNAL'}


    def enumerate_layers(self, context):
        return [] if not utils.CONST_CLOUD_COLLECTION_NAME in bpy.data.collections \
            else [(str(i), x.name, x.name) for i,x in \
                enumerate(bpy.data.collections[utils.CONST_CLOUD_COLLECTION_NAME].objects.values())]
    cloud_layers: bpy.props.EnumProperty(items = enumerate_layers, name = "Cloud Layers")


    @classmethod
    def poll(self, context):
        return utils.CONST_WORLD_NAME in bpy.data.worlds \
            and utils.CONST_CLOUD_COLLECTION_NAME in bpy.data.collections \
            and bpy.data.collections[utils.CONST_CLOUD_COLLECTION_NAME].objects.values()


    def get_selected_layer(self, context):
        return self.enumerate_layers(context)[int(self.cloud_layers)][1]


    def execute(self, context):
        # Expose the selected value as a custom property on the Earth world object
        bpy.data.worlds[utils.CONST_WORLD_NAME]["ui_selected_cloud_layer"] \
            = self.get_selected_layer(context)
        return {'FINISHED'}
