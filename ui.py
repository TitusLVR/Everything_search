import bpy
import os

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
        prefs = bpy.context.preferences.addons[__package__].preferences
        props = context.scene.EverythingSearch
        
        layout = self.layout
        layout.prop(props, "search_query", text="Search")
        layout.prop(props, "search_filter", text="File Type")
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

CLASSES = (EVERYTHING_PT_Panel,)
