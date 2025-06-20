import bpy
import os
from .preferences import get_dynamic_filetype_items

def update_search(self, context):
    prefs = bpy.context.preferences.addons[__package__ or "Everything_search"].preferences
    props = context.scene.EverythingSearch
    query = props.search_query
    # Use the dynamic selection for filetype!
    filetype = props.filetype_enum if props.filetype_enum else "blend"
    props.results.clear()
    props.scroll_offset = 0

    if not query.strip():
        return
    if not prefs.everything_dll_path or not os.path.isfile(prefs.everything_dll_path):
        print("[Everything Sidebar] DLL path not set or DLL missing.")
        return
    try:
        from .ipc import EverythingIPC
        search_str = f"{query} *.{filetype}" if filetype != "all" else query
        results = EverythingIPC(prefs.everything_dll_path).query(
            search_str, prefs.everything_results_max
        )
        for path in results:
            item = props.results.add()
            item.name = path
        visible_count = prefs.everything_panel_show_max
        max_offset = max(0, len(props.results) - visible_count)
        props.scroll_offset = min(props.scroll_offset, max_offset)
    except Exception as e:
        print(f"[Everything Sidebar Search Error] {e}")

class EverythingSearch_Item(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

class EverythingSearch(bpy.types.PropertyGroup):
    search_query: bpy.props.StringProperty(
        name="Search",
        default="",
        update=update_search,
        options={'TEXTEDIT_UPDATE'},
        description="Search query for Everything",
    )
    filetype_enum: bpy.props.StringProperty(
        name="File Type",
        default="blend",
        description="Filter results by file type"
    )
    scroll_offset: bpy.props.IntProperty(default=0)
    results: bpy.props.CollectionProperty(type=EverythingSearch_Item)
