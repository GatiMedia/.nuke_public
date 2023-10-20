import nuke

MATERIAL_LAYER_PREFIX = 'M_'
X_DIST = 1000
Y_DIST = 200
GRADE_DIST = 2500
SELECT_VAL = True

def materialLayerSetup():
    nodes = nuke.selectedNodes()
    if not len(nodes) == 1:
        nuke.alert('<font color=orange><h3>Please, select a single node first with material passes!')
    else:
        curSel = nuke.selectedNode()
        curSelChannels = curSel.channels()
        layersList = []
        for rawChannels in curSelChannels:
            splitRawChannels = rawChannels.split('.')
            layersList.append(splitRawChannels[0])
        channelLayers = list(set(layersList))
        channelLayers.sort()
        colorGroup = []
        for c in channelLayers:
            if c.startswith(MATERIAL_LAYER_PREFIX):
                colorGroup.append(c)
            else:
                continue
        noteVal = '' + '\n'.join(channelLayers)

        if "M_specular_direct" in colorGroup:
            colorGroup.remove("M_specular")
        if "M_diffuse_direct" in colorGroup:
            colorGroup.remove("M_diffuse")

        if not colorGroup:
            nuke.alert('<font color=orange><h3><center>No color passes found!\n\nAvailable layers are:\n\n<font color=yellow><h4>' + ',\n'.join(channelLayers))
        else:
            # create dotMain
            dotMain = nuke.nodes.Dot()
            dotMain['xpos'].setValue(int(curSel['xpos'].value()) + (curSel.screenWidth() / 2) - (dotMain.screenWidth() / 2))
            dotMain['ypos'].setValue(int(curSel['ypos'].value()) + 300)
            dotMain.setSelected(SELECT_VAL)
            dotMain.setInput(0, curSel)

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

            for index, n in enumerate(colorGroup):
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
                mergeFrom['xpos'].setValue(int(curSel['xpos'].value()) - (len(colorGroup) + 2) * X_DIST)
                mergeFrom['ypos'].setValue(int(dotshuf['ypos'].value()) - (mergeFrom.screenHeight() / 2))
                mergeFrom['operation'].setValue('from')
                mergeFrom['label'].setValue(n)
                mergeFrom.setSelected(SELECT_VAL)
                mergeFrom.setInput(1, dotshuf)
                if mergeFrom:
                    mergeFrom.setInput(0, mergeFromold)
                if index == 0:
                    mergefirst = mergeFrom

                if index + 1 == len(colorGroup):
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
                dotgrade['ypos'].setValue(int(dot['ypos'].value()) + int((len(colorGroup) + 2) * Y_DIST) + 250)
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

                ### START OF MERGE DIVIDE / MULTIPLY SECTION ON MAIN PIPE

                # creating dot_divide
                dot_divide = nuke.nodes.Dot()
                dot_divide['xpos'].setValue(int(dotgrade['xpos'].value())-120)
                dot_divide['ypos'].setValue(int(unprem['ypos'].value()) + 100)
                dot_divide.setSelected(SELECT_VAL)
                if index == 0:
                    old_dot_divide = dot_divide
                else:
                    old_dot_divide.setInput(0, dot_divide)
                    old_dot_divide = dot_divide

                # creating merge_divide
                merge_divide= nuke.nodes.Merge2()
                merge_divide['xpos'].setValue(int(unprem['xpos'].value()))
                merge_divide['ypos'].setValue(int(unprem['ypos'].value())+200)
                merge_divide['operation'].setValue('divide')
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
                merge_mult= nuke.nodes.Merge2()
                merge_mult['xpos'].setValue(int(merge_divide['xpos'].value()))
                merge_mult['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST - 200)
                merge_mult['operation'].setValue('multiply')
                merge_mult.setSelected(SELECT_VAL)
                merge_mult.setInput(0, merge_divide)
                merge_mult.setInput(1, old_dot_multiply)

                ### END OF MERGE DIVIDE / MULTIPLY SECTION ON MAIN PIPE

                # creating prem
                prem = nuke.nodes.Premult()
                prem['xpos'].setValue(int(shuffle['xpos'].value()))
                prem['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST - 100)
                prem.setSelected(SELECT_VAL)
                prem.setInput(0, merge_mult)

                # creating dotgrade2
                dotgrade2 = nuke.nodes.Dot()
                dotgrade2['xpos'].setValue(int(dotgrade['xpos'].value()))
                dotgrade2['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST)
                dotgrade2['label'].setValue("  <h1>" + n + "</h1>")
                dotgrade2['note_font_size'].setValue(30)
                dotgrade2.setSelected(SELECT_VAL)
                dotgrade2.setInput(0, prem)

                # creating expAlpha
                expAlpha = nuke.nodes.Expression()
                expAlpha['channel0'].setValue('alpha')
                expAlpha['expr0'].setValue('clamp(r+g+b)')
                expAlpha['xpos'].setValue(int(shuffle['xpos'].value()))
                expAlpha['ypos'].setValue(int(dotgrade2['ypos'].value()) + 200)
                expAlpha.setSelected(SELECT_VAL)
                expAlpha.setInput(0, dotgrade2)

                # creating dotExpr
                dotExpr = nuke.nodes.Dot()
                dotExpr['xpos'].setValue(int(dotgrade['xpos'].value()))
                dotExpr['ypos'].setValue(int(expAlpha['ypos'].value()) + int(index * Y_DIST) + 250)
                dotExpr.setSelected(SELECT_VAL)
                dotExpr.setInput(0, expAlpha)

                # creating mergePlus
                mergePlus = nuke.nodes.Merge2()
                mergePlus['xpos'].setValue(int(removeN['xpos'].value()))
                mergePlus['ypos'].setValue(int(dotExpr['ypos'].value()))
                mergePlus['operation'].setValue('plus')
                mergePlus['label'].setValue(n)
                mergePlus.setSelected(SELECT_VAL)
                mergePlus.setInput(1, dotExpr)
                if mergePlusOld:
                    mergePlus.setInput(0, mergePlusOld)
                else:
                    mergePlus.setInput(0, removeN)
                mergePlusOld = mergePlus

            # # creating shuffleExtra
            # shuffle = nuke.nodes.Shuffle2()
            # shuffle['in1'].setValue('rgba')
            # shuffle['out1'].setValue('M_Extra_Material')
            # shuffle['label'].setValue("<b>[value in1] -> [value out1]")
            # shuffle['note_font_size'].setValue(25)
            # shuffle['xpos'].setValue(int(mergeFrom['xpos'].value()))
            # shuffle['ypos'].setValue(int(mergeFrom['ypos'].value()) + 100)
            # shuffle.setSelected(SELECT_VAL)
            # shuffle.setInput(0, mergeFrom)
            #
            # # creating shuffleExtraRGB
            # shuffleExtraRGB = nuke.nodes.Shuffle2()
            # shuffleExtraRGB['in1'].setValue('M_Extra_Material')
            # shuffleExtraRGB['out1'].setValue('rgba')
            # shuffleExtraRGB['label'].setValue("<b>[value in1] -> [value out1]")
            # shuffleExtraRGB['note_font_size'].setValue(25)
            # shuffleExtraRGB['xpos'].setValue(int(mergeFrom['xpos'].value()))
            # shuffleExtraRGB['ypos'].setValue(int(shuffle['ypos'].value()) + 100)
            # shuffleExtraRGB.setSelected(SELECT_VAL)
            # shuffleExtraRGB.setInput(0, shuffle)

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

            #creating dot_leftover
            dot_leftover = nuke.nodes.Dot()
            dot_leftover['xpos'].setValue(int(dotUpCorner['xpos'].value()))
            dot_leftover['ypos'].setValue(int(dotgrade['ypos'].value()))
            dot_leftover['label'].setValue("  <h1>M_Left_Over</h1>")
            dot_leftover['note_font_size'].setValue(30)
            dot_leftover.setSelected(SELECT_VAL)
            dot_leftover.setInput(0, clamp)

            # creating unprem_extra
            unprem_extra = nuke.nodes.Unpremult()
            unprem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
            unprem_extra['ypos'].setValue(int(unprem['ypos'].value()))
            unprem_extra.setSelected(SELECT_VAL)
            unprem_extra.setInput(0, dot_leftover)

            ### START OF MERGE DIVIDE / MULTIPLY SECTION ON EXTRA PIPE

            # creating dot_albedo
            dot_albedo = nuke.nodes.Dot()
            dot_albedo['xpos'].setValue(int(dotUpCorner['xpos'].value()) - X_DIST)
            dot_albedo['ypos'].setValue(int(dotUpCorner['ypos'].value()))
            dot_albedo.setSelected(SELECT_VAL)
            dot_albedo.setInput(0, dotUpCorner)

            # creating albedo_shuffle
            albedo_shuffle = nuke.nodes.Shuffle2()
            albedo_shuffle['in1'].setValue('T_albedo')
            albedo_shuffle['label'].setValue("<b>T_albedo")
            albedo_shuffle['note_font_size'].setValue(25)
            albedo_shuffle['xpos'].setValue(int(dot_albedo['xpos'].value()) - (albedo_shuffle.screenWidth() / 2) + (dot_albedo.screenWidth() / 2))
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
            merge_mult_extra.setSelected(SELECT_VAL)
            merge_mult_extra.setInput(0, merge_divide_extra)
            merge_mult_extra.setInput(1, dot_multiply_extra)

            ### END OF MERGE DIVIDE / MULTIPLY SECTION ON EXTRA PIPE

            # creating prem
            prem_extra = nuke.nodes.Premult()
            prem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
            prem_extra['ypos'].setValue(int(prem['ypos'].value()))
            prem_extra.setSelected(SELECT_VAL)
            prem_extra.setInput(0, merge_mult_extra)

            #creating dot_leftover2
            dot_leftover2 = nuke.nodes.Dot()
            dot_leftover2['xpos'].setValue(int(dotUpCorner['xpos'].value()))
            dot_leftover2['ypos'].setValue(int(dotgrade2['ypos'].value()))
            dot_leftover2['label'].setValue("  <h1>M_Left_Over</h1>")
            dot_leftover2['note_font_size'].setValue(30)
            dot_leftover2.setSelected(SELECT_VAL)
            dot_leftover2.setInput(0, prem_extra)

            # creating expAlphaSide
            expAlphaSide = nuke.nodes.Expression()
            expAlphaSide['channel0'].setValue('alpha')
            expAlphaSide['expr0'].setValue('clamp(r+g+b)')
            expAlphaSide['xpos'].setValue(int(prem_extra['xpos'].value()))
            expAlphaSide['ypos'].setValue(int(expAlpha['ypos'].value()))
            expAlphaSide.setSelected(SELECT_VAL)
            expAlphaSide.setInput(0, dot_leftover2)

            # creating dotExprSide
            dotExprSide = nuke.nodes.Dot()
            dotExprSide['xpos'].setValue(int(dot_leftover2['xpos'].value()))
            dotExprSide['ypos'].setValue(int(dotExpr['ypos'].value()) + int(Y_DIST))
            dotExprSide.setSelected(SELECT_VAL)
            dotExprSide.setInput(0, expAlphaSide)

            # creating mergePlusSide
            mergePlusSide = nuke.nodes.Merge2()
            mergePlusSide['xpos'].setValue(int(mergePlus['xpos'].value()))
            mergePlusSide['ypos'].setValue(int(dotExprSide['ypos'].value()))
            mergePlusSide['operation'].setValue('plus')
            mergePlusSide['label'].setValue('M_Left_Over')
            mergePlusSide.setSelected(SELECT_VAL)
            mergePlusSide.setInput(1, dotExprSide)
            mergePlusSide.setInput(0, mergePlusOld)

            # creating dotMsg
            # TODO - add NAN_INF_KILLER _ nuke.createNode('NST_NAN_INF_Killer') - causing connection problems
            dotMsg = nuke.nodes.Dot()
            dotMsg['xpos'].setValue(int(connectDot['xpos'].value()))
            dotMsg['ypos'].setValue(int(mergePlusSide['ypos'].value()) + (Y_DIST * 8))
            dotMsg['label'].setValue(' Add a <b>NAN_INF_Killer</b> node here!')
            dotMsg['note_font_size'].setValue(32)
            dotMsg.setSelected(SELECT_VAL)
            dotMsg.setInput(0, mergePlusSide)

            # creating dotCorner
            dotCorner = nuke.nodes.Dot()
            dotCorner['xpos'].setValue(int(connectDot['xpos'].value()))
            dotCorner['ypos'].setValue(int(dotMsg['ypos'].value()) + Y_DIST)
            dotCorner.setSelected(SELECT_VAL)
            dotCorner.setInput(0, dotMsg)

            # creating copyNode
            copyNode = nuke.nodes.Copy()
            copyNode['xpos'].setValue(int(curSel['xpos'].value()))
            copyNode['ypos'].setValue(int(dotCorner['ypos'].value()))
            copyNode['channels'].setValue('rgb')
            copyNode.setSelected(SELECT_VAL)
            copyNode.setInput(1, dotCorner)
            copyNode.setInput(0, dotMain)

            # creating layerContact
            layerContact = nuke.nodes.LayerContactSheet()
            layerContact['xpos'].setValue(int(dotMain['xpos'].value()) + 400)
            layerContact['ypos'].setValue(int(dotMain['ypos'].value()))
            layerContact['showLayerNames'].setValue(True)
            layerContact.setSelected(SELECT_VAL)
            layerContact.setInput(0, dotMain)

            # creating stickyNote
            stickyNote = nuke.nodes.StickyNote()
            stickyNote['xpos'].setValue(int(layerContact['xpos'].value()) - 40)
            stickyNote['ypos'].setValue(int(layerContact['ypos'].value()) + 200)
            stickyNote['label'].setValue("<h2><center>Available layers:\n\n" + noteVal + "\n\n")
            stickyNote.setSelected(SELECT_VAL)
