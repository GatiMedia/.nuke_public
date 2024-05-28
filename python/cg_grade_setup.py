# --------------------------------------------------------------
#  cg_grade_setup.py
#  Version: 2.5
#  Last Updated: 28/05/2024
#  Last updated by: Attila Gasparetz
# --------------------------------------------------------------
# This tool is based on an AOV naming customization where Color ( Lighting ), Material and Texture groups gets prefixes, respectively "C_", "M_" and "T_"


import nuke

COLOR_LAYER_PREFIX = 'C_'
MATERIAL_LAYER_PREFIX = 'M_'
TEXTURE_LAYER_PREFIX = 'T_'
SELECT_VAL = True
X_DIST = int(nuke.toNode('preferences')['GridWidth'].value() * 7) #770 w def values
Y_DIST = int(nuke.toNode('preferences')['GridHeight'].value() * 4) #96 w def values
GRADE_DIST = int(nuke.toNode('preferences')['GridHeight'].value() * 35) #840 w def values
DOT_GRADE_FONT_SIZE = 25

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

def remove_mask_layers(layers):
    for l in layers:
        if "mask" in l:
            layers.remove(l)
    return layers

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
        color_group.remove('C_direct')
        color_group.remove('C_indirect')
        color_combined_group.append('C_direct')
        color_combined_group.append('C_indirect')
    # Removing passes that has "mask" in the name
    remove_mask_layers(color_group)
    return color_group, color_combined_group

def get_material_layers(channel_layers):
    # Collecting material layers
    material_group = []
    for c in channel_layers:
        if c.startswith(MATERIAL_LAYER_PREFIX):
            material_group.append(c)
        else:
            continue
    # Removing passes that has "mask" in the name
    remove_mask_layers(material_group)
    # Removing passes that would make combined Beauty brighter
    for l in material_group:
        try:
            if "M_specular_direct" in l:
                material_group.remove("M_specular")
        except:
            pass
    for l in material_group:
        try:
            if "M_diffuse_direct" in l:
                material_group.remove("M_diffuse")
        except:
            pass
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
    # return texture_group
    # Updated this function to return None as it seems unnecessary to divide/multiply material passes with the albedo
    return None

def set_center_x(thisnode, othernode):
    thisnode['xpos'].setValue(int(othernode['xpos'].value()+(othernode.screenWidth()/2)-(thisnode.screenWidth()/2)))

def set_center_y(thisnode, othernode):
    thisnode['ypos'].setValue(int(othernode['ypos'].value()+(othernode.screenHeight()/2)-(thisnode.screenHeight()/2)))

def create_unpremult_group(start_point, layers):
    # creating group_unprem_color
    group_unprem_color = nuke.nodes.Group()
    group_unprem_color.setName('Unpremult_Layers1', uncollide=True, updateExpressions=False)
    group_unprem_color['xpos'].setValue(int(start_point['xpos'].value()) - (X_DIST / 2))
    set_center_y(group_unprem_color, start_point)
    group_unprem_color.setSelected(SELECT_VAL)
    group_unprem_color.setInput(0, start_point)

    # Adding Text knobs to the Group node
    knob_1 = nuke.Text_Knob('inf', '')
    group_unprem_color.addKnob(knob_1)
    knob_1.setValue('<b>Unpremultiplied layers:')
    knob_2 = nuke.Text_Knob('rgba_01', '')
    group_unprem_color.addKnob(knob_2)
    knob_2.setValue('<i>rgba')
    for layer_name in layers:
        knob = nuke.Text_Knob(layer_name + "_01", '')
        group_unprem_color.addKnob(knob)
        knob.setValue("<i>" + str(layer_name))

    # populating the Group node with Unpremults
    with group_unprem_color:
        # creating input_color
        input_color = nuke.nodes.Input()
        input_color.setSelected(SELECT_VAL)

        unprem_rgba_color = nuke.nodes.Unpremult()
        unprem_rgba_color['channels'].setValue("rgba")
        unprem_rgba_color['xpos'].setValue(int(input_color['xpos'].value()) - (X_DIST / 4))
        set_center_y(unprem_rgba_color, input_color)
        unprem_rgba_color.setSelected(SELECT_VAL)
        unprem_rgba_color.setInput(0, input_color)

        for index, c_layers in enumerate(layers):
            # creating unprem_color
            unprem_color = nuke.nodes.Unpremult()
            unprem_color['channels'].setValue(c_layers)
            set_center_y(unprem_color, unprem_rgba_color)
            unprem_color.setSelected(SELECT_VAL)
            if index == 0:
                unprem_color.setInput(0, unprem_rgba_color)
                unprem_color['xpos'].setValue(int(unprem_rgba_color['xpos'].value()) - (X_DIST / 4))
                old_unprem_color = unprem_color
            else:
                unprem_color.setInput(0, old_unprem_color)
                unprem_color['xpos'].setValue(int(old_unprem_color['xpos'].value()) - (X_DIST / 4))
                old_unprem_color = unprem_color

        # creating output_color
        output_color = nuke.nodes.Output()
        output_color['xpos'].setValue(int(old_unprem_color['xpos'].value()) - (X_DIST / 4))
        set_center_y(output_color, old_unprem_color)
        output_color.setInput(0, old_unprem_color)
        output_color.setSelected(SELECT_VAL)

    return group_unprem_color

def top_part(channel_layers):
    sel_node = nuke.selectedNode()

    # create dotMain
    dotMain = nuke.nodes.Dot()
    set_center_x(dotMain,sel_node)
    dotMain['ypos'].setValue(int(sel_node['ypos'].value()) + (Y_DIST*3))
    dotMain.setSelected(SELECT_VAL)
    dotMain.setInput(0, sel_node)

    # creating middle_dot
    middle_dot = nuke.nodes.Dot()
    middle_dot['xpos'].setValue(int(dotMain['xpos'].value()) + 220)
    middle_dot['ypos'].setValue(int(dotMain['ypos'].value()))
    middle_dot.setSelected(SELECT_VAL)
    middle_dot.setInput(0, dotMain)

    # creating layer_contact
    layer_contact = nuke.nodes.LayerContactSheet()
    layer_contact['xpos'].setValue(int(middle_dot['xpos'].value()) + 190)
    layer_contact['ypos'].setValue(int(dotMain['ypos'].value()))
    set_center_y(layer_contact,dotMain)
    layer_contact['showLayerNames'].setValue(True)
    layer_contact.setSelected(SELECT_VAL)
    layer_contact.setInput(0, middle_dot)

    # Creating a value to be used on the Sticky Note on the side
    layers_for_stickynote = '' + '\n'.join(channel_layers)

    # creating sticky_note
    sticky_note = nuke.nodes.StickyNote()
    sticky_note['xpos'].setValue(int(layer_contact['xpos'].value()) - 40)
    sticky_note['ypos'].setValue(int(layer_contact['ypos'].value()) + 200)
    sticky_note['label'].setValue("<h2><center>Available layers:\n\n" + layers_for_stickynote + "\n\n")
    sticky_note.setSelected(SELECT_VAL)

    return dotMain, middle_dot

def loop_part(choosen_group, dotMain, choosen_type, texture_group):
    # create dot
    dot = connect_dot = nuke.nodes.Dot()
    dot['xpos'].setValue(int(dotMain['xpos'].value()) - X_DIST)
    set_center_y(dot,dotMain)
    dot.setSelected(SELECT_VAL)
    dot.setInput(0, dotMain)

    # creating unpremult group for lighting layers
    group_unprem_color = create_unpremult_group(dot, choosen_group)

    # create remove_all
    remove_all = nuke.nodes.Remove()
    remove_all['operation'].setValue('remove')
    remove_all['channels'].setValue('all')
    set_center_x(remove_all,dot)
    remove_all['ypos'].setValue(int(connect_dot['ypos'].value()) + Y_DIST)
    remove_all.setSelected(SELECT_VAL)
    remove_all.setInput(0, connect_dot)

    merge_from_old = None
    merge_plus_old = None

    for index, n in enumerate(choosen_group):
        # creating dot
        newX = dot['xpos'].value()
        newY = dot['ypos'].value()
        old_dot = dot
        dot = nuke.nodes.Dot()
        dot['xpos'].setValue(int(newX) - X_DIST)
        dot['ypos'].setValue(newY)
        dot.setSelected(SELECT_VAL)
        # adding color variations to dots
        if index % 2 == 0:
            dot['tile_color'].setValue(2857762815)
        else:
            dot['tile_color'].setValue(4290707711)
        new_dot = dot
        if index == 0:
            new_dot.setInput(0, group_unprem_color)
        else:
            new_dot.setInput(0, old_dot)

        # creating shuffle
        shuffle = nuke.nodes.Shuffle2()
        shuffle['in1'].setValue(n)
        shuffle['in2'].setValue("alpha")
        shuffle['mappings'].setValue([(0, n+'.red', 'rgba.red'), (0, n+'.green', 'rgba.green'), (0, n+'.blue', 'rgba.blue'), (1, 'rgba.alpha', 'rgba.alpha')])
        shuffle['label'].setValue("<b>" + n)
        shuffle['note_font_size'].setValue(25)
        set_center_x(shuffle,dot)
        shuffle['ypos'].setValue(int(dot['ypos'].value()) + (X_DIST/10))
        shuffle.setSelected(SELECT_VAL)
        shuffle.setInput(0, new_dot)

        # creating dotshuf
        dotshuf = nuke.nodes.Dot()
        set_center_x(dotshuf,shuffle)
        dotshuf['ypos'].setValue(int(dot['ypos'].value()) + int(index * Y_DIST) + (Y_DIST*3))
        dotshuf.setSelected(SELECT_VAL)
        dotshuf.setInput(0, shuffle)
        # adding color variations to dots
        if index % 2 == 0:
            dotshuf['tile_color'].setValue(2857762815)
        else:
            dotshuf['tile_color'].setValue(4290707711)

        # creating merge_from
        merge_from = nuke.nodes.Merge2()
        merge_from['operation'].setValue('from')
        merge_from['Achannels'].setValue('rgb')
        merge_from['Bchannels'].setValue('rgb')
        merge_from['output'].setValue('rgb')
        merge_from['label'].setValue(n)
        merge_from['xpos'].setValue(int(connect_dot['xpos'].value()) - (len(choosen_group) + 1) * X_DIST)
        set_center_y(merge_from,dotshuf)
        merge_from.setSelected(SELECT_VAL)
        merge_from.setInput(1, dotshuf)
        if merge_from:
            merge_from.setInput(0, merge_from_old)
        if index == 0:
            mergefirst = merge_from

        if index + 1 == len(choosen_group):
            # creating dot_up_corner
            dot_up_corner = nuke.nodes.Dot()
            set_center_x(dot_up_corner,merge_from)
            dot_up_corner['ypos'].setValue(int(new_dot['ypos'].value()))
            dot_up_corner.setSelected(SELECT_VAL)
            dot_up_corner.setInput(0, new_dot)

            mergefirst.setInput(0, dot_up_corner)

        merge_from_old = merge_from

        if choosen_type == "material" or choosen_type == "full_setup":
            if "M_" in n:
                n_dot = n.replace("M_","")
        if choosen_type == "lighting" or choosen_type == "full_setup":
            if "C_rgba_" in n:
                n_dot = n.replace("C_rgba_","")
            if "C_" in n:
                n_dot = n.replace("C_","")

        # creating dot_grade
        dot_grade = nuke.nodes.Dot()
        dot_grade['xpos'].setValue(int(dotshuf['xpos'].value()))
        dot_grade['ypos'].setValue(int(dot['ypos'].value())+int((len(choosen_group) + 2)*Y_DIST)+(Y_DIST*2))
        dot_grade['label'].setValue("<h1>&nbsp;&nbsp;" + n_dot + "</h1>")
        dot_grade['note_font_size'].setValue(DOT_GRADE_FONT_SIZE)
        dot_grade.setSelected(SELECT_VAL)
        dot_grade.setInput(0, dotshuf)
        # adding color variations to dots
        if index % 2 == 0:
            dot_grade['tile_color'].setValue(2857762815)
        else:
            dot_grade['tile_color'].setValue(4290707711)

        if choosen_type == "material" or choosen_type == "full_setup":
            if texture_group:
                ### START OF MERGE DIVIDE / MULTIPLY SECTION ON MAIN PIPE

                # creating dot_divide
                dot_divide = nuke.nodes.Dot()
                dot_divide['xpos'].setValue(int(dot_grade['xpos'].value()) - 120)
                dot_divide['ypos'].setValue(int(dot_grade['ypos'].value()) + 200)
                dot_divide.setSelected(SELECT_VAL)
                if index == 0:
                    old_dot_divide = dot_divide
                else:
                    old_dot_divide.setInput(0, dot_divide)
                    old_dot_divide = dot_divide

                # creating merge_divide
                merge_divide = nuke.nodes.MergeExpression()
                merge_divide['xpos'].setValue(int(shuffle['xpos'].value()))
                merge_divide['ypos'].setValue(int(dot_grade['ypos'].value()) + 300)
                merge_divide['expr0'].setValue('Ar>0?Br>0?Br/Ar:0:0')
                merge_divide['expr1'].setValue('Ag>0?Bg>0?Bg/Ag:0:0')
                merge_divide['expr2'].setValue('Ab>0?Bb>0?Bb/Ab:0:0')
                merge_divide.setSelected(SELECT_VAL)
                merge_divide.setInput(0, dot_grade)
                merge_divide.setInput(1, old_dot_divide)

                # creating dot_multiply
                dot_multiply = nuke.nodes.Dot()
                dot_multiply['xpos'].setValue(int(dot_divide['xpos'].value()))
                dot_multiply['ypos'].setValue(int(dot_grade['ypos'].value()) + GRADE_DIST - 300)
                dot_multiply.setSelected(SELECT_VAL)
                if index == 0:
                    old_dot_multiply = dot_multiply
                else:
                    old_dot_multiply.setInput(0, dot_multiply)
                    old_dot_multiply = dot_multiply

                # creating merge_mult
                merge_mult = nuke.nodes.Merge2()
                merge_mult['xpos'].setValue(int(merge_divide['xpos'].value()))
                merge_mult['ypos'].setValue(int(dot_grade['ypos'].value()) + GRADE_DIST - 200)
                merge_mult['operation'].setValue('multiply')
                merge_mult['Achannels'].setValue('rgb')
                merge_mult['Bchannels'].setValue('rgb')
                merge_mult['output'].setValue('rgb')
                merge_mult.setSelected(SELECT_VAL)
                merge_mult.setInput(0, merge_divide)
                merge_mult.setInput(1, old_dot_multiply)

                ### END OF MERGE DIVIDE / MULTIPLY SECTION ON MAIN PIPE

        # creating dotgrade2
        dotgrade2 = nuke.nodes.Dot()
        dotgrade2['xpos'].setValue(int(dot_grade['xpos'].value()))
        dotgrade2['ypos'].setValue(int(dot_grade['ypos'].value()) + GRADE_DIST)
        dotgrade2['label'].setValue("<h1>&nbsp;&nbsp;" + n_dot + "</h1>")
        dotgrade2['note_font_size'].setValue(DOT_GRADE_FONT_SIZE)
        dotgrade2.setSelected(SELECT_VAL)
        if choosen_type == "material" or choosen_type == "full_setup":
            if texture_group:
                dotgrade2.setInput(0, merge_mult)
        if not texture_group:
            dotgrade2.setInput(0, dot_grade)
        # adding color variations to dots
        if index % 2 == 0:
            dotgrade2['tile_color'].setValue(2857762815)
        else:
            dotgrade2['tile_color'].setValue(4290707711)

        # creating dot_expr
        dot_expr = nuke.nodes.Dot()
        dot_expr['xpos'].setValue(int(dot_grade['xpos'].value()))
        dot_expr['ypos'].setValue(int(dotgrade2['ypos'].value()) + int(index * Y_DIST) + Y_DIST)
        dot_expr.setSelected(SELECT_VAL)
        dot_expr.setInput(0, dotgrade2)
        # adding color variations to dots
        if index % 2 == 0:
            dot_expr['tile_color'].setValue(2857762815)
        else:
            dot_expr['tile_color'].setValue(4290707711)

        # creating merge_plus
        merge_plus = nuke.nodes.Merge2()
        merge_plus['operation'].setValue('plus')
        merge_plus['Achannels'].setValue('rgb')
        merge_plus['Bchannels'].setValue('rgb')
        merge_plus['output'].setValue('rgb')
        merge_plus['label'].setValue(n)
        merge_plus['xpos'].setValue(int(remove_all['xpos'].value()))
        set_center_y(merge_plus,dot_expr)
        merge_plus.setSelected(SELECT_VAL)
        merge_plus.setInput(1, dot_expr)
        if merge_plus_old:
            merge_plus.setInput(0, merge_plus_old)
        else:
            merge_plus.setInput(0, remove_all)
        merge_plus_old = merge_plus

    # creating copy_extra
    copy_extra = nuke.nodes.Copy()
    copy_extra['from0'].setValue('alpha')
    copy_extra['to0'].setValue('alpha')
    copy_extra['xpos'].setValue(int(merge_from['xpos'].value()))
    copy_extra['ypos'].setValue(int(merge_from['ypos'].value()) + Y_DIST)
    copy_extra.setSelected(SELECT_VAL)
    copy_extra.setInput(0, merge_from)
    copy_extra.setInput(1, dot_up_corner)

    # creating dot_leftover
    dot_leftover = nuke.nodes.Dot()
    dot_leftover['xpos'].setValue(int(dot_up_corner['xpos'].value()))
    dot_leftover['ypos'].setValue(int(dot_grade['ypos'].value()))
    dot_leftover['label'].setValue("  <h1>&nbsp;&nbsp;Left_Over</h1>")
    dot_leftover['note_font_size'].setValue(DOT_GRADE_FONT_SIZE)
    dot_leftover.setSelected(SELECT_VAL)
    dot_leftover.setInput(0, copy_extra)

    if choosen_type == "material" or choosen_type == "full_setup":
        if texture_group:
            ### START OF MERGE DIVIDE / MULTIPLY SECTION ON EXTRA PIPE ###

            # creating dot_albedo
            dot_albedo = nuke.nodes.Dot()
            dot_albedo['xpos'].setValue(int(dot_up_corner['xpos'].value()) - X_DIST)
            dot_albedo['ypos'].setValue(int(dot_up_corner['ypos'].value()))
            dot_albedo.setSelected(SELECT_VAL)
            dot_albedo.setInput(0, dot_up_corner)

            # creating albedo_shuffle
            albedo_shuffle = nuke.nodes.Shuffle2()
            albedo_shuffle['in1'].setValue(texture_group[0])
            albedo_shuffle['label'].setValue("<b>albedo")
            albedo_shuffle['note_font_size'].setValue(25)
            set_center_x(albedo_shuffle, dot_albedo)
            albedo_shuffle['ypos'].setValue(int(dot_albedo['ypos'].value()) + 100)
            albedo_shuffle.setSelected(SELECT_VAL)
            albedo_shuffle.setInput(0, dot_albedo)
            print(albedo_shuffle.name())

            # creating dot_divide_extra
            dot_divide_extra = nuke.nodes.Dot()
            dot_divide_extra['xpos'].setValue(int(dot_albedo['xpos'].value()))
            dot_divide_extra['ypos'].setValue(int(dot_leftover['ypos'].value()) + 200)
            dot_divide_extra.setSelected(SELECT_VAL)
            old_dot_divide.setInput(0, dot_divide_extra)
            dot_divide_extra.setInput(0, albedo_shuffle)

            # creating merge_divide_extra
            merge_divide_extra = nuke.nodes.MergeExpression()
            merge_divide_extra['xpos'].setValue(int(merge_divide['xpos'].value()) - X_DIST)
            merge_divide_extra['ypos'].setValue(int(merge_divide['ypos'].value()) + 200)
            merge_divide_extra['expr0'].setValue('Ar>0?Br>0?Br/Ar:0:0')
            merge_divide_extra['expr1'].setValue('Ag>0?Bg>0?Bg/Ag:0:0')
            merge_divide_extra['expr2'].setValue('Ab>0?Bb>0?Bb/Ab:0:0')
            merge_divide_extra.setSelected(SELECT_VAL)
            merge_divide_extra.setInput(0, dot_leftover)
            merge_divide_extra.setInput(1, dot_divide_extra)

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

    # creating dot_leftover2
    dot_leftover2 = nuke.nodes.Dot()
    dot_leftover2['xpos'].setValue(int(dot_up_corner['xpos'].value()))
    dot_leftover2['ypos'].setValue(int(dotgrade2['ypos'].value()))
    dot_leftover2['label'].setValue("  <h1>&nbsp;&nbsp;Left_Over</h1>")
    dot_leftover2['note_font_size'].setValue(DOT_GRADE_FONT_SIZE)
    dot_leftover2.setSelected(SELECT_VAL)
    if choosen_type == "material" or choosen_type == "full_setup":
        if texture_group:
            dot_leftover2.setInput(0, merge_mult_extra)
    if not texture_group:
        dot_leftover2.setInput(0, dot_leftover)

    # creating dot_expr_side
    dot_expr_side = nuke.nodes.Dot()
    dot_expr_side['xpos'].setValue(int(dot_leftover2['xpos'].value()))
    dot_expr_side['ypos'].setValue(int(dot_expr['ypos'].value()) + int(Y_DIST))
    dot_expr_side.setSelected(SELECT_VAL)
    dot_expr_side.setInput(0, dot_leftover2)

    # creating merge_plus_side
    merge_plus_side = nuke.nodes.Merge2()
    merge_plus_side['operation'].setValue('plus')
    merge_plus_side['Achannels'].setValue('rgb')
    merge_plus_side['Bchannels'].setValue('rgb')
    merge_plus_side['output'].setValue('rgb')
    merge_plus_side['label'].setValue("Left_Over")
    merge_plus_side['xpos'].setValue(int(merge_plus['xpos'].value()))
    set_center_y(merge_plus_side,dot_expr_side)
    merge_plus_side.setSelected(SELECT_VAL)
    merge_plus_side.setInput(1, dot_expr_side)
    merge_plus_side.setInput(0, merge_plus_old)

    # creating dot_expr_side
    dot_bty_alpha = nuke.nodes.Dot()
    set_center_x(dot_bty_alpha,dotMain)
    dot_bty_alpha['ypos'].setValue(int(merge_plus_side['ypos'].value()) + Y_DIST)
    dot_bty_alpha.setSelected(SELECT_VAL)
    dot_bty_alpha.setInput(0, dotMain)

    # creating copy_bty_alpha
    copy_bty_alpha = nuke.nodes.Copy()
    copy_bty_alpha['from0'].setValue('alpha')
    copy_bty_alpha['to0'].setValue('alpha')
    copy_bty_alpha['xpos'].setValue(int(merge_plus_side['xpos'].value()))
    set_center_y(copy_bty_alpha,dot_bty_alpha)
    copy_bty_alpha.setSelected(SELECT_VAL)
    copy_bty_alpha.setInput(0, merge_plus_side)
    copy_bty_alpha.setInput(1, dot_bty_alpha)

    # creating dot_grade_bty
    dot_grade_bty = nuke.nodes.Dot()
    set_center_x(dot_grade_bty,copy_bty_alpha)
    dot_grade_bty['ypos'].setValue(int(copy_bty_alpha['ypos'].value()) + Y_DIST)
    dot_grade_bty['label'].setValue("  <h1>&nbsp;&nbsp;Beauty</h1>")
    dot_grade_bty['note_font_size'].setValue(DOT_GRADE_FONT_SIZE)
    dot_grade_bty.setSelected(SELECT_VAL)
    dot_grade_bty.setInput(0, copy_bty_alpha)

    # creating dot_grade_bty_2
    dot_grade_bty_2 = nuke.nodes.Dot()
    dot_grade_bty_2['xpos'].setValue(int(dot_grade_bty['xpos'].value()))
    if "C_direct" in choosen_group:
        dot_grade_bty_2['ypos'].setValue(int(dot_grade_bty['ypos'].value()) + (Y_DIST * 4)+GRADE_DIST)
    else:
        dot_grade_bty_2['ypos'].setValue(int(dot_grade_bty['ypos'].value()) + Y_DIST+GRADE_DIST)
    # dot_grade_bty_2['ypos'].setValue(int(dot_grade_bty['ypos'].value()) + GRADE_DIST)
    dot_grade_bty_2['label'].setValue("  <h1>&nbsp;&nbsp;<h1>Beauty</h1>")
    dot_grade_bty_2['note_font_size'].setValue(DOT_GRADE_FONT_SIZE)
    dot_grade_bty_2.setSelected(SELECT_VAL)
    dot_grade_bty_2.setInput(0, dot_grade_bty)

    # creating prem_all
    prem_all = nuke.nodes.Premult()
    prem_all['xpos'].setValue(int(merge_plus_side['xpos'].value()))
    prem_all['ypos'].setValue(int(dot_grade_bty_2['ypos'].value()) + Y_DIST)
    prem_all.setSelected(SELECT_VAL)
    prem_all.setInput(0, dot_grade_bty_2)

    # creating dot_corner
    dot_corner = nuke.nodes.Dot()
    dot_corner['xpos'].setValue(int(connect_dot['xpos'].value()))
    dot_corner['ypos'].setValue(int(prem_all['ypos'].value()) + Y_DIST)
    dot_corner.setSelected(SELECT_VAL)
    dot_corner.setInput(0, prem_all)

    # creating copy_rgb
    copy_rgb = nuke.nodes.Copy()
    copy_rgb['channels'].setValue('rgb')
    set_center_x(copy_rgb,dot_bty_alpha)
    set_center_y(copy_rgb,dot_corner)
    copy_rgb.setSelected(SELECT_VAL)
    copy_rgb.setInput(1, dot_corner)
    copy_rgb.setInput(0, dot_bty_alpha)

    bottom_right_corner = copy_rgb
    if choosen_group == "material":
        top_left_corner = dot_albedo
    else:
        top_left_corner = dot_up_corner

    return bottom_right_corner, top_left_corner

def lighting_setup(channel_layers):
    color_group, color_combined_group = get_color_layers(channel_layers)
    color_layers = color_combined_group + color_group

    if color_combined_group and color_group:
        ### TOP PART ###
        dotMain, middle_dot = top_part(channel_layers)

        ### FIRST LOOP ###
        choosen_group = color_group
        bottom_right_corner_first, top_left_corner_first = loop_part(choosen_group, dotMain, "lighting", None)

        ### PREMULT BETWEEN LOOPS ###
        premult_corner = nuke.nodes.Premult()
        premult_corner['xpos'].setValue(int(top_left_corner_first['xpos'].value()) - X_DIST)
        premult_corner['ypos'].setValue(int(top_left_corner_first['ypos'].value()))
        premult_corner.setSelected(SELECT_VAL)
        premult_corner.setInput(0, top_left_corner_first)

        ### SECOND LOOP ###
        choosen_group = color_combined_group
        bottom_right_corner_second, top_left_corner_second = loop_part(choosen_group, premult_corner, "lighting", None)
        # creating dot_divide_bty
        dot_divide_bty = nuke.nodes.Dot()
        dot_divide_bty['xpos'].setValue(int(middle_dot['xpos'].value()))
        dot_divide_bty['ypos'].setValue(int(bottom_right_corner_first['ypos'].value()) + (Y_DIST*2))
        dot_divide_bty.setSelected(SELECT_VAL)
        dot_divide_bty.setInput(0, middle_dot)

        # creating merge_divide_bty
        merge_divide_bty = nuke.nodes.MergeExpression()
        merge_divide_bty['xpos'].setValue(int(bottom_right_corner_first['xpos'].value()))
        set_center_y(merge_divide_bty,dot_divide_bty)
        merge_divide_bty['expr0'].setValue('Ar>0?Br>0?Br/Ar:0:0')
        merge_divide_bty['expr1'].setValue('Ag>0?Bg>0?Bg/Ag:0:0')
        merge_divide_bty['expr2'].setValue('Ab>0?Bb>0?Bb/Ab:0:0')
        merge_divide_bty.setSelected(SELECT_VAL)
        merge_divide_bty.setInput(0, bottom_right_corner_first)
        merge_divide_bty.setInput(1, dot_divide_bty)

        # creating dot_second_loop_corner
        dot_second_loop_corner = nuke.nodes.Dot()
        set_center_x(dot_second_loop_corner,bottom_right_corner_second)
        dot_second_loop_corner['ypos'].setValue(int(merge_divide_bty['ypos'].value()) + (Y_DIST * 2))
        dot_second_loop_corner.setSelected(SELECT_VAL)
        dot_second_loop_corner.setInput(0, bottom_right_corner_second)

        # creating merge_multiply_bty
        merge_multiply_bty = nuke.nodes.Merge2()
        merge_multiply_bty['xpos'].setValue(int(merge_divide_bty['xpos'].value()))
        set_center_y(merge_multiply_bty,dot_second_loop_corner)
        merge_multiply_bty['operation'].setValue('multiply')
        merge_multiply_bty['Achannels'].setValue('rgb')
        merge_multiply_bty['Bchannels'].setValue('rgb')
        merge_multiply_bty['output'].setValue('rgb')
        merge_multiply_bty.setSelected(SELECT_VAL)
        merge_multiply_bty.setInput(0, merge_divide_bty)
        merge_multiply_bty.setInput(1, dot_second_loop_corner)

        # creating dot_result
        dot_result = nuke.nodes.Dot()
        set_center_x(dot_result,merge_multiply_bty)
        dot_result['ypos'].setValue(int(merge_divide_bty['ypos'].value()) + (Y_DIST * 5))
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
        set_center_x(dot_result,bottom_right_corner)
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
        set_center_x(dot_result,bottom_right_corner)
        dot_result['ypos'].setValue(int(bottom_right_corner['ypos'].value()) + (Y_DIST * 4))
        dot_result.setSelected(SELECT_VAL)
        dot_result.setInput(0, bottom_right_corner)

    return dot_result, middle_dot

def material_setup(channel_layers, dotMain, middle_dot):
    material_group = get_material_layers(channel_layers)
    texture_group = get_texture_layer(channel_layers)

    ### LOOP PART ###
    bottom_right_corner, top_left_corner = loop_part(material_group, dotMain, "material", texture_group)
    # creating dot_result
    dot_result = nuke.nodes.Dot()
    set_center_x(dot_result,bottom_right_corner)
    dot_result['ypos'].setValue(int(bottom_right_corner['ypos'].value()) + (Y_DIST * 4))
    dot_result.setSelected(SELECT_VAL)
    dot_result.setInput(0, bottom_right_corner)

    return dot_result

def main(chosen_type):
    if not len(nuke.selectedNodes()) == 1:
        nuke.alert('<font color=orange><h3>Please, select a single node with AOVs!')
    else:
        channel_layers = get_layers()
        color_group, color_combined_group = get_color_layers(channel_layers)
        material_group = get_material_layers(channel_layers)

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
                    merge_divide_bty = nuke.nodes.MergeExpression()
                    set_center_x(merge_divide_bty,dot_result)
                    merge_divide_bty['ypos'].setValue(int(dot_divide_bty['ypos'].value()))
                    merge_divide_bty['expr0'].setValue('Ar>0?Br>0?Br/Ar:0:0')
                    merge_divide_bty['expr1'].setValue('Ag>0?Bg>0?Bg/Ag:0:0')
                    merge_divide_bty['expr2'].setValue('Ab>0?Bb>0?Bb/Ab:0:0')
                    merge_divide_bty.setSelected(SELECT_VAL)
                    merge_divide_bty.setInput(0, dot_result)
                    merge_divide_bty.setInput(1, dot_divide_bty)

                    # creating dot_material_corner
                    dot_material_corner = nuke.nodes.Dot()
                    dot_material_corner['xpos'].setValue(int(dot_divide_bty['xpos'].value()))
                    dot_material_corner['ypos'].setValue(int(dot_divide_bty['ypos'].value()) + (Y_DIST * 2))
                    dot_material_corner.setSelected(SELECT_VAL)
                    dot_material_corner.setInput(0, dot_divide_bty)

                    # creating dot_material_start
                    dot_material_start = nuke.nodes.Dot()
                    dot_material_start['xpos'].setValue(int(dot_divide_bty['xpos'].value()) - (X_DIST))
                    dot_material_start['ypos'].setValue(int(dot_material_corner['ypos'].value()))
                    dot_material_start.setSelected(SELECT_VAL)
                    dot_material_start.setInput(0, dot_material_corner)

                    ### MATERIAL PART ###
                    dot_result = material_setup(channel_layers, dot_material_start, dot_material_corner)

                    ### CONNECTING PART ###
                    # creating merge_multiply_bty
                    merge_multiply_bty = nuke.nodes.Merge2()
                    merge_multiply_bty['xpos'].setValue(int(merge_divide_bty['xpos'].value()))
                    set_center_y(merge_multiply_bty,dot_result)
                    merge_multiply_bty['operation'].setValue('multiply')
                    merge_multiply_bty['Achannels'].setValue('rgb')
                    merge_multiply_bty['Bchannels'].setValue('rgb')
                    merge_multiply_bty['output'].setValue('rgb')
                    merge_multiply_bty.setSelected(SELECT_VAL)
                    merge_multiply_bty.setInput(0, merge_divide_bty)
                    merge_multiply_bty.setInput(1, dot_result)

                    # creating dot_result
                    dot_result = nuke.nodes.Dot()
                    set_center_x(dot_result,merge_multiply_bty)
                    dot_result['ypos'].setValue(int(merge_multiply_bty['ypos'].value()) + (Y_DIST * 4))
                    dot_result.setSelected(SELECT_VAL)
                    dot_result.setInput(0, merge_multiply_bty)
