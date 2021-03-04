# --------------------------------------------------------------
#  menu.py
#  Version: 1.0.10
#  Last Updated: Apr 2nd, 2020
# --------------------------------------------------------------

# --------------------------------------------------------------
#  GLOBAL IMPORTS ::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

import nuke
import platform
import os
import glob, os

# import bm_NodeSandwich

# from http://www.nukepedia.com/python/ui/iconpanel
# import IconPanel


# --------------------------------------------------------------
#  PYCHARM CHEAT SHEET :::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

# Ctrl + '/' - shortcut for comment out and remove comment
# Ctrl + 'D' - duplicate line
# TAB - indent selected line(s)
# TAB + SHIFT - unindent selected line(s)

# --------------------------------------------------------------
#  KNOB DEFAULTS  ::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

## https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/setting_default_parameter_values.html

# -------- LABEL ---------------

#image
nuke.knobDefault('Read.label', "Fr. range: [value first] - [value last]\nRes: [value width] * [value height]")
nuke.knobDefault('Write.label', "Channels: [string toupper [value channel]]")
nuke.knobDefault('Constant.label', "Res: [value width] * [value height]")
nuke.knobDefault('CheckerBoard2.label', "Res: [value width] * [value height]")

#draw

#time
nuke.knobDefault('TimeOffset.label', "Value: [value time_offset]")
nuke.knobDefault('Retime.label', "Out: [value output.first] - [value output.last]")

#channel
nuke.knobDefault('Shuffle.label', "[string toupper [value in1]]")
nuke.knobDefault('ShuffleCopy.label', "[string toupper [value in]]")

#color
nuke.knobDefault('Colorspace.label', "[value colorspace_in] to [value colorspace_out]")
nuke.knobDefault('OCIOColorSpace.label', "[value in_colorspace] to [value out_colorspace]")
nuke.knobDefault('Saturation.label', "Value: [value saturation]")
nuke.knobDefault('Multiply.label', "Value: [value value]")

#filter
nuke.knobDefault('Blur.label', "Size: [value size]")
nuke.knobDefault('Defocus.label', "Size: [value defocus]")
nuke.knobDefault('ZDefocus2.label', "Size: [value size]")
nuke.knobDefault('EdgeBlur.label', "Size: [value size]")
nuke.knobDefault('Sharpen.label', "Size: [value size]")
nuke.knobDefault('Soften.label', "Size: [value size]")

#keyer

#merge
nuke.knobDefault('Switch.label', "Which: [value which]")
nuke.knobDefault('Dissolve.label', "Which: [value which]")

#transform
nuke.knobDefault('Crop.label', "Box: x:[value box.x]  y:[value box.y] r:[value box.r] t:[value box.t]")
nuke.knobDefault('IDistort.label', "Scale: [value uv_scale]")
nuke.knobDefault('SplineWarp3.label', "Out: [string toupper [value output_enum]]")
nuke.knobDefault('STMap.label', "UV: [value uv]")
nuke.knobDefault('VectorDistort.label', "Ref fr.: [value reference_frame]\nOutput: [value output_mode]")
nuke.knobDefault('Reformat.label', '''[if {[value this.type]=="scale"} {return "Scale: [value this.scale]"} {return ""}]''')

#3D
nuke.knobDefault('Camera2.label', "File: [file tail [value file]]")
nuke.knobDefault('ReadGeo2.label', "File: [file tail [value file]]\n[string toupper [value display]]\nRender: [string toupper [value render_mode]]")
nuke.knobDefault('Card2.label', "Display: [string toupper [value display]]\nRender: [string toupper [value render_mode]]")
nuke.knobDefault('Cube.label', "Display: [string toupper [value display]]\nRender: [string toupper [value render_mode]]")
nuke.knobDefault('Cylinder.label', "Display: [string toupper [value display]]\nRender: [string toupper [value render_mode]]")
nuke.knobDefault('Sphere.label', "Display: [string toupper [value display]]\nRender: [string toupper [value render_mode]]")
nuke.knobDefault('Scene.label', "Display: [string toupper [value display]]\nRender: [string toupper [value render_mode]]")

#other
nuke.knobDefault('nuke_dispatch.label', '''Range: [value framestart] - [value frameend]\nBatch: [value batch]\nLic. Rem.: [if {[value removelicense]==true} {return "On"} {return "Off"}]\n[if { [value framestart] == [getenv FS] && [value frameend] == [getenv FE]} {return [knob tile_color 16711935]} else {return [knob tile_color 4278190335]}]''')

# ------------ OTHER KNOBS ------------

#image

#draw
nuke.knobDefault('Text2.xjustify', "center")
nuke.knobDefault('Text2.yjustify', "center")

#time

#channel

#color

#filter
nuke.knobDefault('Blur.size', "2")
nuke.knobDefault('DirBlurWrapper.BlurTye', "linear")
nuke.knobDefault('DirBlurWrapper.BlurLayer', "rgba")

#keyer

#merge
# nuke.knobDefault('Merge.bbox', 'B')
nuke.knobDefault('Merge.also_merge', 'all')
nuke.knobDefault('ContactSheet.roworder', 'TopBottom')
nuke.knobDefault('ContactSheet.width', 'input.width*columns')
nuke.knobDefault('ContactSheet.height', 'input.height*rows')

#transform


#3D
nuke.knobDefault('Project3D.crop', "false")


#other

nuke.knobDefault('Dot.note_font_size', "72")
nuke.knobDefault('BackdropNode.note_font_size', "72")
nuke.knobDefault('StickyNote.note_font_size', "22")


# --------------------------------------------------------------
#  CUSTOM MENUS :::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

## https://learn.foundry.com/nuke/developers/113/pythondevguide/custom_ui.html

# ----- CREATE GM GIZMOS MENU & ASSIGN ITEMS ---------------

GM_Menu = nuke.menu('Nodes').addMenu('GMmenu', icon="gm_icon.png", index=17)

GM_Menu.addCommand('GM_Alpha_Puli', 'nuke.createNode("GM_Alpha_Puli")', icon="")
GM_Menu.addCommand('GM_Channel_Puli', 'nuke.createNode("GM_Channel_Puli")', icon="")
GM_Menu.addCommand('GM_Camera_Around', 'nuke.createNode("GM_Camera_Around")', icon="")
GM_Menu.addCommand('GM_Repeater', 'nuke.createNode("GM_Repeater")', icon="")
GM_Menu.addCommand('GM_ShapeRepeater', 'nuke.createNode("GM_ShapeRepeater")', icon="")
GM_Menu.addCommand('GM_Moving_Lines', 'nuke.createNode("GM_Moving_Lines")', icon="")
GM_Menu.addCommand('GM_CrossPatern', 'nuke.createNode("GM_CrossPattern")', icon="")
GM_Menu.addCommand('GM_Matte_Edge', 'nuke.createNode("GM_Matte_Edge")', icon="")
GM_Menu.addCommand('GM_Round_Matte', 'nuke.createNode("GM_Round_Matte")', icon="")
GM_Menu.addCommand('GM_TransformColorTexture', 'nuke.createNode("GM_TransformColorTexture")', icon="")
GM_Menu.addCommand('GM_Color_Flicker', 'nuke.createNode("GM_Color_Flicker")', icon="")
GM_Menu.addCommand('GM_Liquid_Distortion', 'nuke.createNode("GM_Liquid_Distortion")', icon="")
GM_Menu.addCommand('GM_Overscan', 'nuke.createNode("GM_Overscan")', icon="")
GM_Menu.addCommand('GM_Script_Boost', 'nuke.createNode("GM_Script_Boost")', icon="")
GM_Menu.addCommand('GM_Input_Info', 'nuke.createNode("GM_Input_Info")', icon="")
GM_Menu.addCommand('GM_Render_Switch', 'nuke.createNode("GM_Render_Switch")', icon="")
GM_Menu.addCommand('GM_Switch_Highlight', 'nuke.createNode("GM_Switch_Highlight")', icon="")



# ----- CREATE UTILITIES MENU & ASSIGN ITEMS -------------------

utilitiesMenu = nuke.menu('Nuke').addMenu('My Menu')

utilitiesMenu.addCommand( 'message', "nuke.message('yay, it works too')", index=0 )


# --------------------------------------------------------------
#  USEFUL SNIPPETS :::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

# From https://www.ftrack.com/en/2019/09/8-ways-to-increase-your-efficiency-with-foundrys-nuke.html

def close():
    for node in nuke.allNodes():
        node.hideControlPanel()

utilitiesMenu.addCommand('close', 'close()' , 'shift+d', index=1 )

# Tracker ref frame on current frame

nuke.addOnUserCreate( lambda :nuke.thisNode()[ 'reference_frame' ].setValue(nuke.frame()), nodeClass= 'Tracker4' )

# From http://www.lookinvfx.com/nuke-python-snippets/

def disconnectViewers():
    nuke.selectAll()
    nuke.invertSelection()

    for n in nuke.allNodes():
        if n.Class() == "Viewer":
            n['selected'].setValue(True)

    nuke.extractSelected()

nuke.addOnScriptLoad(disconnectViewers)

# based on Ben`s Foundry webinar: https://app.livestorm.co/foundry/foundry-session-how-to-improve-your-nuke-workflow-with-python-scripting

def RotoBlur_Shortcut():
    y_offset = 60
    r = nuke.createNode('Roto', 'output alpha')
    y = int(r.ypos() + y_offset)
    b = nuke.nodes.Blur()
    b['size'].setValue(2)
    b['label'].setValue('Size: [value size]')
    b['xpos'].setValue(r.xpos())
    b['ypos'].setValue(y)
    b.setInput(0,r)
    b.hideControlPanel()

nuke.menu('Nodes').addMenu('Draw').addCommand('Create Roto and Blur node.', 'RotoBlur_Shortcut()', shortcut='o', icon='Roto.png')

# based on Ben`s NodeSandwhich: https://github.com/BenMcEwan/nuke_public/blob/master/python/bm_NodeSandwich.py

def SharpenSandwhich():
    y_offset = 60
    Lo1 = nuke.createNode('Log2Lin')
    Lo1['operation'].setValue('lin2log')
    Lo1.hideControlPanel()
    ySh = int(Lo1.ypos() + y_offset)
    yLo = int(Lo1.ypos() + (90+y_offset))
    Sh = nuke.nodes.Sharpen()
    Sh['size'].setValue(3)
    Sh['label'].setValue('Size: [value size]')
    Sh['xpos'].setValue(Lo1.xpos())
    Sh['ypos'].setValue(ySh)
    Sh.setInput(0,Lo1)
    Lo2 = nuke.nodes.Log2Lin()
    Lo2['operation'].setValue('log2lin')
    Lo2['xpos'].setValue(Lo1.xpos())
    Lo2['ypos'].setValue(yLo)
    Lo2.setInput(0,Sh)
    Lo2.hideControlPanel()
    Sh.showControlPanel()


nuke.menu('Nodes').addMenu('Filter').addCommand('SharpenSandwhich', 'SharpenSandwhich()', shortcut='ctrl+l', icon='Sharpen.png', index=26)



# Written by Attila Gasparetz based on https://community.foundry.com/discuss/topic/154100/how-to-open-folder-from-write-node

def openFolder():
    import platform
    import subprocess
    import os

    multipleNodes = nuke.selectedNodes()

    if len(multipleNodes) == 0 or len(multipleNodes) > 1:
        nuke.message("""<center><font color=orange>Select a single node with a <font color=yellow><u><a href="https://learn.foundry.com/nuke/developers/63/ndkdevguide/knobs-and-handles/knobtypes.html#knobs-knobtypes-file-knob"><font color=yellow>File</a></u><font color=orange> knob!""")

    else:
        fileNode = nuke.selectedNode()

        if fileNode.knob('file'):
            # get path to directory
            dirname = fileNode.knob('file').evaluate()
            dirname = os.path.dirname(dirname)

            operatingSystem = platform.system()

            if os.path.isdir(dirname):

                # windows
                if operatingSystem == 'Windows':
                    os.startfile(dirname)
                # mac
                elif operatingSystem == 'Darwin':
                    subprocess.Popen(['open', dirname])
                # linux
                else:
                    subprocess.Popen(['xdg-open', dirname])

            else:
                nuke.message("<center><font color=orange>The folder wasn't created yet to open!")

        else:
            nuke.message(
                """<center><font color=orange>Select a single node with a <font color=yellow><u><a href="https://learn.foundry.com/nuke/developers/63/ndkdevguide/knobs-and-handles/knobtypes.html#knobs-knobtypes-file-knob"><font color=yellow>File</a></u><font color=orange> knob!""")

utilitiesMenu.addCommand('Open Folder in file browser', 'openFolder()', shortcut='ctrl+f', index=4)

# Create Backdrop_Adjust

def create_BD_Adj():
    z_List = []
    if nuke.selectedNodes():

        if nuke.selectedNodes('BackdropNode'):
            sel_bd = nuke.selectedNodes('BackdropNode')
            for s in sel_bd:
                z_List.append(s['z_order'].value())
            else:
                pass

        if not z_List:
            z_List.append(1)
        z_Min = min(z_List)


        nodes = nuke.selectedNodes()

        # Calculate bounds for the backdrop node.
        bdX = min([node.xpos() for node in nodes])
        bdY = min([node.ypos() for node in nodes])
        bdW = max([node.xpos() + node.screenWidth() for node in nodes]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in nodes]) - bdY

        # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
        left, top, right, bottom = (-100, -200, 100, 100)
        bdX += left
        bdY += top
        bdW += (right - left)
        bdH += (bottom - top)

        # Creating the node
        bd_this = nuke.nodes.Backdrop_Adjust()
        bd_this["xpos"].setValue(bdX)
        bd_this["bdwidth"].setValue(bdW)
        bd_this["ypos"].setValue(bdY)
        bd_this["bdheight"].setValue(bdH)
        bd_this['z_order'].setValue(z_Min - 1)

        # Handle tile_color by Borsari Nicola
        ok_colors = [3149642751, 2863311615, 2576980479, 2290649343, 2004318207, 1717987071, 1431655935, 1145324799,
                     572662527, 286331391, 255]

        if nuke.selectedNodes('BackdropNode'):
            existing_indexes = [0]
            for bd in nuke.selectedNodes('BackdropNode'):
                color = int(bd['tile_color'].getValue())
                try:
                    curr_index = ok_colors.index(color)
                    existing_indexes.append(curr_index)
                except ValueError:
                    continue

            new_index = sorted(existing_indexes)[-1] + 1

            try:
                bd_this['tile_color'].setValue(ok_colors[new_index])
            except IndexError:
                bd_this['tile_color'].setValue(ok_colors[-1])
        else:
            bd_this['tile_color'].setValue(3149642751)

        bd_this.hideControlPanel()
    else:
        bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that['tile_color'].setValue(3149642751)
        bd_that['z_order'].setValue(0)
        bd_that.hideControlPanel()

nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust.', 'create_BD_Adj()', shortcut='ctrl+b', icon='Backdrop.png', index=3)



####-----------####
#### TextFixer ####
####-----------####
## by Attila Gasparetz
## Version: 1.0.02
## Last Updated: 02/03/2021
## For more info: https://www.gatimedia.co.uk/oldtext2newtext

import sys
import webbrowser

# Creating custom menu
TextFixer = nuke.menu('Nuke').addMenu('Text Fixer')


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


TextFixer.addCommand('Old Text Node Finder', 'oldTextFinder()')


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


TextFixer.addCommand('Old Text 2 New Text', 'OldText2NewText()')


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


TextFixer.addCommand('New Text Node Finder', 'newTextFinder()')


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


TextFixer.addCommand('New Text 2 Old Text', 'NewText2OldText()')


def OpenPage():
    webbrowser.open('https://www.gatimedia.co.uk/oldtext2newtext')


TextFixer.addCommand('Open Page', 'OpenPage()')


# --------------------------------------------------------------
#  SHORTCUTS ::::::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

nuke.toolbar('Nodes').addCommand('Channel/ChannelMerge', 'nuke.createNode("ChannelMerge")', 'shift+c', shortcutContext=dagContext)
