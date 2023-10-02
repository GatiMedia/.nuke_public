# --------------------------------------------------------------
#  gm_autoplace.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 02/10/2023
# --------------------------------------------------------------

import nuke
import os

def gm_autoplace():
    READ_PREFIX = "000_"
    DIVIDER = "__#__#__"
    sel_nodes = nuke.selectedNodes()
    node_names = []
    for n in sel_nodes:
        try:
            if n.Class() == "Read":
                file_name = os.path.basename(n['file'].value())
                node_names.append(READ_PREFIX + file_name + DIVIDER + n.name())
            else:
                node_names.append(n.name())
        except:
            pass
    node_names.sort()
    new_names = []
    for n in node_names:
        try:
            n = n.split(DIVIDER, 1)[1]
            new_names.append(n)
        except:
            new_names.append(n)

    #first_xpos = min([node.knob("z_order").value() for node in selectedBackdropNodes])
    first_xpos = []
    first_ypos = nuke.toNode(new_names[0])['ypos'].value()
    for n in sel_nodes:
        first_xpos.append(n['xpos'].value())

    grid_width = nuke.toNode('preferences')['GridWidth'].value()
    for x, node in enumerate(new_names):
        nuke.toNode(node)['ypos'].setValue(float(first_ypos))
        nuke.toNode(node)['xpos'].setValue(float(min(first_xpos) + (x*(grid_width*3))))
