# --------------------------------------------------------------
#  change_label.py
#  Version: 1.0
#  Last Updated: 13/02/2024
#  Last updated by: Attila Gasparetz
# --------------------------------------------------------------
import nuke
import nukescripts

## defining the popup window
class ChangeLabelWindow(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'ChangeLabel')
        self.setMinimumSize(400, 150)

        self.labelKnob = nuke.EvalString_Knob('label_value', 'Label')
        self.addKnob(self.labelKnob)

        self.spaceKnob = nuke.Text_Knob('space2', '')
        self.addKnob(self.spaceKnob)

        self.infoKnob = nuke.Text_Knob('info', '')
        self.infoKnob.setValue('<font color=orange><b>Type in the new label<b>')
        self.addKnob(self.infoKnob)

        self.spaceKnob = nuke.Text_Knob('space3', '')
        self.addKnob(self.spaceKnob)

        self.labelMode = nuke.Enumeration_Knob('label_values', 'Labels', ["Add to label","Add to existing label"])
        self.addKnob(self.labelMode)

        self.spaceKnob = nuke.Text_Knob('space4', '')
        self.addKnob(self.spaceKnob)

## opening the popup window
def setLabel():
    if len(nuke.selectedNodes()) == 0:
        nuke.alert('<font color=orange><h3>Select at least a single node first!')
    else:
        bdS = ChangeLabelWindow()
        if bdS.showModalDialog():
            new_label = bdS.labelKnob.value()
            label_mode = bdS.labelMode.value()
            for node in nuke.selectedNodes():
                if label_mode == "Add to label":
                    node['label'].setValue(new_label)
                else:
                    if not node['label'].value() == "":
                        node['label'].setValue(str(node['label'].value()) + "\n" + str(new_label))
                    else:
                        node['label'].setValue(new_label)
