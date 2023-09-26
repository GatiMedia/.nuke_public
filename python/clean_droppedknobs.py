# --------------------------------------------------------------
#  move_selected.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 26/09/2023
# --------------------------------------------------------------

import nuke

def cleanDroppedKnobs():
    for node in nuke.allNodes(recurseGroups=True):
        for knob in node.knobs():
            if 'panelDropped' in knob:
                try:
                    node.removeKnob(node[knob])
                except:
                    pass
