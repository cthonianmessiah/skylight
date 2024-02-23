import bpy

from ... import dependencies, utils

class SKYLIGHT_PT_missing_dependency_warning(bpy.types.Panel):
    """Shows a warning message when the addon's external dependencies are not satisfied."""
    bl_label = "Skylight Disabled"
    bl_category = "Skylight"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        return not dependencies.satisfied()

    def draw(self, context):
        layout = self.layout

        lines = [f"The \"{utils.CONST_ADDON_NAME}\" addon has detected one or more missing dependenices.",
                 f"Please check the addon's Preferences (Edit > Preferences > Addons).",
                 f"This addon's settings will be found under \"{utils.CONST_ADDON_NAME}\" in the details section.",
                 f"You will see buttons for downloading the missing dependencies.",
                 f"If the dependency install fails and you don't want to run with elevated permissions,"
                 f"you can use the alternative instruction in the \"DOWNLOADING.txt\" file in this addon's root folder."]

        for line in lines:
            layout.label(text=line);
