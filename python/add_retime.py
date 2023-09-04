import nuke

def addRetime():
    for node in nuke.selectedNodes():
        try:
            retime = nuke.createNode('Retime')
            retime['output.first_lock'].setValue(1)
            retime['output.first'].setValue(1001)
            retime['xpos'].setValue(node['xpos'].value())
            retime['ypos'].setValue(node['ypos'].value() + 100)
            retime.setInput(0, node)
        except Exception:
            pass