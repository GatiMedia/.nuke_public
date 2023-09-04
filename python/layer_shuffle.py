import nuke


def layerShuffle():
    nodes = nuke.selectedNodes()

    X_DIST = 220
    Y_DIST = 200
    SELECT_VAL = True
    if not len(nodes) == 1:
        nuke.alert('<font color=orange><h3>Please, select a single Read node first!')
    else:
        if not nodes[0].Class() == "Read":
            nuke.alert('<font color=orange><h3>Please, select a single Read node first!')
        else:
            curSel = nuke.selectedNode()
            curSelChannels = curSel.channels()
            layersList = []
            for rawChannels in curSelChannels:
                splitRawChannels = rawChannels.split('.')
                layersList.append(splitRawChannels[0])
            channelLayers = list(set(layersList))
            channelLayers.sort()
            noteVal = '' + '\n'.join(channelLayers)

            if len(channelLayers) == 1:
                nuke.alert('<font color=orange><h3><center>Not enough layers to break it down!\n\nOnly found:\n\n<font color=yellow><h4>' + ',\n'.join(channelLayers))
            else:
                # create dotMain
                dot = connectDot = nuke.nodes.Dot()
                dot['xpos'].setValue(int(curSel['xpos'].value()) + (curSel.screenWidth() / 2) - (dot.screenWidth() / 2))
                dot['ypos'].setValue(int(curSel['ypos'].value()) + 300)
                dot.setSelected(SELECT_VAL)
                dot.setInput(0, curSel)

                # creating layerContact
                layerContact = nuke.nodes.LayerContactSheet()
                layerContact['xpos'].setValue(int(dot['xpos'].value())-36)
                layerContact['ypos'].setValue(int(dot['ypos'].value()) + Y_DIST)
                layerContact['showLayerNames'].setValue(True)
                layerContact.setSelected(SELECT_VAL)
                layerContact.setInput(0, dot)

                for index, n in enumerate(channelLayers):
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
                    shuffle['xpos'].setValue(int(dot['xpos'].value())-36)
                    shuffle['ypos'].setValue(int(dot['ypos'].value()) + Y_DIST)
                    shuffle.setSelected(SELECT_VAL)
                    shuffle.setInput(0, newDot)

                # creating stickyNote
                stickyNote = nuke.nodes.StickyNote()
                stickyNote['xpos'].setValue(int(layerContact['xpos'].value()))
                stickyNote['ypos'].setValue(int(layerContact['ypos'].value()) + Y_DIST)
                stickyNote['label'].setValue("<h2><center>Available layers:\n\n" + noteVal + "\n\n")
                stickyNote.setSelected(SELECT_VAL)