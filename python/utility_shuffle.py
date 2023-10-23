# --------------------------------------------------------------
#  utility_shuffle.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 23/10/2023
# --------------------------------------------------------------
# This tool is based on an AOV naming customization where Color ( Lighting ), Material and Texture groups gets prefixes, respectively "C_", "M_" and "T_"
# This tool assumes Stamps is installed

import nuke
import stamps
import os

def utilityShuffle():
    nodes = nuke.selectedNodes()
    X_DIST = 220
    Y_DIST = 250
    SELECT_VAL = True
    NOT_SELECT_VAL = False

    if not len(nodes) == 1:
        nuke.alert('<font color=orange><h3>Please, select a single node with Utilities first!')
    else:
        curSel = nuke.selectedNode()
        curSelChannels = curSel.channels()
        layersList = []
        for rawChannels in curSelChannels:
            splitRawChannels = rawChannels.split('.')
            layersList.append(splitRawChannels[0])
        channelLayers = list(set(layersList))

        utilities_of_interest = []
        for l in channelLayers:
            if "ID" in l or l == "N" or l == "P" or l == "Pref" or l == "Z":
                utilities_of_interest.append(l)

        utilities_of_interest.sort()

        curSel_name = curSel.name()
        topnode = nuke.tcl("value [topnode "+curSel_name+"].name")
        curSel_file = nuke.toNode(topnode)['file'].value()
        filename, file_extension =os.path.splitext(os.path.basename(curSel_file))
        file_val = filename.split(".")[0]

        if len(channelLayers) == 1:
            nuke.alert(
                '<font color=orange><h3><center>Not enough layers to break it down!\n\nOnly found:\n\n<font color=yellow><h4>' + ',\n'.join(
                    channelLayers))
        else:
            # create dotMain
            dot = connectDot = nuke.nodes.Dot()
            dot['xpos'].setValue(int(curSel['xpos'].value()) + (curSel.screenWidth() / 2) - (dot.screenWidth() / 2))
            dot['ypos'].setValue(int(curSel['ypos'].value()) + 300)
            dot.setSelected(SELECT_VAL)
            dot.setInput(0, curSel)

            # create dot_stamp_bty
            dot_stamp_bty = nuke.nodes.Dot()
            dot_stamp_bty['xpos'].setValue(int(dot['xpos'].value()))
            dot_stamp_bty['ypos'].setValue(int(dot['ypos'].value()) + Y_DIST)
            dot_stamp_bty.setSelected(SELECT_VAL)
            dot_stamp_bty.setInput(0, dot)

            dot.setSelected(NOT_SELECT_VAL)
            curSel.setSelected(NOT_SELECT_VAL)

            # creating BTY stamp
            anchor_title = file_val
            node = dot
            node_type = dot.Class()
            na = stamps.anchor(title=anchor_title, tags="3D", input_node=node, node_type="node_type")
            stamps.stampCreateWired(na)

            for index, n in enumerate(utilities_of_interest):
                # creating dot
                newX = dot['xpos'].value()
                newY = dot['ypos'].value()
                oldDot = dot
                dot = nuke.nodes.Dot()
                dot['xpos'].setValue(int(newX) + X_DIST)
                dot['ypos'].setValue(newY)
                dot.setSelected(SELECT_VAL)
                newDot = dot
                newDot.setInput(0, oldDot)

                # creating shuffle
                shuffle = nuke.nodes.Shuffle2()
                shuffle['in1'].setValue(n)
                shuffle['label'].setValue("<b><center>" + n + "</b></center>")
                shuffle['note_font_size'].setValue(22)
                if n == "Z":
                    shuffle['mappings'].setValue([(0, 'Z.Z', 'rgba.red'), (0, 'Z.Z', 'rgba.green'), (0, 'Z.Z', 'rgba.blue'), (0, 'Z.Z', 'rgba.alpha')])
                shuffle['xpos'].setValue(int(dot['xpos'].value()) - 36)
                shuffle['ypos'].setValue(int(dot['ypos'].value()) + Y_DIST)
                shuffle.setSelected(SELECT_VAL)
                shuffle.setInput(0, newDot)

                oldDot.setSelected(NOT_SELECT_VAL)
                newDot.setSelected(NOT_SELECT_VAL)
                dot.setSelected(NOT_SELECT_VAL)
                newDot.setSelected(NOT_SELECT_VAL)
                curSel.setSelected(NOT_SELECT_VAL)

                # creating stamps
                anchor_title = shuffle['in1'].value()
                node = shuffle
                node_type = shuffle.Class()
                na = stamps.anchor(title=anchor_title, tags="Utility", input_node=node, node_type="node_type")
                stamps.stampCreateWired(na)

                shuffle['ypos'].setValue(int(shuffle['ypos'].value()) - (Y_DIST / 2))
