import bpy
import os
import rna_keymap_ui
import sys

# File extension categories
image_exts = [".tga", ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".exr", ".hdr", ".psd", ".jp2"]
model_exts = [".obj", ".fbx", ".usd", ".stl", ".dae", ".abc", ".ply", ".glb", ".gltf", ".3ds", ".x3d", ".wrl", ".svg", ".obj.gz"]
text_exts  = [".py", ".txt", ".json", ".xml", ".cfg", ".ini", ".log", ".md", ".csv"]
video_exts = [".mp4", ".avi", ".mov", ".mkv", ".webm", ".mpeg", ".mpg", ".ogv", ".ogg", ".m4v"]
audio_exts = [".mp3", ".wav", ".ogg", ".flac", ".aac", ".aiff"]



# Utility for UI
def get_dynamic_filetype_items():
    # Called from UI only (never at registration)
    addon = bpy.context.preferences.addons.get(__package__ or "Everything_search")
    if not addon:
        return [("blend", "BLEND", "Blend files"), ("all", "All", "All file types")]
    prefs = addon.preferences
    items = [("blend", "BLEND", "Blend files")]
    for prop in dir(prefs):
        if prop.startswith("use_format_") and getattr(prefs, prop):
            ext = prop.replace("use_format_", "").replace("_", ".")
            label = ext.upper()
            if ext != "blend":
                items.append((ext, label, f"{label} files"))
    items.append(("all", "All", "All file types"))
    return items

class EverythingSearch_Addon_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__ or "Everything_search"

    everything_dll_path: bpy.props.StringProperty(
        name="Everything DLL Path",
        subtype='FILE_PATH',
        default="",
        description="Path to Everything64.dll (usually in the Everything installation folder, e.g., C:\\Program Files\\Everything\\Everything64.dll). If not set, the add-on will not work.",
    )
    everything_results_max: bpy.props.IntProperty(
        name="Max Results",
        min=1, max=10000,
        default=512,
        description="Maximum number of Everything results to fetch. Lower values may improve performance but limit results (try 25~100 and increase if needed)"
    )
    everything_panel_show_max: bpy.props.IntProperty(
        name="Results Shown in Panel",
        min=1, max=100,
        default=25,
        description="Number of results visible in panel at once"
    )

    # The toggles!
    show_supported_formats: bpy.props.BoolProperty(name="", default=False)
    use_format_tga: bpy.props.BoolProperty(name="TGA", default=True)
    use_format_png: bpy.props.BoolProperty(name="PNG", default=True)
    use_format_jpg: bpy.props.BoolProperty(name="JPG", default=True)
    use_format_jpeg: bpy.props.BoolProperty(name="JPEG", default=False)
    use_format_bmp: bpy.props.BoolProperty(name="BMP", default=False)
    use_format_gif: bpy.props.BoolProperty(name="GIF", default=False)
    use_format_tif: bpy.props.BoolProperty(name="TIF", default=False)
    use_format_tiff: bpy.props.BoolProperty(name="TIFF", default=False)
    use_format_exr: bpy.props.BoolProperty(name="EXR", default=False)
    use_format_hdr: bpy.props.BoolProperty(name="HDR", default=True)
    use_format_psd: bpy.props.BoolProperty(name="PSD", default=False)
    use_format_jp2: bpy.props.BoolProperty(name="JP2", default=False)
    use_format_obj: bpy.props.BoolProperty(name="OBJ", default=True)
    use_format_fbx: bpy.props.BoolProperty(name="FBX", default=True)
    use_format_usd: bpy.props.BoolProperty(name="USD", default=True)
    use_format_stl: bpy.props.BoolProperty(name="STL", default=False)
    use_format_dae: bpy.props.BoolProperty(name="DAE", default=False)
    use_format_abc: bpy.props.BoolProperty(name="ABC", default=False)
    use_format_ply: bpy.props.BoolProperty(name="PLY", default=False)
    use_format_glb: bpy.props.BoolProperty(name="GLB", default=False)
    use_format_gltf: bpy.props.BoolProperty(name="GLTF", default=False)
    use_format_3ds: bpy.props.BoolProperty(name="3DS", default=False)
    use_format_x3d: bpy.props.BoolProperty(name="X3D", default=False)
    use_format_wrl: bpy.props.BoolProperty(name="WRL", default=False)
    use_format_svg: bpy.props.BoolProperty(name="SVG", default=False)
    use_format_obj_gz: bpy.props.BoolProperty(name="OBJ.GZ", default=False)
    use_format_py: bpy.props.BoolProperty(name="PY", default=True)
    use_format_txt: bpy.props.BoolProperty(name="TXT", default=True)
    use_format_json: bpy.props.BoolProperty(name="JSON", default=False)
    use_format_xml: bpy.props.BoolProperty(name="XML", default=False)
    use_format_cfg: bpy.props.BoolProperty(name="CFG", default=False)
    use_format_ini: bpy.props.BoolProperty(name="INI", default=True)
    use_format_log: bpy.props.BoolProperty(name="LOG", default=False)
    use_format_md: bpy.props.BoolProperty(name="MD", default=False)
    use_format_csv: bpy.props.BoolProperty(name="CSV", default=False)
    use_format_mp4: bpy.props.BoolProperty(name="MP4", default=False)
    use_format_avi: bpy.props.BoolProperty(name="AVI", default=True)
    use_format_mov: bpy.props.BoolProperty(name="MOV", default=False)
    use_format_mkv: bpy.props.BoolProperty(name="MKV", default=False)
    use_format_webm: bpy.props.BoolProperty(name="WEBM", default=False)
    use_format_mpeg: bpy.props.BoolProperty(name="MPEG", default=False)
    use_format_mpg: bpy.props.BoolProperty(name="MPG", default=False)
    use_format_ogv: bpy.props.BoolProperty(name="OGV", default=False)
    use_format_ogg_video: bpy.props.BoolProperty(name="OGG", default=False)
    use_format_m4v: bpy.props.BoolProperty(name="M4V", default=False)
    use_format_mp3: bpy.props.BoolProperty(name="MP3", default=True)
    use_format_wav: bpy.props.BoolProperty(name="WAV", default=False)
    use_format_ogg_audio: bpy.props.BoolProperty(name="OGG", default=False)
    use_format_flac: bpy.props.BoolProperty(name="FLAC", default=False)
    use_format_aac: bpy.props.BoolProperty(name="AAC", default=False)
    use_format_aiff: bpy.props.BoolProperty(name="AIFF", default=False)

    def dll_exists(self):
        return bool(self.everything_dll_path) and os.path.isfile(self.everything_dll_path)

    def draw(self, context):
        layout = self.layout

        # --- DLL Path Section ---
        box = layout.box()
        box.label(text="Library setup:", icon='PREFERENCES')
        col = box.column(align=True)
        exists = self.dll_exists()
        icon = 'CHECKMARK' if exists else 'CANCEL'
        label = "Everything64.dll - FOUND" if exists else "Everything64.dll - NOT FOUND, Copy it manually to Everything Installation Folder"
        row = col.row(align=True)
        row.label(text=label, icon=icon)
        if not exists:
            row.operator("everything.open_dll_subfolder", icon='FILE_FOLDER', text="Open DLL folder - Manual Copy")
        col.separator()
        col.prop(self, "everything_dll_path")

        # --- Core Settings ---
        box = layout.box()
        box.label(text="Settings:", icon='SETTINGS')
        col = box.column(align=True)
        col.prop(self, "everything_results_max")
        col.prop(self, "everything_panel_show_max")

        # --- Supported File Formats (collapsible) ---
        box_file_formats = layout.box()
        row = box_file_formats.row()
        row.prop(self, "show_supported_formats", icon="TRIA_DOWN" if self.show_supported_formats else "TRIA_RIGHT", emboss=False)
        row.label(text="Supported File Formats:", icon='FILE_TICK')

        if self.show_supported_formats:
            # --- Image Formats ---
            box = box_file_formats.box()
            box.label(text="Image Formats:", icon='IMAGE_DATA')
            row = box.row(align=True)
            row.prop(self, "use_format_tga", toggle=True)
            row.prop(self, "use_format_png", toggle=True)
            row.prop(self, "use_format_jpg", toggle=True)
            row.prop(self, "use_format_jpeg", toggle=True)
            row.prop(self, "use_format_bmp", toggle=True)
            row.prop(self, "use_format_gif", toggle=True)
            row.prop(self, "use_format_tif", toggle=True)
            row.prop(self, "use_format_tiff", toggle=True)
            row.prop(self, "use_format_exr", toggle=True)
            row.prop(self, "use_format_hdr", toggle=True)
            row.prop(self, "use_format_psd", toggle=True)
            row.prop(self, "use_format_jp2", toggle=True)
            
            # --- Model Formats ---
            box = box_file_formats.box()
            box.label(text="Model Formats:", icon='MESH_DATA')
            row = box.row(align=True)
            row.prop(self, "use_format_obj", toggle=True)
            row.prop(self, "use_format_fbx", toggle=True)
            row.prop(self, "use_format_usd", toggle=True)
            row.prop(self, "use_format_stl", toggle=True)
            row.prop(self, "use_format_dae", toggle=True)
            row.prop(self, "use_format_abc", toggle=True)
            row.prop(self, "use_format_ply", toggle=True)
            row.prop(self, "use_format_glb", toggle=True)
            row.prop(self, "use_format_gltf", toggle=True)
            row.prop(self, "use_format_3ds", toggle=True)
            row.prop(self, "use_format_x3d", toggle=True)
            row.prop(self, "use_format_wrl", toggle=True)
            row.prop(self, "use_format_svg", toggle=True)
            row.prop(self, "use_format_obj_gz", toggle=True)
            
            # --- Text Formats ---
            box = box_file_formats.box()
            box.label(text="Text Formats:", icon='TEXT')
            row = box.row(align=True)
            row.prop(self, "use_format_py", toggle=True)
            row.prop(self, "use_format_txt", toggle=True)
            row.prop(self, "use_format_json", toggle=True)
            row.prop(self, "use_format_xml", toggle=True)
            row.prop(self, "use_format_cfg", toggle=True)
            row.prop(self, "use_format_ini", toggle=True)
            row.prop(self, "use_format_log", toggle=True)
            row.prop(self, "use_format_md", toggle=True)
            row.prop(self, "use_format_csv", toggle=True)
            
            # --- Video Formats ---
            box = box_file_formats.box()
            box.label(text="Video Formats:", icon='SEQUENCE')
            row = box.row(align=True)
            row.prop(self, "use_format_mp4", toggle=True)
            row.prop(self, "use_format_avi", toggle=True)
            row.prop(self, "use_format_mov", toggle=True)
            row.prop(self, "use_format_mkv", toggle=True)
            row.prop(self, "use_format_webm", toggle=True)
            row.prop(self, "use_format_mpeg", toggle=True)
            row.prop(self, "use_format_mpg", toggle=True)
            row.prop(self, "use_format_ogv", toggle=True)
            row.prop(self, "use_format_ogg_video", toggle=True)
            row.prop(self, "use_format_m4v", toggle=True)
            
            # --- Audio Formats ---
            box = box_file_formats.box()
            box.label(text="Audio Formats:", icon='SOUND')
            row = box.row(align=True)
            row.prop(self, "use_format_mp3", toggle=True)
            row.prop(self, "use_format_wav", toggle=True)
            row.prop(self, "use_format_ogg_audio", toggle=True)
            row.prop(self, "use_format_flac", toggle=True)
            row.prop(self, "use_format_aac", toggle=True)
            row.prop(self, "use_format_aiff", toggle=True)

        # --- Keymap Shortcut ---
        box = layout.box()
        box.label(text="Shortcut to Open Panel:", icon='KEY_HLT')
        kc = bpy.context.window_manager.keyconfigs.addon
        col = box.column()
        if kc:
            import sys
            import rna_keymap_ui
            addon_main = sys.modules[__package__]
            for km, kmi in getattr(addon_main, "addon_keymaps", []):
                col.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.label(text="Keyconfig not found", icon='ERROR')
