# coding=utf-8
# --------------------------------------------------------------
#  menu.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 23/10/2023
# --------------------------------------------------------------

nuke.tprint(f'Running {__file__}')

# --------------------------------------------------------------
#  GLOBAL IMPORTS ::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

import nuke
import platform
import os
import glob, os
import webbrowser

# --------------------------------------------------------------
#  PYCHARM CHEAT SHEET :::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

# Ctrl + '/' - shortcut for comment out and remove comment
# Ctrl + 'D' - duplicate line
# TAB - indent selected line(s)
# TAB + SHIFT - unindent selected line(s)
# Alt + Shift + Up Arrow - move line(s) up
# Alt + Shift + Down Arrow - move line(s) down

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
nuke.knobDefault('Merge.label', '[knob tile_color [ expr {[value disable]? 4278190335:0}]]')
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

# ------------ OTHER KNOBS ------------

#image

#draw
nuke.knobDefault('Text2.xjustify', "center")
nuke.knobDefault('Text2.yjustify', "center")

#time

#channel

#color

#filter
nuke.knobDefault('DirBlurWrapper.BlurTye', "linear")
nuke.knobDefault('DirBlurWrapper.BlurLayer', "rgba")

#keyer

#merge
nuke.knobDefault('ContactSheet.roworder', 'TopBottom')
nuke.knobDefault('ContactSheet.width', 'input.width*columns')
nuke.knobDefault('ContactSheet.height', 'input.height*rows')

#transform


#3D
nuke.knobDefault('Project3D.crop', "false")


#other
nuke.knobDefault('Dot.note_font_size', "22")
nuke.knobDefault('BackdropNode.note_font_size', "22")
nuke.knobDefault('StickyNote.note_font_size', "22")
nuke.knobDefault('LayerContactSheet.showLayerNames', "true")


# --------------------------------------------------------------
#  SHORTCUTS ::::::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

# ChannelMerge
nuke.toolbar('Nodes').addCommand('Channel/ChannelMerge', 'nuke.createNode("ChannelMerge")', 'shift+c', shortcutContext=dagContext)
# Shuffle
nuke.toolbar('Nodes').addCommand('Channel/Shuffle', 'nuke.createNode("Shuffle2")', 'h', shortcutContext=dagContext)
# Tracker
nuke.menu('Nodes').addCommand("Transform/Tracker4", "nuke.createNode('Tracker4')", "ctrl+alt+t", icon="Tracker.png", shortcutContext=2)

# --------------------------------------------------------------
#  CUSTOM MENUS ::::::::::::::::::::::::::::::::::::::::::::::::
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
GM_Menu.addCommand('GM_Liquid_Distortion', 'nuke.createNode("GM_Liquid_Distortion")', icon="")
GM_Menu.addCommand('GM_Script_Boost', 'nuke.createNode("GM_Script_Boost")', icon="")
GM_Menu.addCommand('GM_Input_Info', 'nuke.createNode("GM_Input_Info")', icon="")
GM_Menu.addCommand('GM_Render_Switch', 'nuke.createNode("GM_Render_Switch")', icon="")
GM_Menu.addCommand('GM_Switch_Highlight', 'nuke.createNode("GM_Switch_Highlight")', icon="")

# --------------------------------------------------------------
#  USEFUL SNIPPETS :::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

# From http://www.lookinvfx.com/nuke-python-snippets/
def disconnectViewers():
    nuke.selectAll()
    nuke.invertSelection()
    for n in nuke.allNodes():
        if n.Class() == "Viewer":
            n['selected'].setValue(True)
    nuke.extractSelected()
nuke.addOnScriptLoad(disconnectViewers)


# Tracker ref frame on current frame
nuke.addOnUserCreate( lambda :nuke.thisNode()[ 'reference_frame' ].setValue(nuke.frame()), nodeClass= 'Tracker4' )


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

# --------------------------------------------------------------
# CREATE UTILITIES MENU & ASSIGN ITEMS :::::::::::::::::::::::::
# --------------------------------------------------------------

utilitiesMenu = nuke.menu('Nuke').addMenu('GM Menu')

# --------------------------------------------------------------
#   MENU ITEMS :::::::::::::::::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------

def open_gatimedia_site():
    webbrowser.open('https://www.gatimedia.co.uk/tutorials', new=2)

utilitiesMenu.addCommand('Open GatiMedia', 'open_gatimedia_site()')

utilitiesMenu.addSeparator()

us_menu = utilitiesMenu.addMenu('Useful Sites')

def open_ben_mcewan_site():
    webbrowser.open('https://benmcewan.com/blog', new=2)
us_menu.addCommand('Ben McEwan', 'open_ben_mcewan_site()')

def open_chris_fryer_site():
    webbrowser.open('https://www.chrisfryer.co.uk/blog', new=2)
us_menu.addCommand('Chris Fryer', 'open_chris_fryer_site()')

def open_erwan_leroy_site():
    webbrowser.open('https://erwanleroy.com/blog', new=2)
us_menu.addCommand('Erwan Leroy', 'open_erwan_leroy_site()')

def open_kenn_hedin_kalvik_site():
    webbrowser.open('https://www.keheka.com/', new=2)
us_menu.addCommand('Kenn Hedin Kalvik', 'open_kenn_hedin_kalvik_site()')

def open_cameron_carson_site():
    webbrowser.open('https://www.cameroncarson.com/nuke-wave-expressions', new=2)
us_menu.addCommand('Cameron Carson - Wave Expressions', 'open_cameron_carson_site()')


#useful_sites = {
#  "Ben McEwan": "https://benmcewan.com/blog/",
#  "Chris Fryer": "https://www.chrisfryer.co.uk/blog",
#  "Erwan Leroy": "https://erwanleroy.com/blog/",
#  "Kenn Hedin Kalvik": "https://www.keheka.com/",
#  "Cameron Carson - Wave Expressions": "https://www.cameroncarson.com/nuke-wave-expressions",
#  "Mads Hagbarth": "https://hagbarth.net/blog/"
#}
#
#def open_website(url):
#    return lambda: webbrowser.open(url, new=2)
#
#for name, url in useful_sites.items():
#    us_menu.addCommand(name, lambda: open_website(url))


utilitiesMenu.addSeparator()

try:
    import text_fixer
    tf_menu = utilitiesMenu.addMenu('Text Fixer', icon='Text.png')
    tf_menu.addCommand('Old Text Node Finder', 'text_fixer.oldTextFinder()')
    tf_menu.addCommand('Old Text 2 New Text', 'text_fixer.OldText2NewText()')
    tf_menu.addCommand('New Text Node Finder', 'text_fixer.newTextFinder()')
    tf_menu.addCommand('New Text 2 Old Text', 'text_fixer.NewText2OldText()')
    tf_menu.addCommand('Open Page', 'text_fixer.OpenPage()')
except:
    pass

try:
    import move_selected
    ms_menu = utilitiesMenu.addMenu('Move Selected Nodes', icon='Transform.png')
    ms_menu.addCommand('Move 1 ▲', 'move_selected.move_up_one()', shortcut='ctrl+Up')
    ms_menu.addCommand('Move 1 ▼', 'move_selected.move_down_one()', shortcut='ctrl+Down')
    ms_menu.addCommand('Move 1 ◄', 'move_selected.move_left_one()', shortcut='ctrl+Left')
    ms_menu.addCommand('Move 1 ►', 'move_selected.move_right_one()', shortcut='ctrl+Right')
    ms_menu.addSeparator()
    ms_menu.addCommand('Move 10 ▲', 'move_selected.move_up_ten()', shortcut='ctrl+shift+Up')
    ms_menu.addCommand('Move 10 ▼', 'move_selected.move_down_ten()', shortcut='ctrl+shift+Down')
    ms_menu.addCommand('Move 10 ◄', 'move_selected.move_left_ten()', shortcut='ctrl+shift+Left')
    ms_menu.addCommand('Move 10 ►', 'move_selected.move_right_ten()', shortcut='ctrl+shift+Right')
except:
    pass

try:
    import close_properties
    utilitiesMenu.addCommand('Close Properties', 'close_properties.close()', 'shift+d', icon='Tile.png')
except:
    pass

try:
    import gm_autoplace
    utilitiesMenu.addCommand('GM_Autoplace', 'gm_autoplace.gm_autoplace()', 'l', icon="Group.png", shortcutContext=dagContext)
except:
    pass

try:
    import shuffle_rgb
    utilitiesMenu.addCommand('Shuffle RGB', 'shuffle_rgb.shuffleRGB()', 'ctrl+h', icon='CopyNode.png')
except:
    pass

try:
    import layer_shuffle
    utilitiesMenu.addCommand('LayerShuffle', 'layer_shuffle.layerShuffle()', icon='Shuffle.png')
except:
    pass
try:
    import utility_shuffle
    utilitiesMenu.addCommand('Utility Shuffle + Stamps', 'utility_shuffle.utilityShuffle()', icon='Shuffle.png')
except:
    pass
    
try:
    import change_channels
    utilitiesMenu.addCommand('Change Channels', 'change_channels.changeChannels()', 'shift+a', icon='ChannelMerge.png')
except:
    pass

try:
    import add_retime
    utilitiesMenu.addCommand('Add Retime', 'add_retime.addRetime()', icon='Retime.png')
except:
    pass

try:
    import find_animated_nodes
    utilitiesMenu.addCommand('Find Animated Nodes', 'find_animated_nodes.openAnimNodesWindow()', icon='CurveTool.png')
except:
    pass

try:
    import open_folder
    utilitiesMenu.addCommand('Open Folder in file browser', 'open_folder.openFolder()', 'ctrl+f', icon='Read.png')
except:
    pass

try:
    import clean_droppedknobs
    utilitiesMenu.addCommand('Clean DroppedKnobs', 'clean_droppedknobs.cleanDroppedKnobs()')
except:
    pass

try:
    import cg_grade_lighting
    import cg_grade_material
    import cg_grade_all
    cg_grade_menu = utilitiesMenu.addMenu('Dynamic CG Grade Setups (BETA)', icon='Geometry.png')
    cg_grade_menu.addCommand('Lighting Setup', 'cg_grade_lighting.colorLayerSetup()', icon='Geometry.png')
    cg_grade_menu.addCommand('Material Setup', 'cg_grade_material.materialLayerSetup()', icon='Geometry.png')
    cg_grade_menu.addCommand('Full Setup', 'cg_grade_all.cgGradeSetup()', icon='Geometry.png')
except:
    pass

nuke.tprint(f'End of {__file__}')
