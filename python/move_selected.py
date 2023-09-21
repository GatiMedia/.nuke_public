import nuke

### Move 1

def move_up_one():
    for n in nuke.selectedNodes():
        n['ypos'].setValue(int(n['ypos'].value()) - int(nuke.toNode('preferences')['GridHeight'].value()))

def move_down_one():
    for n in nuke.selectedNodes():
        n['ypos'].setValue(int(n['ypos'].value()) + int(nuke.toNode('preferences')['GridHeight'].value()))

def move_left_one():
    for n in nuke.selectedNodes():
        n['xpos'].setValue(int(n['xpos'].value()) - int(nuke.toNode('preferences')['GridWidth'].value()))

def move_right_one():
    for n in nuke.selectedNodes():
        n['xpos'].setValue(int(n['xpos'].value()) + int(nuke.toNode('preferences')['GridWidth'].value()))

### Move 10

def move_up_ten():
    for n in nuke.selectedNodes():
        n['ypos'].setValue(int(n['ypos'].value()) - int(nuke.toNode('preferences')['GridHeight'].value()*10))

def move_down_ten():
    for n in nuke.selectedNodes():
        n['ypos'].setValue(int(n['ypos'].value()) + int(nuke.toNode('preferences')['GridHeight'].value()*10))

def move_left_ten():
    for n in nuke.selectedNodes():
        n['xpos'].setValue(int(n['xpos'].value()) - int(nuke.toNode('preferences')['GridWidth'].value()*10))

def move_right_ten():
    for n in nuke.selectedNodes():
        n['xpos'].setValue(int(n['xpos'].value()) + int(nuke.toNode('preferences')['GridWidth'].value()*10))
