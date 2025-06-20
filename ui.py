import bpy
import os
from .preferences import get_dynamic_filetype_items
from .properties import update_search

# --- PANEL ---
class EVERYTHING_PT_Panel(bpy.types.Panel):
    bl_label = "Everything Search"
    bl_idname = "EVERYTHING_PT_sidebar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category =  "Everything"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        prefs = bpy.context.preferences.addons[__package__ or "Everything_search"].preferences
        props = context.scene.EverythingSearch
        layout = self.layout

        # Search box
        layout.prop(props, "search_query", text="Search")

        # --- Dynamic Filetype Dropdown ---
        enum_items = get_dynamic_filetype_items()
        selected = props.filetype_enum if props.filetype_enum else "blend"
        label_dict = {value: label for value, label, _desc in enum_items}
        row = layout.row()
        row.label(text="File Type")
        row.menu("EVERYTHING_MT_filetype_enum", text=label_dict.get(selected, selected))
        # --- End Dropdown ---

        # Results info
        total = len(props.results)
        visible_count = prefs.everything_panel_show_max
        offset = props.scroll_offset
        if total:
            showing_min = offset + 1
            showing_max = min(offset + visible_count, total)
            layout.label(
                text=f"Results: {total}  (showing {showing_min} - {showing_max})",
                icon='VIEWZOOM'
            )
        else:
            layout.label(text="Results: 0", icon='VIEWZOOM')
        col = layout.column()
        if total > visible_count:
            row = layout.row(align=True)
            row.operator("everything.scroll_results", text="<-").direction = 'LEFT'
            row.operator("everything.scroll_results", text="->").direction = 'RIGHT'
        if total:
            for item in props.results[offset:offset+visible_count]:
                col.operator("everything.open_file", text=os.path.basename(item.name), icon='FILEBROWSER').filepath = item.name
        else:
            col.label(text="No results", icon='INFO')


# --- DYNAMIC DROPDOWN MENU ---
class EVERYTHING_MT_filetype_enum(bpy.types.Menu):
    bl_label = "Select File Type"

    def draw(self, context):
        props = context.scene.EverythingSearch
        enum_items = get_dynamic_filetype_items()
        for value, label, _desc in enum_items:
            self.layout.operator(
                "everything.set_filetype_enum",
                text=label,
                depress=(props.filetype_enum == value)
            ).value = value

# --- OPERATOR TO SET FILETYPE ---
class EVERYTHING_OT_SetFiletypeEnum(bpy.types.Operator):
    bl_idname = "everything.set_filetype_enum"
    bl_label = "Set File Type"
    value: bpy.props.StringProperty()

    def execute(self, context):
        props = context.scene.EverythingSearch
        props.filetype_enum = self.value
        # Optionally update search automatically:
        update_search(props, context)
        return {'FINISHED'}



