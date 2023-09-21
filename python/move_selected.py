import nuke

### Move 1

def move_up_one():
    grid_height = nuke.toNode('preferences')['GridHeight'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['ypos'].setValue(int(n['ypos'].value()) - int(grid_height))

def move_down_one():
    grid_height = nuke.toNode('preferences')['GridHeight'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['ypos'].setValue(int(n['ypos'].value()) + int(grid_height))

def move_left_one():
    grid_width = nuke.toNode('preferences')['GridWidth'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['xpos'].setValue(int(n['xpos'].value()) - int(grid_width))

def move_right_one():
    grid_width = nuke.toNode('preferences')['GridWidth'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['xpos'].setValue(int(n['xpos'].value()) + int(grid_width))

### Move 10

def move_up_ten():
    grid_height = nuke.toNode('preferences')['GridHeight'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['ypos'].setValue(int(n['ypos'].value()) - int(grid_height*10))

def move_down_ten():
    grid_height = nuke.toNode('preferences')['GridHeight'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['ypos'].setValue(int(n['ypos'].value()) + int(grid_height*10))

def move_left_ten():
    grid_width = nuke.toNode('preferences')['GridWidth'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['xpos'].setValue(int(n['xpos'].value()) - int(grid_width*10))

def move_right_ten():
    grid_width = nuke.toNode('preferences')['GridWidth'].value()
    sel = nuke.selectedNodes()
    for n in sel:
        n['xpos'].setValue(int(n['xpos'].value()) + int(grid_width*10))
