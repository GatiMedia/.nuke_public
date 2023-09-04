## Imports
import nuke
import nukescripts

### Collect animated nodes
def getAnimNodes():
    anim_nodes = []
    for node in nuke.allNodes():
        for knob in node.allKnobs():
            if knob.toScript().startswith("{curve "):
                anim_nodes.append(node.name())
    anim_nodes = list(dict.fromkeys(anim_nodes))
    anim_nodes.sort(key=str.lower)
    return anim_nodes

### Set up the popup window
class animNodesWindow(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Animated Nodes Finder')
        self.setMinimumSize(400, 150)

        self.nodeNamesKnob = nuke.Enumeration_Knob('anim_nodes', 'Nodes', getAnimNodes())
        self.addKnob(self.nodeNamesKnob)

        self.spaceKnob = nuke.Text_Knob('space2', '')
        self.addKnob(self.spaceKnob)

        self.infoKnob = nuke.Text_Knob('info', '')
        self.infoKnob.setValue('<p style="font-size:15px">&#128269; Select an Animated Node to Zoom on!</p>')
        self.addKnob(self.infoKnob)

        self.spaceKnob2 = nuke.Text_Knob('space3', '')
        self.addKnob(self.spaceKnob2)

### Open the popup window
def openAnimNodesWindow():
    if getAnimNodes():
        anim_nodes_window = animNodesWindow()
        if anim_nodes_window.showModalDialog():
            selected_node = anim_nodes_window.nodeNamesKnob.value()
            for node in nuke.allNodes():
                node.setSelected(False)
            nuke.toNode(selected_node).setSelected(True)
            nuke.zoomToFitSelected()
    else:
        nuke.message('''<center><p style="font-size:30px">&#128531; <p style="font-size:15px"> Didn't find any animated nodes!</p>''')
