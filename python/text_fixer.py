####-----------####
#### TextFixer ####
####-----------####
## by Attila Gasparetz
## Version: 1.0.02
## Last Updated: 02/03/2021
## For more info: https://www.gatimedia.co.uk/oldtext2newtext

import sys
import webbrowser
import nuke

def oldTextFinder():
    oldText = []
    if nuke.allNodes('Text'):
        for node in nuke.allNodes():
            node.setSelected(False)
        for node in nuke.allNodes(recurseGroups=True):
            if node.Class() == "Text":
                try:
                    node.setSelected(True)
                    oldText.append(node.name())
                except Exception:
                    pass
        for i in nuke.allNodes('Group'):
            i.begin()
            for node in nuke.allNodes('Text'):
                try:
                    node.setSelected(True)
                    oldText.append(i.name() + " (is a Group node with Text inside)")
                    nodeNames = [n.name() for n in nuke.selectedNodes()]
                    if nodeNames:
                        i.setSelected(True)
                except Exception:
                    pass
            i.end()
        if nuke.ask(
                "<b><center><font color=orange>These are the old Text ( Class=Text ) nodes in your script:\n\n<font color=yellow>" + ', '.join(
                        oldText) + "\n\n<font color=orange>Would you like to zoom on them?"):
            nuke.zoomToFitSelected()
    else:
        nuke.message(
            """<b><center><font color=orange>GOOD NEWS!\n\nYou don't have any  old Text ( Class=Text ) node in your script.<p style="font-size:60px">&#128512;</p><a href="https://www.gatimedia.co.uk/oldtext2newtext"><font color=yellow><u>Learn about Old vs. New Text\n""")

def OldText2NewText():
    if nuke.selectedNodes('Text'):
        selTextNodes = nuke.selectedNodes('Text')
        for i in nuke.allNodes():
            i.setSelected(False)
        for textnode in selTextNodes:
            textnode.setSelected(True)
        for oldText in nuke.selectedNodes('Text'):
            ###################
            ## OLD TEXT NODE ##
            ###################
            # NAME
            oldText_name = oldText['name'].value()

            # TEXT
            oldText_output = oldText["output"].value()
            oldText_premult = oldText["premult"].value()
            oldText_cliptype = oldText["cliptype"].value()
            oldText_replace = oldText["replace"].value()
            oldText_invert = oldText["invert"].value()
            oldText_opacity = oldText["opacity"].value()
            oldText_maskChannelMask = oldText["maskChannelMask"].value()
            oldText_maskChannelInput = oldText["maskChannelInput"].value()
            oldText_inject = oldText["inject"].value()
            oldText_invert_mask = oldText["invert_mask"].value()
            oldText_message = oldText["message"].toScript()
            # size - font_size
            oldText_size = oldText["size"].value()
            # kerning - tracking
            oldText_kerning = oldText["kerning"].value()
            oldText_leading = oldText["leading"].value()
            oldText_xjustify = oldText["xjustify"].value()
            oldText_yjustify = oldText["yjustify"].value()
            oldText_box = oldText["box"].value()

            oldText_translate_x = oldText["translate"].value(0)
            oldText_translate_y = oldText["translate"].value(1)
            oldText_rotate = oldText["rotate"].value()
            oldText_scale = oldText["scale"].value()
            oldText_skewX = oldText["skewX"].value()
            oldText_skewY = oldText["skewY"].value()
            oldText_skew_order = oldText["skew_order"].value()
            oldText_center = oldText["center"].value()

            # COLOR
            oldText_ramp = oldText["ramp"].value()
            oldText_color = oldText["color"].value()

            # NODE
            oldText_label = oldText["label"].value()
            oldText_note_font_size = oldText["note_font_size"].value()
            oldText_note_font_color = oldText["note_font_color"].value()
            oldText_hide_input = oldText["hide_input"].value()
            oldText_postage_stamp = oldText["postage_stamp"].value()
            oldText_disable = oldText["disable"].value()

            # DEPENDENCIES
            oldText_dependencies = oldText.dependencies()

            # OLDTEXT DEPENDENTS
            oldText_dependents_0 = []
            oldText_dependents_1 = []
            oldText_dependents_2 = []
            oldText_dependents_3 = []
            oldText_dependents_4 = []
            oldText_dependents_5 = []
            oldText_dependents_6 = []
            oldText_dependents_7 = []
            oldText_dependents_8 = []
            oldText_dependents_9 = []
            for node in nuke.allNodes():
                try:
                    if node.input(0).name() == oldText_name:
                        oldText_dependents_0.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(1).name() == oldText_name:
                        oldText_dependents_1.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(2).name() == oldText_name:
                        newText_dependents_2.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(3).name() == oldText_name:
                        oldText_dependents_3.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(4).name() == oldText_name:
                        oldText_dependents_4.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(5).name() == oldText_name:
                        oldText_dependents_5.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(6).name() == oldText_name:
                        oldText_dependents_6.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(7).name() == oldText_name:
                        oldText_dependents_7.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(8).name() == oldText_name:
                        oldText_dependents_8.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(9).name() == oldText_name:
                        oldText_dependents_9.append(node.name())
                except Exception:
                    pass

            # POSITION
            oldText_xpos = oldText['xpos'].value()
            oldText_ypos = oldText['ypos'].value()

            nuke.delete(oldText)

            ###################
            ## NEW TEXT NODE ##
            ###################

            newText = nuke.nodes.Text2()

            # NAME
            newText['name'].setValue(oldText_name)

            # POSITION
            newText['xpos'].setValue(oldText_xpos)
            newText['ypos'].setValue(oldText_ypos)

            # DEPENDENCIES
            if oldText_dependencies:
                try:
                    newText.setInput(0, oldText_dependencies[0])
                except Exception:
                    pass

            # RECONNECT DEPENDENTS
            if oldText_dependents_0:
                try:
                    for node in oldText_dependents_0:
                        nuke.toNode(node).setInput(0, newText)
                except Exception:
                    pass
            if oldText_dependents_1:
                try:
                    for node in oldText_dependents_1:
                        nuke.toNode(node).setInput(1, newText)
                except Exception:
                    pass
            if oldText_dependents_2:
                try:
                    for node in oldText_dependents_2:
                        nuke.toNode(node).setInput(2, newText)
                except Exception:
                    pass
            if oldText_dependents_3:
                try:
                    for node in oldText_dependents_3:
                        nuke.toNode(node).setInput(3, newText)
                except Exception:
                    pass
            if oldText_dependents_4:
                try:
                    for node in oldText_dependents_4:
                        nuke.toNode(node).setInput(4, newText)
                except Exception:
                    pass
            if oldText_dependents_5:
                try:
                    for node in oldText_dependents_5:
                        nuke.toNode(node).setInput(5, newText)
                except Exception:
                    pass
            if oldText_dependents_6:
                try:
                    for node in oldText_dependents_6:
                        nuke.toNode(node).setInput(7, newText)
                except Exception:
                    pass
            if oldText_dependents_7:
                try:
                    for node in oldText_dependents_7:
                        nuke.toNode(node).setInput(7, newText)
                except Exception:
                    pass
            if oldText_dependents_8:
                try:
                    for node in oldText_dependents_8:
                        nuke.toNode(node).setInput(8, newText)
                except Exception:
                    pass
            if oldText_dependents_9:
                try:
                    for node in oldText_dependents_9:
                        nuke.toNode(node).setInput(9, newText)
                except Exception:
                    pass

            # TEXT
            newText["output"].setValue(oldText_output)
            newText["premult"].setValue(oldText_premult)
            newText["cliptype"].setValue(oldText_cliptype)
            newText["replace"].setValue(oldText_replace)
            newText["invert"].setValue(oldText_invert)
            newText["opacity"].setValue(oldText_opacity)
            newText["maskChannelMask"].setValue(oldText_maskChannelMask)
            newText["maskChannelInput"].setValue(oldText_maskChannelInput)
            newText["inject"].setValue(oldText_inject)
            newText["invert_mask"].setValue(oldText_invert_mask)
            newText["message"].setValue(oldText_message)
            # size = font_size
            newText["font_size"].setValue(oldText_size)
            newText["global_font_scale"].setValue(0.6)
            # kerning = tracking
            newText["tracking"].setValue(oldText_kerning)
            newText["leading"].setValue(oldText_leading)
            newText["xjustify"].setValue(oldText_xjustify)
            newText["yjustify"].setValue(oldText_yjustify)
            newText["box"].setValue(oldText_box)

            # COLOR
            newText["ramp"].setValue(oldText_ramp)
            newText["color"].setValue(oldText_color)

            # NODE
            newText["label"].setValue(oldText_label)
            newText["note_font_size"].setValue(oldText_note_font_size)
            newText["note_font_color"].setValue(oldText_note_font_color)
            newText["hide_input"].setValue(oldText_hide_input)
            newText["postage_stamp"].setValue(oldText_postage_stamp)
            newText["disable"].setValue(oldText_disable)

            # GROUPS
            newText.showControlPanel()
            animLayers = newText['group_animations'].getAllItems()
            newText['group_animations'].setSelectedItems(animLayers)
            newText["translate"].setValue(oldText_translate_x, 0)
            newText["translate"].setValue(oldText_translate_y, 1)
            newText["rotate"].setValue(oldText_rotate)
            newText["scale"].setValue(oldText_scale)
            newText["skewX"].setValue(oldText_skewX)
            newText["skewY"].setValue(oldText_skewY)
            newText["skew_order"].setValue(oldText_skew_order)
            newText["center"].setValue(oldText_center)
            newText.hideControlPanel()

            newText.setSelected(True)
    else:
        nuke.message(
            """<center><b><font color=orange>Select some Text nodes first!\n\n<a href="https://www.gatimedia.co.uk/oldtext2newtext"><font color=yellow><u>Learn about Old vs. New Text\n""")

def newTextFinder():
    newText = []
    if nuke.allNodes('Text2'):
        for node in nuke.allNodes():
            node.setSelected(False)
        for node in nuke.allNodes(recurseGroups=True):
            if node.Class() == "Text2":
                try:
                    node.setSelected(True)
                    newText.append(node.name())
                except Exception:
                    pass
        for i in nuke.allNodes('Group'):
            i.begin()
            for node in nuke.allNodes('Text2'):
                try:
                    node.setSelected(True)
                    newText.append(i.name() + " (is a Group node with Text inside)")
                    nodeNames = [n.name() for n in nuke.selectedNodes()]
                    if nodeNames:
                        i.setSelected(True)
                except Exception:
                    pass
            i.end()
        if nuke.ask(
                "<b><center><font color=orange>These are the new Text ( Class=Text2 ) nodes in your script:\n\n<font color=yellow>" + ', '.join(
                        newText) + "\n\n<font color=orange>Would you like to zoom on them?"):
            nuke.zoomToFitSelected()
    else:
        nuke.message(
            """<b><center><font color=orange>GOOD NEWS!\n\nYou don't have any new Text ( Class=Text2 ) node in your script.<p style="font-size:60px">&#128512;</p><a href="https://www.gatimedia.co.uk/oldtext2newtext"><font color=yellow><u>Learn about Old vs. New Text\n""")


def NewText2OldText():
    if nuke.selectedNodes('Text2'):
        selText2Nodes = nuke.selectedNodes('Text2')

        for i in nuke.allNodes():
            i.setSelected(False)

        oldTextTemp = nuke.createNode('Text')
        fontVal = oldTextTemp['font'].value()
        nuke.delete(oldTextTemp)

        for textnode2 in selText2Nodes:
            textnode2.setSelected(True)

        for newText in nuke.selectedNodes('Text2'):
            ###################
            ## NEW TEXT NODE ##
            ###################

            # NAME
            newText_name = newText['name'].value()

            # POSITION
            newText_xpos = newText['xpos'].value()
            newText_ypos = newText['ypos'].value()

            # TEXT
            newText_output = newText["output"].value()
            newText_premult = newText["premult"].value()
            newText_cliptype = newText["cliptype"].value()
            newText_replace = newText["replace"].value()
            newText_invert = newText["invert"].value()
            newText_opacity = newText["opacity"].value()
            newText_maskChannelMask = newText["maskChannelMask"].value()
            newTex_maskChannelInput = newText["maskChannelInput"].value()
            newText_inject = newText["inject"].value()
            newText_invert_mask = newText["invert_mask"].value()
            newText_message = newText["message"].toScript()
            # size = font_size
            newText_font_size = newText["font_size"].value()
            newText_global_font_scale = newText["global_font_scale"].value()
            # kerning = tracking
            newText_tracking = newText["tracking"].value()
            newText_leading = newText["leading"].value()
            newText_xjustify = newText["xjustify"].value()
            newText_yjustify = newText["yjustify"].value()
            newText_box = newText["box"].value()

            # COLOR
            newText_ramp = newText["ramp"].value()
            newText_color = newText["color"].value()

            # NODE
            newText_label = newText["label"].value()
            newText_note_font_size = newText["note_font_size"].value()
            newText_note_font_color = newText["note_font_color"].value()
            newText_hide_input = newText["hide_input"].value()
            newText_postage_stamp = newText["postage_stamp"].value()
            newText_disable = newText["disable"].value()

            # GROUPS
            newText.showControlPanel()
            animLayers = newText['group_animations'].getAllItems()
            newText['group_animations'].setSelectedItems(animLayers)
            newText_translateX = newText["translate"].value(0)
            newText_translateY = newText["translate"].value(1)
            newText_rotate = newText["rotate"].value()
            newText_scale = newText["scale"].value()
            newText_skewX = newText["skewX"].value()
            newText_skewY = newText["skewY"].value()
            newText_skew_order = newText["skew_order"].value()
            newText_center = newText["center"].value()
            newText.hideControlPanel()

            # DEPENDENCIES
            newText_dependencies = newText.dependencies()

            # OLDTEXT DEPENDENTS
            newText_dependents_0 = []
            newText_dependents_1 = []
            newText_dependents_2 = []
            newText_dependents_3 = []
            newText_dependents_4 = []
            newText_dependents_5 = []
            newText_dependents_6 = []
            newText_dependents_7 = []
            newText_dependents_8 = []
            newText_dependents_9 = []
            for node in nuke.allNodes():
                try:
                    if node.input(0).name() == newText_name:
                        newText_dependents_0.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(1).name() == newText_name:
                        newText_dependents_1.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(2).name() == newText_name:
                        newText_dependents_2.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(3).name() == newText_name:
                        newText_dependents_3.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(4).name() == newText_name:
                        newText_dependents_4.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(5).name() == newText_name:
                        newText_dependents_5.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(6).name() == newText_name:
                        newText_dependents_6.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(7).name() == newText_name:
                        newText_dependents_7.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(8).name() == newText_name:
                        newText_dependents_8.append(node.name())
                except Exception:
                    pass
            for node in nuke.allNodes():
                try:
                    if node.input(9).name() == newText_name:
                        newText_dependents_9.append(node.name())
                except Exception:
                    pass

            nuke.delete(newText)

            ###################
            ## OLD TEXT NODE ##
            ###################

            oldText = nuke.nodes.Text()

            # NAME
            oldText['name'].setValue(newText_name)

            # POSITION
            oldText['xpos'].setValue(newText_xpos)
            oldText['ypos'].setValue(newText_ypos)

            # DEPENDENCIES
            if newText_dependencies:
                try:
                    oldText.setInput(0, newText_dependencies[0])
                except Exception:
                    pass

            # RECONNECT DEPENDENTS
            if newText_dependents_0:
                try:
                    for node in newText_dependents_0:
                        nuke.toNode(node).setInput(0, oldText)
                except Exception:
                    pass
            if newText_dependents_1:
                try:
                    for node in newText_dependents_1:
                        nuke.toNode(node).setInput(1, oldText)
                except Exception:
                    pass
            if newText_dependents_2:
                try:
                    for node in newText_dependents_2:
                        nuke.toNode(node).setInput(2, oldText)
                except Exception:
                    pass
            if newText_dependents_3:
                try:
                    for node in newText_dependents_3:
                        nuke.toNode(node).setInput(3, oldText)
                except Exception:
                    pass
            if newText_dependents_4:
                try:
                    for node in newText_dependents_4:
                        nuke.toNode(node).setInput(4, oldText)
                except Exception:
                    pass
            if newText_dependents_5:
                try:
                    for node in newText_dependents_5:
                        nuke.toNode(node).setInput(5, oldText)
                except Exception:
                    pass
            if newText_dependents_6:
                try:
                    for node in newText_dependents_6:
                        nuke.toNode(node).setInput(6, oldText)
                except Exception:
                    pass
            if newText_dependents_7:
                try:
                    for node in newText_dependents_7:
                        nuke.toNode(node).setInput(7, oldText)
                except Exception:
                    pass
            if newText_dependents_8:
                try:
                    for node in newText_dependents_8:
                        nuke.toNode(node).setInput(8, oldText)
                except Exception:
                    pass
            if newText_dependents_9:
                try:
                    for node in newText_dependents_9:
                        nuke.toNode(node).setInput(9, oldText)
                except Exception:
                    pass

            # FONT
            oldText["font"].setValue(fontVal)

            # TEXT
            oldText["output"].setValue(newText_output)
            oldText["premult"].setValue(newText_premult)
            oldText["cliptype"].setValue(newText_cliptype)
            oldText["replace"].setValue(newText_replace)
            oldText["invert"].setValue(newText_invert)
            oldText["opacity"].setValue(newText_opacity)
            oldText["maskChannelMask"].setValue(newText_maskChannelMask)
            oldText["maskChannelInput"].setValue(newTex_maskChannelInput)
            oldText["inject"].setValue(newText_inject)
            oldText["invert_mask"].setValue(newText_invert_mask)
            oldText["message"].setValue(newText_message)
            # size - font_size
            oldText["size"].setValue(newText_font_size)
            # kerning - tracking
            oldText["kerning"].setValue(newText_tracking)
            oldText["leading"].setValue(newText_leading)
            oldText["xjustify"].setValue(newText_xjustify)
            oldText["yjustify"].setValue(newText_yjustify)
            oldText["box"].setValue(newText_box)

            oldText["translate"].setValue(newText_translateX, 0)
            oldText["translate"].setValue(newText_translateY, 1)
            oldText["rotate"].setValue(newText_rotate)
            oldText["scale"].setValue(newText_scale)
            oldText["skewX"].setValue(newText_skewX)
            oldText["skewY"].setValue(newText_skewY)
            oldText["skew_order"].setValue(newText_skew_order)
            oldText["center"].setValue(newText_center)

            # COLOR
            oldText["ramp"].setValue(newText_ramp)
            oldText["color"].setValue(newText_color)

            # NODE
            oldText["label"].setValue(newText_label)
            oldText["note_font_size"].setValue(newText_note_font_size)
            oldText["note_font_color"].setValue(newText_note_font_color)
            oldText["hide_input"].setValue(newText_hide_input)
            oldText["postage_stamp"].setValue(newText_postage_stamp)
            oldText["disable"].setValue(newText_disable)

            oldText.hideControlPanel()

            oldText.setSelected(True)

    else:
        nuke.message(
            """<center><b><font color=orange>Select some Text2 nodes first!\n\n<a href="https://www.gatimedia.co.uk/oldtext2newtext"><font color=yellow><u>Learn about Old vs. New Text\n""")

def OpenPage():
    webbrowser.open('https://www.gatimedia.co.uk/oldtext2newtext')
