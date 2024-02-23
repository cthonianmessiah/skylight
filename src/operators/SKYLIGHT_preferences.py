import bpy

from ... import dependencies, utils

from .SKYLIGHT_OT_install_skyfield import SKYLIGHT_OT_install_skyfield
from .SKYLIGHT_OT_download_de421 import SKYLIGHT_OT_download_de421
from .SKYLIGHT_OT_download_sky import SKYLIGHT_OT_download_sky
from .SKYLIGHT_OT_download_moon import SKYLIGHT_OT_download_moon


class SKYLIGHT_preferences(bpy.types.AddonPreferences):
    """Addon preferences that provide a mechanism for downloading/installing external dependencies."""
    bl_idname = utils.CONST_ADDON_NAME

    download_progress: bpy.props.StringProperty(
        name="Downloading",
        description="The progress of the current download.",
        default="",
        update=lambda _, __: None
        )

    running_modal: bpy.props.BoolProperty(
        name="RunningModal",
        description="True if one of the preferences modal operations is running",
        default=False,
        update=lambda _, __: None
        )


    @classmethod
    def poll(self, context):
        return not dependencies.satisfied()


    def draw(self, context):
        layout = self.layout
        if self.running_modal:
            layout.label(text=f"Progress: {self.download_progress}")
        else:
            if not dependencies.dep_skyfield:
                layout.operator(SKYLIGHT_OT_install_skyfield.bl_idname, icon="SCRIPT")
            if not dependencies.dep_de421_spice:
                layout.operator(SKYLIGHT_OT_download_de421.bl_idname, icon="FILE_NEW")
            if not dependencies.dep_sky_texture:
                layout.operator(SKYLIGHT_OT_download_sky.bl_idname, icon="FILE_NEW")
            if not dependencies.dep_moon_texture:
                layout.operator(SKYLIGHT_OT_download_moon.bl_idname, icon="FILE_NEW")
