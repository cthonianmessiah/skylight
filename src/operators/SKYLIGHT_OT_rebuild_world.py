import bpy
import os

from ... import dependencies, utils

class SKYLIGHT_OT_rebuild_world(bpy.types.Operator):
    """Displays a confirmation dialog for importing or reimporting the Skylight world shader
       into the current scene."""
    bl_idname = 'skylight.rebuild_world'
    bl_label = "Rebuild World Shader"
    bl_description = ("Imports or reimports the Skylight world shader into the current scene")
    bl_options = {'REGISTER', 'INTERNAL'}

    append_as: bpy.props.StringProperty(
        name="Append As",
        description="The name to give to the Skylight world shader.",
        default=utils.CONST_WORLD_NAME,
        update=lambda _, __: None
        )


    @classmethod
    def poll(self, context):
        return dependencies.satisfied() and bpy.data.filepath != str(utils.get_blend_path().resolve())


    def execute(self, context):
        temp_rename = False
        newname = "temp"
        worlds = bpy.data.worlds
        if worlds.get(self.append_as):
            worlds.remove(worlds[self.append_as], do_unlink=True)
        if worlds.get(utils.CONST_WORLD_NAME):
            temp_rename = True
            gen = 0
            while worlds.get(newname):
                gen += 1
                newname = f"temp{gen}"
            worlds[utils.CONST_WORLD_NAME].name = newname

        file_path = utils.get_blend_path()
        inner_path = 'World'
        object_name = utils.CONST_WORLD_NAME
        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
            )
        if self.append_as != utils.CONST_WORLD_NAME:
            worlds[utils.CONST_WORLD_NAME].name = self.append_as
        if temp_rename:
            worlds[newname].name = utils.CONST_WORLD_NAME
        context.scene.world = worlds[self.append_as]

        return {'FINISHED'}


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.label(text="Will Overwrite Conflicts!", icon="ERROR")
        layout.prop(self, 'append_as')
