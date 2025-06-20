bl_info = {
    "name": "Everything Search",
    "author": "Titus",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "SideBar -> Everything",
    "description": "Everything live search in the sidebar with file opening support",
    "doc_url": "https://github.com/TitusLVR/Everything_search",
    "category": "Import-Export",
}

import bpy  # noqa: E402

# Explicit class imports
from .preferences import EverythingSearch_Addon_Preferences   # noqa: E402
from .properties import EverythingSearch_Item, EverythingSearch # noqa: E402
from .operators import EVERYTHING_OT_Open_File, EVERYTHING_OT_Scroll_Results, EVERYTHING_OT_Open_Dll_Subfolder, EVERYTHING_OT_Open_Panel # noqa: E402
from .ui import EVERYTHING_PT_Panel # noqa: E402

classes = [
    EverythingSearch_Addon_Preferences,
    EverythingSearch_Item,
    EverythingSearch,
    EVERYTHING_OT_Open_File,
    EVERYTHING_OT_Scroll_Results,
    EVERYTHING_OT_Open_Dll_Subfolder,
    EVERYTHING_OT_Open_Panel,
    EVERYTHING_PT_Panel,
]

addon_keymaps = []

def register():
    # ...register your classes etc...
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.EverythingSearch = bpy.props.PointerProperty(type=EverythingSearch)
    # Register keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type='EMPTY')
        kmi = km.keymap_items.new("everything.open_panel", type='F9', value='PRESS')
        addon_keymaps.append((km, kmi))

def unregister():
    # Unregister keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    # Unregister classes and properties
    del bpy.types.Scene.EverythingSearch
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
