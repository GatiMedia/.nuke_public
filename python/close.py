import nuke 

# From https://www.ftrack.com/en/2019/09/8-ways-to-increase-your-efficiency-with-foundrys-nuke.html

def close():
    for node in nuke.allNodes(recurseGroups=True):
        node.hideControlPanel()
