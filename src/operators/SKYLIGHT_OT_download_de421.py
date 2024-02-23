import bpy

from ... import dependencies, utils

class SKYLIGHT_OT_download_de421(bpy.types.Operator):
    """Attempts to download the DE421 SPICE kernel from NASA."""
    bl_idname = 'skylight.download_de421'
    bl_label = "Download DE421 SPICE Kernel"
    bl_description = ("Downloads the DE421 SPICE kernel to enable calculation of ephemeris.")
    bl_options = {'REGISTER', 'INTERNAL'}

    _timer = None
    _finished = False
    _progress = ""
    _cancelled = False

    @classmethod
    def poll(self, context):
        return not dependencies.dep_de421_spice

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def execute(self, context):
        self._timer = None
        self._finished = False
        self._progress = ""
        self._cancelled = False
        if not dependencies.dep_requests:
            utils.install_module(utils.CONST_REQUESTS_MODULE_NAME)

        def show_progress(progress):
            self._progress = progress

        def show_finished():
            self._finished = True

        def check_cancelled():
            return self._cancelled

        wm = context.window_manager
        context.preferences.addons[utils.CONST_ADDON_NAME].preferences.running_modal = True
        context.preferences.addons[utils.CONST_ADDON_NAME].preferences.download_progress = ""
        utils.background_invoke(lambda: utils.download_resource(utils.CONST_DE421_URL, utils.get_de421_path().resolve(), utils.CONST_MEGABYTE, show_progress, show_finished, check_cancelled))
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            context.preferences.addons[utils.CONST_ADDON_NAME].preferences.running_modal = False
            context.preferences.addons[utils.CONST_ADDON_NAME].preferences.download_progress = ""
            return {'CANCELLED'}

        if event.type == 'TIMER':
            context.preferences.addons[utils.CONST_ADDON_NAME].preferences.download_progress = self._progress
            if self._finished:
                context.preferences.addons[utils.CONST_ADDON_NAME].preferences.running_modal = False
                context.preferences.addons[utils.CONST_ADDON_NAME].preferences.download_progress = ""
                dependencies.dep_de421_spice = True
                utils.align_preferences()
                return {'FINISHED'}
        return {'PASS_THROUGH'}
