# --------------------------------------------------------------
#  clean_droppedknobs.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 26/09/2023
# --------------------------------------------------------------

# based on code on this thread https://community.foundry.com/discuss/topic/152473/paneldropped

import nuke

def cleanDroppedKnobs():
    for node in nuke.allNodes(recurseGroups=True):
        for knob in node.knobs():
            if 'panelDropped' in knob:
                try:
                    node.removeKnob(node[knob])
                except:
                    pass
