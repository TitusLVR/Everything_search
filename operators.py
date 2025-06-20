import bpy
import os
import subprocess
from .preferences import image_exts, model_exts, text_exts, video_exts, audio_exts

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
            #.blend – Replace current session
            if ext == ".blend":
                bpy.ops.wm.open_mainfile(filepath=self.filepath)

            #3‑D geometry imports .obj", ".fbx", ".usd", ".stl", ".dae", ".abc", ".ply", ".glb", ".gltf", ".3ds", ".x3d", ".wrl", ".svg", ".obj.gz"
            elif ext in model_exts:
                if ext == ".fbx":
                    bpy.ops.import_scene.fbx(filepath=self.filepath)
                elif ext == ".obj":
                    bpy.ops.wm.obj_import(filepath=self.filepath)
                elif ext == ".usd":
                    bpy.ops.wm.usd_import(filepath=self.filepath)
                elif ext == ".stl":  # STL files
                    bpy.ops.import_mesh.stl(filepath=self.filepath)
                elif ext == ".dae":  # DAE files
                    bpy.ops.wm.collada_import(filepath=self.filepath)
                elif ext == ".abc":  # Alembic files
                    bpy.ops.wm.alembic_import(filepath=self.filepath)
                elif ext == ".glb" or ext == ".gltf":  # GLTF/GLB files
                    bpy.ops.wm.gltf_import(filepath=self.filepath)
                elif ext == ".ply":  # PLY files
                    bpy.ops.import_mesh.ply(filepath=self.filepath)
                elif ext == ".glb":
                    bpy.ops.wm.gltf_import(filepath=self.filepath)                
                elif ext == ".3ds":  # 3DS files
                    bpy.ops.import_scene.autodesk_3ds(filepath=self.filepath)
                elif ext == ".x3d" or ext == ".wrl":  # X3D/VRML files
                    bpy.ops.import_scene.x3d(filepath=self.filepath)
                elif ext == ".wrl":  # VRML files
                    bpy.ops.import_scene.x3d(filepath=self.filepath)
                elif ext == ".svg":  # SVG files
                    bpy.ops.import_curve.svg(filepath=self.filepath)
                elif ext == ".obj.gz":  # Gzipped OBJ files
                    bpy.ops.wm.obj_import(filepath=self.filepath, use_gzip=True)

            #Scripts / plain‑text → Text Editor
            elif ext in text_exts:
                bpy.ops.text.open(filepath=self.filepath)
            # Video files
            elif ext in video_exts:
                bpy.ops.clip.open(filepath=self.filepath)
            # Audio files
            elif ext in audio_exts:
                bpy.ops.sound.open(filepath=self.filepath)
            # Images
            elif ext in image_exts:
                bpy.ops.image.open(filepath=self.filepath)
            # Fallback – open folder
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


