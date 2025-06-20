import bpy
import os
import subprocess


class EVERYTHING_OT_Open_File(bpy.types.Operator):
    """Open a file in Blender

    Behaviour depends on file extension:
    - .blend: open as main file (replaces current session)
        ALT + Click: open in a new Blender instance (only for .blend files)
    - .fbx, .obj, .usd: import into current scene using the corresponding import operator
    - .py, .txt: load into the Blender Text Editor
    - .tga, .png, .jpg, .jpeg: load as images (Image Editor & datablock)
    CTRL + Click: open containing folder
    """
    bl_idname = "everything.open_file"
    bl_label = "Open File"

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        # Ensure the file exists first
        if not os.path.exists(self.filepath):
            self.report({'ERROR'}, "File not found.")
            return {'CANCELLED'}

        _, ext = os.path.splitext(self.filepath)
        ext = ext.lower()

        try:
            # 1️⃣  .blend – Replace current session
            if ext == ".blend":
                bpy.ops.wm.open_mainfile(filepath=self.filepath)

            # 2️⃣  3‑D geometry imports
            elif ext in {".fbx", ".obj", ".usd"}:
                if ext == ".fbx":
                    bpy.ops.import_scene.fbx(filepath=self.filepath)
                elif ext == ".obj":
                    bpy.ops.wm.obj_import(filepath=self.filepath)
                else:  # .usd
                    # USD importer is available in Blender 3.6+
                    bpy.ops.wm.usd_import(filepath=self.filepath)

            # 3️⃣  Scripts / plain‑text → Text Editor
            elif ext in {".py", ".txt"}:
                bpy.ops.text.open(filepath=self.filepath)

            # 4️⃣  Images
            elif ext in {".tga", ".png", ".jpg", ".jpeg"}:
                bpy.ops.image.open(filepath=self.filepath)

            # 5️⃣  Fallback – open folder
            else:
                folder = os.path.dirname(self.filepath)
                if os.path.exists(folder):
                    os.startfile(folder)
                self.report({'WARNING'}, f"Unhandled extension '{ext}', folder opened instead.")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to open file: {e}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # Open containing folder
        if event.ctrl:
            folder = os.path.dirname(self.filepath)
            if os.path.exists(folder):
                os.startfile(folder)
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Folder not found.")
                return {'CANCELLED'}

        # Open in a new Blender instance
        elif event.alt:
            blender_path = bpy.app.binary_path
            if os.path.exists(self.filepath):
                subprocess.Popen([blender_path, self.filepath])
                self.report({'INFO'}, "Opened in new Blender instance.")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "File not found.")
                return {'CANCELLED'}

        # Default behaviour
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


