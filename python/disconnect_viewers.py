import nuke

# From http://www.lookinvfx.com/nuke-python-snippets/

def disconnectViewers():
    nuke.selectAll()
    nuke.invertSelection()

    for n in nuke.allNodes():
        if n.Class() == "Viewer":
            n['selected'].setValue(True)

    nuke.extractSelected()

nuke.addOnScriptLoad(disconnectViewers)
