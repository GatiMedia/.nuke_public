# --------------------------------------------------------------
#  add_retime.py
#  Last Updated: 22/02/2024
#  Last updated by: Attila Gasparetz
# --------------------------------------------------------------

import nuke

def addRetime():
    multipleNodes = nuke.selectedNodes()
    if len(multipleNodes) == 0:
        nuke.message("""<center><font color=orange>Select a node/nodes first!""")
    else:
        for node in multipleNodes:
            try:
                retime = nuke.createNode('Retime')
                retime['output.first_lock'].setValue(1)
                retime['output.first'].setValue(nuke.Root().firstFrame())
                retime['xpos'].setValue(node['xpos'].value())
                retime['ypos'].setValue(node['ypos'].value() + 220)
                retime.setInput(0, node)
            except:
                pass
