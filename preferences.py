import bpy
import os
import rna_keymap_ui
import sys


class EverythingSearch_Addon_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__ or "everything_search"

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

    def dll_exists(self):
        return bool(self.everything_dll_path) and os.path.isfile(self.everything_dll_path)

    def draw(self, context):
        layout = self.layout
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
        box = layout.box()
        box.label(text="Settings:", icon='SETTINGS')
        col = box.column(align=True)
        col.prop(self, "everything_results_max")
        col.prop(self, "everything_panel_show_max")

        box = layout.box()
        box.label(text="Shortcut to Open Panel:", icon='KEY_HLT')

        kc = bpy.context.window_manager.keyconfigs.addon
        col = box.column()
        if kc:
            addon_main = sys.modules[__package__]
            for km, kmi in getattr(addon_main, "addon_keymaps", []):
                col.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.label(text="Keyconfig not found", icon='ERROR')
CLASSES = (EverythingSearch_Addon_Preferences,)
