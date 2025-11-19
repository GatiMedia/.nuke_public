# --------------------------------------------------------------
#  reload_read.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 02/09/2025
# --------------------------------------------------------------

import nuke

def reload_all_read():
    nodes_classes = ["Read", "DeepRead", "Camera2", "Camera3", "ReadGeo", "ReadGeo2"]
    for node in nuke.allNodes(group=nuke.root()):
        if node.Class() in nodes_classes:
            try:
                node["reload"].execute()
            except Exception:
                pass

def reload_sel_read():
    nodes_classes = ["Read", "DeepRead", "Camera2", "Camera3", "ReadGeo", "ReadGeo2"]
    for node in nuke.selectedNodes():
        if node.Class() in nodes_classes:
            try:
                node["reload"].execute()
            except Exception:
                pass
