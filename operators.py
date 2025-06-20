import bpy
import os
import subprocess

import bpy
import os
import subprocess

class EVERYTHING_OT_Open_File(bpy.types.Operator):
    """Open a file in Blender
    CTRL + Click: Open the containing folder
    ALT + Click: Open in a new Blender instance
    """
    bl_idname = "everything.open_file"
    bl_label = "Open File"

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        if os.path.exists(self.filepath):
            bpy.ops.wm.open_mainfile(filepath=self.filepath)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "File not found.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        if event.ctrl:
            # Open the containing folder
            folder = os.path.dirname(self.filepath)
            if os.path.exists(folder):
                os.startfile(folder)  # Windows-only; use `subprocess.call(["xdg-open", folder])` for Linux
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Folder not found.")
                return {'CANCELLED'}

        elif event.alt:
            # Open in a new Blender instance
            blender_path = bpy.app.binary_path
            if os.path.exists(self.filepath):
                subprocess.Popen([blender_path, self.filepath])
                self.report({'INFO'}, "Opened in new Blender instance.")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "File not found.")
                return {'CANCELLED'}

        else:
            return self.execute(context)


class EVERYTHING_OT_Scroll_Results(bpy.types.Operator):
    bl_idname = "everything.scroll_results"
    bl_label = "Scroll Results"
    bl_options = {'INTERNAL'}
    direction: bpy.props.EnumProperty(
        items=[
            ('LEFT', "Left", ""),
            ('RIGHT', "Right", ""),
        ]
    )
    def execute(self, context):
        props = context.scene.EverythingSearch
        prefs = bpy.context.preferences.addons[__package__].preferences
        visible_count = prefs.everything_panel_show_max
        max_results = len(props.results)
        max_offset = max(0, max_results - visible_count)
        if self.direction == 'LEFT':
            props.scroll_offset = max(0, props.scroll_offset - visible_count)
        else:
            props.scroll_offset = min(max_offset, props.scroll_offset + visible_count)
        props.scroll_offset = min(props.scroll_offset, max_offset)
        return {'FINISHED'}


class EVERYTHING_OT_Open_Dll_Subfolder(bpy.types.Operator):
    bl_idname = "everything.open_dll_subfolder"
    bl_label = "Open DLL Folder"
    bl_description = "Open the 'dll' folder inside the add-on directory (where Everything64.dll should be)"

    def execute(self, context):
        addon_folder = os.path.dirname(__file__)
        dll_folder = os.path.join(addon_folder, "dll")
        if not os.path.isdir(dll_folder):
            self.report({'ERROR'}, f"'dll' folder does not exist at: {dll_folder}")
            return {'CANCELLED'}
        try:
            subprocess.Popen(f'explorer "{dll_folder}"')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Could not open folder: {e}")
            return {'CANCELLED'}


class EVERYTHING_OT_Open_Panel(bpy.types.Operator):
    """Open the Everything Sidebar Panel (shows in 3D View UI region)"""
    bl_idname = "everything.open_panel"
    bl_label = "Open Everything Sidebar Panel"

    def execute(self, context):
        # The name below must match your panel's bl_idname!
        bpy.ops.wm.call_panel(name="EVERYTHING_PT_sidebar")
        return {'FINISHED'}


