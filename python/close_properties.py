# --------------------------------------------------------------
#  close.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 26/09/2023
# --------------------------------------------------------------

# From https://www.ftrack.com/en/2019/09/8-ways-to-increase-your-efficiency-with-foundrys-nuke.html

import nuke 

def close():
    for node in nuke.allNodes(recurseGroups=True):
        node.hideControlPanel()
