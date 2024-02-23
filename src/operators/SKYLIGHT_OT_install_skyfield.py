import bpy

from ... import dependencies, utils

class SKYLIGHT_OT_install_skyfield(bpy.types.Operator):
    """Attempts to install the skyfield Python module when executed.
       This may require elevated permissions on Windows."""
    bl_idname = 'skylight.install_skyfield'
    bl_label = "Install Skyfield Module"
    bl_description = ("Downloads and installs the Skyfield Python module for calculating ephemerides. "
                      "Requires an internet connection and may require elevated privileges.")
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(self, context):
        return not dependencies.dep_skyfield

    def execute(self, context):
        utils.install_module(utils.CONST_SKYFIELD_MODULE_NAME)
        dependencies.dep_skyfield = True
        utils.align_preferences()
        return {'FINISHED'}
