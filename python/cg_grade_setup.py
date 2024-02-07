# --------------------------------------------------------------
#  cg_grade_setup.py
#  Version: 2.0
#  Last Updated: 07/02/2024
#  Last updated by: Attila Gasparetz
# --------------------------------------------------------------
# This tool is based on an AOV naming customization where Color ( Lighting ), Material and Texture groups gets prefixes, respectively "C_", "M_" and "T_"

import nuke

COLOR_LAYER_PREFIX = 'C_'
MATERIAL_LAYER_PREFIX = 'M_'
TEXTURE_LAYER_PREFIX = 'T_'
X_DIST = 1000
Y_DIST = 200
GRADE_DIST = 2500
SELECT_VAL = True

#TODO - ADD UNPREMULT BEFORE SHUFFLE ( ON ALL ) AND PREMULT BEFORE COPY

#TODO - REMOVE ANY LAYERS THAT HAS "mask" IN THE NAME

#TODO - MAKE XPOS/YPOS CHANGES BETWEEN DOT AND OTHER NODE SIZES MORE ELEGANT

def get_layers():
    sel_node_for_layers = nuke.selectedNode()
    cur_sel_channels = sel_node_for_layers.channels()
    layers_list = []
    for raw_channels in cur_sel_channels:
        split_raw_channels = raw_channels.split('.')
        layers_list.append(split_raw_channels[0])
    channel_layers = list(set(layers_list))
    channel_layers.sort()
    return channel_layers

def get_color_layers(channel_layers):
    # Collecting all color/lighting layers
    color_group = []
    for c in channel_layers:
        if c.startswith(COLOR_LAYER_PREFIX):
            color_group.append(c)
        else:
            continue
    # Separating C_direct and C_indirect from the ones starting with C_rgba_ to avoid doubling the Beauty
    color_combined_group = []
    color_emitter_prefix = "C_rgba_"
    if 'C_direct' in color_group:
        # if color_emitter_prefix.startswith(tuple(color_group)):
        color_group.remove('C_direct')
        color_group.remove('C_indirect')
        color_combined_group.append('C_direct')
        color_combined_group.append('C_indirect')
    return color_group, color_combined_group

def get_material_layers(channel_layers):
    # Collecting material layers
    material_group = []
    for c in channel_layers:
        if c.startswith(MATERIAL_LAYER_PREFIX):
            material_group.append(c)
        else:
            continue

    # Removing passes that would make combined Beauty brighter
    for l in material_group:
        if "M_specular_direct" in l:
            material_group.remove("M_specular")
    for l in material_group:
        if "M_diffuse_direct" in l:
            material_group.remove("M_diffuse")

    return material_group

def get_texture_layer(channel_layers):
    texture_group = []
    for c in channel_layers:
        if c.startswith(TEXTURE_LAYER_PREFIX):
            texture_group.append(c)
        else:
            continue
    if "T_diffuse_albedo" in texture_group:
        if "T_albedo" in texture_group:
            texture_group.remove("T_albedo")
    return texture_group

def top_part(channel_layers):
    sel_node = nuke.selectedNode()

    # create dotMain
    dotMain = nuke.nodes.Dot()
    dotMain['xpos'].setValue(int(sel_node['xpos'].value()) + (sel_node.screenWidth() / 2) - (dotMain.screenWidth() / 2))
    dotMain['ypos'].setValue(int(sel_node['ypos'].value()) + 300)
    dotMain.setSelected(SELECT_VAL)
    dotMain.setInput(0, sel_node)

    # creating middle_dot
    middle_dot = nuke.nodes.Dot()
    middle_dot['xpos'].setValue(int(dotMain['xpos'].value()) + 220)
    middle_dot['ypos'].setValue(int(dotMain['ypos'].value()))
    middle_dot.setSelected(SELECT_VAL)
    middle_dot.setInput(0, dotMain)

    # creating layerContact
    layerContact = nuke.nodes.LayerContactSheet()
    layerContact['xpos'].setValue(int(middle_dot['xpos'].value()) + 190)
    layerContact['ypos'].setValue(int(dotMain['ypos'].value()))
    layerContact['showLayerNames'].setValue(True)
    layerContact.setSelected(SELECT_VAL)
    layerContact.setInput(0, middle_dot)

    # Creating a value to be used on the Sticky Note on the side
    layers_for_stickynote = '' + '\n'.join(channel_layers)

    # creating stickyNote
    stickyNote = nuke.nodes.StickyNote()
    stickyNote['xpos'].setValue(int(layerContact['xpos'].value()) - 40)
    stickyNote['ypos'].setValue(int(layerContact['ypos'].value()) + 200)
    stickyNote['label'].setValue("<h2><center>Available layers:\n\n" + layers_for_stickynote + "\n\n")
    stickyNote.setSelected(SELECT_VAL)

    return dotMain, middle_dot

def loop_part(choosen_group, dotMain, choosen_type, texture_group):

    # create dot
    dot = connectDot = nuke.nodes.Dot()
    dot['xpos'].setValue(int(dotMain['xpos'].value()) - X_DIST)
    dot['ypos'].setValue(int(dotMain['ypos'].value()))
    dot.setSelected(SELECT_VAL)
    dot.setInput(0, dotMain)

    # create removeN
    removeN = nuke.nodes.Remove()
    removeN['operation'].setValue('remove')
    removeN['channels'].setValue('all')
    removeN['xpos'].setValue(int(connectDot['xpos'].value()) - 36)
    removeN['ypos'].setValue(int(connectDot['ypos'].value()) + 200)
    removeN.setSelected(SELECT_VAL)
    removeN.setInput(0, connectDot)

    mergeFromold = None
    mergePlusOld = None

    for index, n in enumerate(choosen_group):
        # creating dot
        newX = dot['xpos'].value()
        newY = dot['ypos'].value()
        oldDot = dot
        dot = nuke.nodes.Dot()
        dot['xpos'].setValue(int(newX) - X_DIST)
        dot['ypos'].setValue(newY)
        dot.setSelected(SELECT_VAL)
        newDot = dot
        newDot.setInput(0, oldDot)

        # creating shuffle
        shuffle = nuke.nodes.Shuffle2()
        shuffle['in1'].setValue(n)
        shuffle['label'].setValue("<b>" + n)
        shuffle['note_font_size'].setValue(25)
        shuffle['xpos'].setValue(int(dot['xpos'].value()) - (shuffle.screenWidth() / 2) + (dot.screenWidth() / 2))
        shuffle['ypos'].setValue(int(dot['ypos'].value()) + 100)
        shuffle.setSelected(SELECT_VAL)
        shuffle.setInput(0, newDot)

        # creating Copy
        copy = nuke.nodes.Copy()
        copy['from0'].setValue('alpha')
        copy['to0'].setValue('alpha')
        copy['xpos'].setValue(int(shuffle['xpos'].value()))
        copy['ypos'].setValue(int(shuffle['ypos'].value()) + 100)
        copy.setSelected(SELECT_VAL)
        copy.setInput(0, shuffle)
        copy.setInput(1, newDot)

        # creating dotshuf
        dotshuf = nuke.nodes.Dot()
        dotshuf['xpos'].setValue(
            int(shuffle['xpos'].value()) - (dotshuf.screenWidth() / 2) + (shuffle.screenWidth() / 2))
        dotshuf['ypos'].setValue(int(dot['ypos'].value()) + int(index * Y_DIST) + 350)
        dotshuf.setSelected(SELECT_VAL)
        dotshuf.setInput(0, copy)

        # creating mergeFrom
        mergeFrom = nuke.nodes.Merge2()
        mergeFrom['xpos'].setValue(int(connectDot['xpos'].value()) - (len(choosen_group) + 1) * X_DIST)
        mergeFrom['ypos'].setValue(int(dotshuf['ypos'].value()) - (mergeFrom.screenHeight() / 2))
        mergeFrom['operation'].setValue('from')
        mergeFrom['Achannels'].setValue('rgb')
        mergeFrom['Bchannels'].setValue('rgb')
        mergeFrom['output'].setValue('rgb')
        mergeFrom['label'].setValue(n)
        mergeFrom.setSelected(SELECT_VAL)
        mergeFrom.setInput(1, dotshuf)
        if mergeFrom:
            mergeFrom.setInput(0, mergeFromold)
        if index == 0:
            mergefirst = mergeFrom

        if index + 1 == len(choosen_group):
            # creating dotUpCorner
            dotUpCorner = nuke.nodes.Dot()
            dotUpCorner['xpos'].setValue(int(mergeFrom['xpos'].value()) + 36)
            dotUpCorner['ypos'].setValue(int(newDot['ypos'].value()))
            dotUpCorner.setSelected(SELECT_VAL)
            dotUpCorner.setInput(0, newDot)

            mergefirst.setInput(0, dotUpCorner)

        mergeFromold = mergeFrom

        # creating dotgrade
        dotgrade = nuke.nodes.Dot()
        dotgrade['xpos'].setValue(int(dotshuf['xpos'].value()))
        dotgrade['ypos'].setValue(int(dot['ypos'].value()) + int((len(choosen_group) + 2) * Y_DIST) + 250)
        dotgrade['label'].setValue("  <h1>" + n + "</h1>")
        dotgrade['note_font_size'].setValue(30)
        dotgrade.setSelected(SELECT_VAL)
        dotgrade.setInput(0, dotshuf)

        # creating unprem
        unprem = nuke.nodes.Unpremult()
        unprem['xpos'].setValue(int(shuffle['xpos'].value()))
        unprem['ypos'].setValue(int(dotgrade['ypos'].value()) + 100)
        unprem.setSelected(SELECT_VAL)
        unprem.setInput(0, dotgrade)

        if choosen_type == "material" or choosen_type == "full_setup":
            if texture_group:
                ### START OF MERGE DIVIDE / MULTIPLY SECTION ON MAIN PIPE

                # creating dot_divide
                dot_divide = nuke.nodes.Dot()
                dot_divide['xpos'].setValue(int(dotgrade['xpos'].value()) - 120)
                dot_divide['ypos'].setValue(int(unprem['ypos'].value()) + 100)
                dot_divide.setSelected(SELECT_VAL)
                if index == 0:
                    old_dot_divide = dot_divide
                else:
                    old_dot_divide.setInput(0, dot_divide)
                    old_dot_divide = dot_divide

                # creating merge_divide
                merge_divide = nuke.nodes.Merge2()
                merge_divide['xpos'].setValue(int(unprem['xpos'].value()))
                merge_divide['ypos'].setValue(int(unprem['ypos'].value()) + 200)
                merge_divide['operation'].setValue('divide')
                merge_divide['Achannels'].setValue('rgb')
                merge_divide['Bchannels'].setValue('rgb')
                merge_divide['output'].setValue('rgb')
                merge_divide.setSelected(SELECT_VAL)
                merge_divide.setInput(0, old_dot_divide)
                merge_divide.setInput(1, unprem)

                # creating dot_multiply
                dot_multiply = nuke.nodes.Dot()
                dot_multiply['xpos'].setValue(int(dot_divide['xpos'].value()))
                dot_multiply['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST - 300)
                dot_multiply.setSelected(SELECT_VAL)
                if index == 0:
                    old_dot_multiply = dot_multiply
                else:
                    old_dot_multiply.setInput(0, dot_multiply)
                    old_dot_multiply = dot_multiply

                # creating merge_mult
                merge_mult = nuke.nodes.Merge2()
                merge_mult['xpos'].setValue(int(merge_divide['xpos'].value()))
                merge_mult['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST - 200)
                merge_mult['operation'].setValue('multiply')
                merge_mult['Achannels'].setValue('rgb')
                merge_mult['Bchannels'].setValue('rgb')
                merge_mult['output'].setValue('rgb')
                merge_mult.setSelected(SELECT_VAL)
                merge_mult.setInput(0, merge_divide)
                merge_mult.setInput(1, old_dot_multiply)

                ### END OF MERGE DIVIDE / MULTIPLY SECTION ON MAIN PIPE

        # creating prem
        prem = nuke.nodes.Premult()
        prem['xpos'].setValue(int(shuffle['xpos'].value()))
        prem['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST - 100)
        prem.setSelected(SELECT_VAL)
        if choosen_type == "material" or choosen_type == "full_setup":
            if texture_group:
                prem.setInput(0, merge_mult)
        if not texture_group:
            prem.setInput(0, unprem)

        # creating dotgrade2
        dotgrade2 = nuke.nodes.Dot()
        dotgrade2['xpos'].setValue(int(dotgrade['xpos'].value()))
        dotgrade2['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST)
        dotgrade2['label'].setValue("  <h1>" + n + "</h1>")
        dotgrade2['note_font_size'].setValue(30)
        dotgrade2.setSelected(SELECT_VAL)
        dotgrade2.setInput(0, prem)

        # creating dotExpr
        dotExpr = nuke.nodes.Dot()
        dotExpr['xpos'].setValue(int(dotgrade['xpos'].value()))
        dotExpr['ypos'].setValue(int(dotgrade2['ypos'].value()) + int(index * Y_DIST) + 450)
        dotExpr.setSelected(SELECT_VAL)
        dotExpr.setInput(0, dotgrade2)

        # creating mergePlus
        mergePlus = nuke.nodes.Merge2()
        mergePlus['xpos'].setValue(int(removeN['xpos'].value()))
        mergePlus['ypos'].setValue(int(dotExpr['ypos'].value()) - int(mergePlus.screenHeight()/2) + int(dotExpr.screenHeight()/2))
        mergePlus['operation'].setValue('plus')
        mergePlus['Achannels'].setValue('rgb')
        mergePlus['Bchannels'].setValue('rgb')
        mergePlus['output'].setValue('rgb')
        mergePlus['label'].setValue(n)
        mergePlus.setSelected(SELECT_VAL)
        mergePlus.setInput(1, dotExpr)
        if mergePlusOld:
            mergePlus.setInput(0, mergePlusOld)
        else:
            mergePlus.setInput(0, removeN)
        mergePlusOld = mergePlus

    # creating copy_extra
    copy_extra = nuke.nodes.Copy()
    copy_extra['from0'].setValue('alpha')
    copy_extra['to0'].setValue('alpha')
    copy_extra['xpos'].setValue(int(mergeFrom['xpos'].value()))
    copy_extra['ypos'].setValue(int(mergeFrom['ypos'].value()) + 100)
    copy_extra.setSelected(SELECT_VAL)
    copy_extra.setInput(0, mergeFrom)
    copy_extra.setInput(1, dotUpCorner)

    # creating clamp
    clamp = nuke.nodes.Clamp()
    clamp['maximum'].setValue(1000)
    clamp['xpos'].setValue(int(copy_extra['xpos'].value()))
    clamp['ypos'].setValue(int(copy_extra['ypos'].value()) + 50)
    clamp.setSelected(SELECT_VAL)
    clamp.setInput(0, copy_extra)

    # creating dot_leftover
    dot_leftover = nuke.nodes.Dot()
    dot_leftover['xpos'].setValue(int(dotUpCorner['xpos'].value()))
    dot_leftover['ypos'].setValue(int(dotgrade['ypos'].value()))
    dot_leftover['label'].setValue("  <h1>Left_Over</h1>")
    dot_leftover['note_font_size'].setValue(30)
    dot_leftover.setSelected(SELECT_VAL)
    dot_leftover.setInput(0, clamp)

    # creating unprem_extra
    unprem_extra = nuke.nodes.Unpremult()
    unprem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
    unprem_extra['ypos'].setValue(int(unprem['ypos'].value()))
    unprem_extra.setSelected(SELECT_VAL)
    unprem_extra.setInput(0, dot_leftover)

    if choosen_type == "material" or choosen_type == "full_setup":
        if texture_group:
            ### START OF MERGE DIVIDE / MULTIPLY SECTION ON EXTRA PIPE ###

            # creating dot_albedo
            dot_albedo = nuke.nodes.Dot()
            dot_albedo['xpos'].setValue(int(dotUpCorner['xpos'].value()) - X_DIST)
            dot_albedo['ypos'].setValue(int(dotUpCorner['ypos'].value()))
            dot_albedo.setSelected(SELECT_VAL)
            dot_albedo.setInput(0, dotUpCorner)

            # creating albedo_shuffle
            albedo_shuffle = nuke.nodes.Shuffle2()
            albedo_shuffle['in1'].setValue(texture_group[0])
            albedo_shuffle['label'].setValue("<b>albedo")
            albedo_shuffle['note_font_size'].setValue(25)
            albedo_shuffle['xpos'].setValue(
                int(dot_albedo['xpos'].value()) - (albedo_shuffle.screenWidth() / 2) + (dot_albedo.screenWidth() / 2))
            albedo_shuffle['ypos'].setValue(int(dot_albedo['ypos'].value()) + 100)
            albedo_shuffle.setSelected(SELECT_VAL)
            albedo_shuffle.setInput(0, dot_albedo)

            # creating albedo_copy
            albedo_copy = nuke.nodes.Copy()
            albedo_copy['from0'].setValue('alpha')
            albedo_copy['to0'].setValue('alpha')
            albedo_copy['xpos'].setValue(int(albedo_shuffle['xpos'].value()))
            albedo_copy['ypos'].setValue(int(albedo_shuffle['ypos'].value()) + 100)
            albedo_copy.setSelected(SELECT_VAL)
            albedo_copy.setInput(0, albedo_shuffle)
            albedo_copy.setInput(1, dot_albedo)

            # creating albedo_unprem
            albedo_unprem = nuke.nodes.Unpremult()
            albedo_unprem['xpos'].setValue(int(albedo_copy['xpos'].value()))
            albedo_unprem['ypos'].setValue(int(unprem['ypos'].value()))
            albedo_unprem.setSelected(SELECT_VAL)
            albedo_unprem.setInput(0, albedo_copy)

            # creating dot_divide_extra
            dot_divide_extra = nuke.nodes.Dot()
            dot_divide_extra['xpos'].setValue(int(dot_albedo['xpos'].value()))
            dot_divide_extra['ypos'].setValue(int(unprem_extra['ypos'].value()) + 100)
            dot_divide_extra.setSelected(SELECT_VAL)
            old_dot_divide.setInput(0, dot_divide_extra)
            dot_divide_extra.setInput(0, albedo_unprem)

            # creating merge_divide_extra
            merge_divide_extra = nuke.nodes.Merge2()
            merge_divide_extra['xpos'].setValue(int(unprem_extra['xpos'].value()))
            merge_divide_extra['ypos'].setValue(int(unprem_extra['ypos'].value()) + 200)
            merge_divide_extra['operation'].setValue('divide')
            merge_divide_extra['Achannels'].setValue('rgb')
            merge_divide_extra['Bchannels'].setValue('rgb')
            merge_divide_extra['output'].setValue('rgb')
            merge_divide_extra.setSelected(SELECT_VAL)
            merge_divide_extra.setInput(0, dot_divide_extra)
            merge_divide_extra.setInput(1, unprem_extra)

            # creating dot_multiply_extra
            dot_multiply_extra = nuke.nodes.Dot()
            dot_multiply_extra['xpos'].setValue(int(dot_albedo['xpos'].value()))
            dot_multiply_extra['ypos'].setValue(int(dot_leftover['ypos'].value()) + GRADE_DIST - 300)
            dot_multiply_extra.setSelected(SELECT_VAL)
            old_dot_multiply.setInput(0, dot_multiply_extra)
            dot_multiply_extra.setInput(0, dot_divide_extra)

            # creating merge_mult_extra
            merge_mult_extra = nuke.nodes.Merge2()
            merge_mult_extra['xpos'].setValue(int(merge_divide_extra['xpos'].value()))
            merge_mult_extra['ypos'].setValue(int(dot_leftover['ypos'].value()) + GRADE_DIST - 200)
            merge_mult_extra['operation'].setValue('multiply')
            merge_mult_extra['Achannels'].setValue('rgb')
            merge_mult_extra['Bchannels'].setValue('rgb')
            merge_mult_extra['output'].setValue('rgb')
            merge_mult_extra.setSelected(SELECT_VAL)
            merge_mult_extra.setInput(0, merge_divide_extra)
            merge_mult_extra.setInput(1, dot_multiply_extra)

            ### END OF MERGE DIVIDE / MULTIPLY SECTION ON EXTRA PIPE

    # creating prem
    prem_extra = nuke.nodes.Premult()
    prem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
    prem_extra['ypos'].setValue(int(prem['ypos'].value()))
    prem_extra.setSelected(SELECT_VAL)
    if choosen_type == "material" or choosen_type == "full_setup":
        if texture_group:
            prem_extra.setInput(0, merge_mult_extra)
    if not texture_group:
        prem_extra.setInput(0, unprem_extra)

    # creating dot_leftover2
    dot_leftover2 = nuke.nodes.Dot()
    dot_leftover2['xpos'].setValue(int(dotUpCorner['xpos'].value()))
    dot_leftover2['ypos'].setValue(int(dotgrade2['ypos'].value()))
    dot_leftover2['label'].setValue("  <h1>Left_Over</h1>")
    dot_leftover2['note_font_size'].setValue(30)
    dot_leftover2.setSelected(SELECT_VAL)
    dot_leftover2.setInput(0, prem_extra)

    # creating dotExprSide
    dotExprSide = nuke.nodes.Dot()
    dotExprSide['xpos'].setValue(int(dot_leftover2['xpos'].value()))
    dotExprSide['ypos'].setValue(int(dotExpr['ypos'].value()) + int(Y_DIST))
    dotExprSide.setSelected(SELECT_VAL)
    dotExprSide.setInput(0, dot_leftover2)

    # creating mergePlusSide
    mergePlusSide = nuke.nodes.Merge2()
    mergePlusSide['xpos'].setValue(int(mergePlus['xpos'].value()))
    mergePlusSide['ypos'].setValue(int(dotExprSide['ypos'].value()) - int(mergePlusSide.screenHeight()/2) + int(dotExprSide.screenHeight()/2))
    mergePlusSide['operation'].setValue('plus')
    mergePlusSide['Achannels'].setValue('rgb')
    mergePlusSide['Bchannels'].setValue('rgb')
    mergePlusSide['output'].setValue('rgb')
    mergePlusSide['label'].setValue("Left_Over")
    mergePlusSide.setSelected(SELECT_VAL)
    mergePlusSide.setInput(1, dotExprSide)
    mergePlusSide.setInput(0, mergePlusOld)

    # creating dotCorner
    dotCorner = nuke.nodes.Dot()
    dotCorner['xpos'].setValue(int(connectDot['xpos'].value()))
    if "C_direct" in choosen_group:
        dotCorner['ypos'].setValue(int(mergePlusSide['ypos'].value()) + (Y_DIST * 14))
    else:
        dotCorner['ypos'].setValue(int(mergePlusSide['ypos'].value()) + (Y_DIST * 10))
    dotCorner.setSelected(SELECT_VAL)
    dotCorner.setInput(0, mergePlusSide)

    # creating copyNode
    copyNode = nuke.nodes.Copy()
    copyNode['xpos'].setValue(int(dotMain['xpos'].value()) - int(copyNode.screenWidth()/2) + int(dotMain.screenWidth()/2))
    copyNode['ypos'].setValue(int(dotCorner['ypos'].value()) - int(copyNode.screenHeight()/2) + int(dotCorner.screenHeight()/2))
    copyNode['channels'].setValue('rgb')
    copyNode.setSelected(SELECT_VAL)
    copyNode.setInput(1, dotCorner)
    copyNode.setInput(0, dotMain)

    bottom_right_corner = copyNode
    if choosen_group == "material":
        top_left_corner = dot_albedo
    else:
        top_left_corner = dotUpCorner

    return bottom_right_corner, top_left_corner

def lighting_setup(channel_layers):
    color_group, color_combined_group = get_color_layers(channel_layers)

    if color_combined_group and color_group:
        ### TOP PART ###
        dotMain, middle_dot = top_part(channel_layers)

        ### FIRST LOOP ###
        choosen_group = color_group
        bottom_right_corner_first, top_left_corner_first = loop_part(choosen_group, dotMain, "lighting", None)

        ### DOT BETWEEN LOOPS ###
        dot_corner = nuke.nodes.Dot()
        dot_corner['xpos'].setValue(int(top_left_corner_first['xpos'].value()) - 880)
        dot_corner['ypos'].setValue(int(top_left_corner_first['ypos'].value()))
        dot_corner.setSelected(SELECT_VAL)
        dot_corner.setInput(0, top_left_corner_first)

        ### SECOND LOOP ###
        choosen_group = color_combined_group
        bottom_right_corner_second, top_left_corner_second = loop_part(choosen_group, dot_corner, "lighting", None)

        # creating dot_divide_bty
        dot_divide_bty = nuke.nodes.Dot()
        dot_divide_bty['xpos'].setValue(int(middle_dot['xpos'].value()))
        dot_divide_bty['ypos'].setValue(int(bottom_right_corner_first['ypos'].value()) + (Y_DIST * 2))
        dot_divide_bty.setSelected(SELECT_VAL)
        dot_divide_bty.setInput(0, middle_dot)

        # creating merge_divide_bty
        merge_divide_bty = nuke.nodes.Merge2()
        merge_divide_bty['xpos'].setValue(int(bottom_right_corner_first['xpos'].value()))
        merge_divide_bty['ypos'].setValue(int(dot_divide_bty['ypos'].value()))
        merge_divide_bty['operation'].setValue('divide')
        merge_divide_bty['Achannels'].setValue('rgb')
        merge_divide_bty['Bchannels'].setValue('rgb')
        merge_divide_bty['output'].setValue('rgb')
        merge_divide_bty.setSelected(SELECT_VAL)
        merge_divide_bty.setInput(0, dot_divide_bty)
        merge_divide_bty.setInput(1, bottom_right_corner_first)

        # creating merge_multiply_bty
        merge_multiply_bty = nuke.nodes.Merge2()
        merge_multiply_bty['xpos'].setValue(int(merge_divide_bty['xpos'].value()))
        merge_multiply_bty['ypos'].setValue(int(bottom_right_corner_second['ypos'].value()))
        merge_multiply_bty['operation'].setValue('multiply')
        merge_multiply_bty['Achannels'].setValue('rgb')
        merge_multiply_bty['Bchannels'].setValue('rgb')
        merge_multiply_bty['output'].setValue('rgb')
        merge_multiply_bty.setSelected(SELECT_VAL)
        merge_multiply_bty.setInput(0, merge_divide_bty)
        merge_multiply_bty.setInput(1, bottom_right_corner_second)

        # creating dot_result
        dot_result = nuke.nodes.Dot()
        dot_result['xpos'].setValue(int(merge_multiply_bty['xpos'].value()) - int(dot_result.screenWidth()/2) + int(merge_multiply_bty.screenWidth()/2))
        dot_result['ypos'].setValue(int(merge_divide_bty['ypos'].value()) + (Y_DIST * 4))
        dot_result.setSelected(SELECT_VAL)
        dot_result.setInput(0, merge_multiply_bty)

        middle_dot = dot_divide_bty

    if color_group and not color_combined_group:
        ### TOP PART ###
        dotMain, middle_dot = top_part(channel_layers)
        ### LOOP PART ###
        choosen_group = color_group
        bottom_right_corner, top_left_corner = loop_part(choosen_group, dotMain, "lighting", None)
        # creating dot_result
        dot_result = nuke.nodes.Dot()
        dot_result['xpos'].setValue(int(bottom_right_corner['xpos'].value()) - int(dot_result.screenWidth() / 2) + int(bottom_right_corner.screenWidth() / 2))
        dot_result['ypos'].setValue(int(bottom_right_corner['ypos'].value()) + (Y_DIST * 4))
        dot_result.setSelected(SELECT_VAL)
        dot_result.setInput(0, bottom_right_corner)

    if color_combined_group and not color_group:
        ### TOP PART ###
        dotMain, middle_dot = top_part(channel_layers)
        ### LOOP PART ###
        choosen_group = color_combined_group
        bottom_right_corner, top_left_corner = loop_part(choosen_group, dotMain, "lighting", None)
        # creating dot_result
        dot_result = nuke.nodes.Dot()
        dot_result['xpos'].setValue(int(bottom_right_corner['xpos'].value()) - int(dot_result.screenWidth() / 2) + int(bottom_right_corner.screenWidth() / 2))
        dot_result['ypos'].setValue(int(bottom_right_corner['ypos'].value()) + (Y_DIST * 4))
        dot_result.setSelected(SELECT_VAL)
        dot_result.setInput(0, bottom_right_corner)

    return dot_result, middle_dot

def material_setup(channel_layers, dotMain, middle_dot):
    material_group = get_material_layers(channel_layers)
    texture_group = get_texture_layer(channel_layers)

    ### TOP PART ###
    # dotMain, middle_dot = top_part(channel_layers)
    ### LOOP PART ###
    bottom_right_corner, top_left_corner = loop_part(material_group, dotMain, "material", texture_group)
    # creating dot_result
    dot_result = nuke.nodes.Dot()
    dot_result['xpos'].setValue(
        int(bottom_right_corner['xpos'].value()) - int(dot_result.screenWidth() / 2) + int(bottom_right_corner.screenWidth() / 2))
    dot_result['ypos'].setValue(int(bottom_right_corner['ypos'].value()) + (Y_DIST * 4))
    dot_result.setSelected(SELECT_VAL)
    dot_result.setInput(0, bottom_right_corner)

    return dot_result

def main(chosen_type):
    channel_layers = get_layers()
    color_group, color_combined_group = get_color_layers(channel_layers)
    material_group = get_material_layers(channel_layers)
    texture_group = get_texture_layer(channel_layers)

    if chosen_type == "lighting":
        if not color_combined_group and not color_group:
            nuke.alert('<font color=orange><center><h3>Please, select a single node with lighting passes!\n(Layers that start with "C_")')
        else:
            lighting_setup(channel_layers)

    if chosen_type == "material":

        if not material_group:
            nuke.alert('<font color=orange><center><h3>Please, select a single node with material passes!\n(Layers that start with "M_")')
        else:
            ### TOP PART ###
            dotMain, middle_dot = top_part(channel_layers)
            ### LOOP PART ###
            material_setup(channel_layers, dotMain, middle_dot)

    if chosen_type == "full_setup":
        if not color_combined_group and not color_group and not material_group:
            nuke.alert('<font color=orange><center><h3>Please, select a single node with lighting and material passes!\n(Lighting passes start with "C_" and material passes start with "M_")')
        else:
            if not color_combined_group and not color_group:
                nuke.alert('<font color=orange><center><h3>Please, select a single node with lighting passes!\n(Layers that start with "C_")')
            if not material_group:
                nuke.alert('<font color=orange><center><h3>Please, select a single node with material passes!\n(Layers that start with "M_")')
        if color_combined_group or color_group:
            if material_group:
                ### LIGHT PART ###
                dot_result, middle_dot = lighting_setup(channel_layers)

                ### INBETWEEN PART ###
                # creating dot_divide_bty
                dot_divide_bty = nuke.nodes.Dot()
                dot_divide_bty['xpos'].setValue(int(middle_dot['xpos'].value()))
                dot_divide_bty['ypos'].setValue(int(dot_result['ypos'].value()) + (Y_DIST * 1))
                dot_divide_bty.setSelected(SELECT_VAL)
                dot_divide_bty.setInput(0, middle_dot)

                # creating merge_divide_bty
                merge_divide_bty = nuke.nodes.Merge2()
                merge_divide_bty['xpos'].setValue(int(dot_result['xpos'].value()) - int(merge_divide_bty.screenWidth()/2) + int(dot_result.screenWidth()/2))
                merge_divide_bty['ypos'].setValue(int(dot_divide_bty['ypos'].value()))
                merge_divide_bty['operation'].setValue('divide')
                merge_divide_bty['Achannels'].setValue('rgb')
                merge_divide_bty['Bchannels'].setValue('rgb')
                merge_divide_bty['output'].setValue('rgb')
                merge_divide_bty.setSelected(SELECT_VAL)
                merge_divide_bty.setInput(0, dot_divide_bty)
                merge_divide_bty.setInput(1, dot_result)

                # creating dot_material_corner
                dot_material_corner = nuke.nodes.Dot()
                dot_material_corner['xpos'].setValue(int(dot_divide_bty['xpos'].value()))
                dot_material_corner['ypos'].setValue(int(dot_divide_bty['ypos'].value()) + (Y_DIST))
                dot_material_corner.setSelected(SELECT_VAL)
                dot_material_corner.setInput(0, dot_divide_bty)

                # creating dot_material_main
                dot_material_main = nuke.nodes.Dot()
                dot_material_main['xpos'].setValue(int(dot_material_corner['xpos'].value()) - (X_DIST * 2))
                dot_material_main['ypos'].setValue(int(dot_material_corner['ypos'].value()))
                dot_material_main.setSelected(SELECT_VAL)
                dot_material_main.setInput(0, dot_material_corner)

                ### MATERIAL PART ###
                dot_result = material_setup(channel_layers, dot_material_main, dot_material_corner)

                ### CONNECTING PART ###
                # creating merge_multiply_bty
                merge_multiply_bty = nuke.nodes.Merge2()
                merge_multiply_bty['xpos'].setValue(int(merge_divide_bty['xpos'].value()))
                merge_multiply_bty['ypos'].setValue(int(dot_result['ypos'].value()))
                merge_multiply_bty['operation'].setValue('multiply')
                merge_multiply_bty['Achannels'].setValue('rgb')
                merge_multiply_bty['Bchannels'].setValue('rgb')
                merge_multiply_bty['output'].setValue('rgb')
                merge_multiply_bty.setSelected(SELECT_VAL)
                merge_multiply_bty.setInput(0, merge_divide_bty)
                merge_multiply_bty.setInput(1, dot_result)

                # creating dot_result
                dot_result = nuke.nodes.Dot()
                dot_result['xpos'].setValue(int(merge_multiply_bty['xpos'].value()) - int(dot_result.screenWidth() / 2) + int(merge_multiply_bty.screenWidth() / 2))
                dot_result['ypos'].setValue(int(merge_multiply_bty['ypos'].value()) + (Y_DIST * 4))
                dot_result.setSelected(SELECT_VAL)
                dot_result.setInput(0, merge_multiply_bty)
