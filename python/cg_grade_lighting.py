# --------------------------------------------------------------
#  cg_grade_lighting.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 29/11/2023
# --------------------------------------------------------------
# This tool is based on an AOV naming customization where Color (Lighting), Material and Texture groups gets prefixes, respectively "C_", "M_" and "T_"

import nuke

COLOR_LAYER_PREFIX = 'C_'
X_DIST = 1000
Y_DIST = 200
GRADE_DIST = 2500
SELECT_VAL = True

def colorLayerSetup():
    nodes = nuke.selectedNodes()
    if not len(nodes) == 1:
        nuke.alert('<font color=orange><h3>Please, select a single node first with color passes!')
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
            if c.startswith(COLOR_LAYER_PREFIX):
                colorGroup.append(c)
            else:
                continue
        noteVal = '' + '\n'.join(channelLayers)

        color_new_group = []
        if 'C_direct' in colorGroup:
            colorGroup.remove('C_direct')
            colorGroup.remove('C_indirect')
            color_new_group.append('C_direct')
            color_new_group.append('C_indirect')

        if not colorGroup:
            nuke.alert('<font color=orange><h3><center>No color passes found!\n\nAvailable layers are:\n\n<font color=yellow><h4>' + ',\n'.join(channelLayers))
        else:
            # create dotMain
            dotMain = nuke.nodes.Dot()
            dotMain['xpos'].setValue(int(curSel['xpos'].value()) + (curSel.screenWidth() / 2) - (dotMain.screenWidth() / 2))
            dotMain['ypos'].setValue(int(curSel['ypos'].value()) + 300)
            dotMain.setSelected(SELECT_VAL)
            dotMain.setInput(0, curSel)

            ######################################################
            ############## RIGHT SIDE MAIN PIPES #################
            ######################################################

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

                # creating prem
                prem = nuke.nodes.Premult()
                prem['xpos'].setValue(int(shuffle['xpos'].value()))
                prem['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST - 100)
                prem.setSelected(SELECT_VAL)
                prem.setInput(0, unprem)

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

            ######################################################
            ############## RIGHT SIDE EXTRA SECTION ##############
            ######################################################

            # creating shuffleExtra
            shuffle = nuke.nodes.Shuffle2()
            shuffle['in1'].setValue('rgba')
            shuffle['out1'].setValue('C_Extra_Light')
            shuffle['label'].setValue("<b>[value in1] -> [value out1]")
            shuffle['note_font_size'].setValue(25)
            shuffle['xpos'].setValue(int(mergeFrom['xpos'].value()))
            shuffle['ypos'].setValue(int(mergeFrom['ypos'].value()) + 100)
            shuffle.setSelected(SELECT_VAL)
            shuffle.setInput(0, mergeFrom)

            # creating shuffleExtraRGB
            shuffleExtraRGB = nuke.nodes.Shuffle2()
            shuffleExtraRGB['in1'].setValue('C_Extra_Light')
            shuffleExtraRGB['out1'].setValue('rgba')
            shuffleExtraRGB['label'].setValue("<b>[value in1] -> [value out1]")
            shuffleExtraRGB['note_font_size'].setValue(25)
            shuffleExtraRGB['xpos'].setValue(int(mergeFrom['xpos'].value()))
            shuffleExtraRGB['ypos'].setValue(int(shuffle['ypos'].value()) + 100)
            shuffleExtraRGB.setSelected(SELECT_VAL)
            shuffleExtraRGB.setInput(0, shuffle)

            # creating copy_extra
            copy_extra = nuke.nodes.Copy()
            copy_extra['from0'].setValue('alpha')
            copy_extra['to0'].setValue('alpha')
            copy_extra['xpos'].setValue(int(shuffleExtraRGB['xpos'].value()))
            copy_extra['ypos'].setValue(int(shuffleExtraRGB['ypos'].value()) + 150)
            copy_extra.setSelected(SELECT_VAL)
            copy_extra.setInput(0, shuffleExtraRGB)
            copy_extra.setInput(1, dotUpCorner)

            # creating dot_leftover
            dot_leftover = nuke.nodes.Dot()
            dot_leftover['xpos'].setValue(int(dotUpCorner['xpos'].value()))
            dot_leftover['ypos'].setValue(int(dotgrade['ypos'].value()))
            dot_leftover['label'].setValue("  <h1>C_Left_Over</h1>")
            dot_leftover['note_font_size'].setValue(30)
            dot_leftover.setSelected(SELECT_VAL)
            dot_leftover.setInput(0, copy_extra)

            # creating unprem_extra
            unprem_extra = nuke.nodes.Unpremult()
            unprem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
            unprem_extra['ypos'].setValue(int(unprem['ypos'].value()))
            unprem_extra.setSelected(SELECT_VAL)
            unprem_extra.setInput(0, dot_leftover)

            # creating prem
            prem_extra = nuke.nodes.Premult()
            prem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
            prem_extra['ypos'].setValue(int(prem['ypos'].value()))
            prem_extra.setSelected(SELECT_VAL)
            prem_extra.setInput(0, unprem_extra)

            # creating dot_leftover2
            dot_leftover2 = nuke.nodes.Dot()
            dot_leftover2['xpos'].setValue(int(dotUpCorner['xpos'].value()))
            dot_leftover2['ypos'].setValue(int(dotgrade2['ypos'].value()))
            dot_leftover2['label'].setValue("  <h1>C_Left_Over</h1>")
            dot_leftover2['note_font_size'].setValue(30)
            dot_leftover2.setSelected(SELECT_VAL)
            dot_leftover2.setInput(0, prem_extra)

            # creating expAlphaSide
            expAlphaSide = nuke.nodes.Expression()
            expAlphaSide['channel0'].setValue('alpha')
            expAlphaSide['expr0'].setValue('clamp(r+g+b)')
            expAlphaSide['xpos'].setValue(int(shuffle['xpos'].value()))
            expAlphaSide['ypos'].setValue(int(expAlpha['ypos'].value()))
            expAlphaSide.setSelected(SELECT_VAL)
            expAlphaSide.setInput(0, dot_leftover2)

            # creating dotExprSide
            dotExprSide = nuke.nodes.Dot()
            dotExprSide['xpos'].setValue(int(expAlphaSide['xpos'].value()) + 36)
            dotExprSide['ypos'].setValue(int(dotExpr['ypos'].value()) + int(Y_DIST))
            dotExprSide.setSelected(SELECT_VAL)
            dotExprSide.setInput(0, expAlphaSide)

            # creating mergePlusSide
            mergePlusSide = nuke.nodes.Merge2()
            mergePlusSide['xpos'].setValue(int(mergePlus['xpos'].value()))
            mergePlusSide['ypos'].setValue(int(dotExprSide['ypos'].value()))
            mergePlusSide['operation'].setValue('plus')
            mergePlusSide['Achannels'].setValue('rgb')
            mergePlusSide['Bchannels'].setValue('rgb')
            mergePlusSide['output'].setValue('rgb')
            mergePlusSide['label'].setValue('C_Left_Over')
            mergePlusSide.setSelected(SELECT_VAL)
            mergePlusSide.setInput(1, dotExprSide)
            mergePlusSide.setInput(0, mergePlusOld)

            # creating dotCorner
            dotCorner = nuke.nodes.Dot()
            dotCorner['xpos'].setValue(int(connectDot['xpos'].value()))
            dotCorner['ypos'].setValue(int(mergePlusSide['ypos'].value()) + (Y_DIST * 8))
            dotCorner.setSelected(SELECT_VAL)
            dotCorner.setInput(0, mergePlusSide)

            # creating copyNode
            copyNode = nuke.nodes.Copy()
            copyNode['xpos'].setValue(int(curSel['xpos'].value()))
            copyNode['ypos'].setValue(int(dotCorner['ypos'].value()) + (shuffle.screenHeight() / 2) - (newDot.screenHeight() / 2))
            copyNode['channels'].setValue('rgb')
            copyNode.setSelected(SELECT_VAL)
            copyNode.setInput(1, dotCorner)
            copyNode.setInput(0, dotMain)

            ######################################################
            ############## LEFT SIDE MAIN PIPES ##################
            ######################################################


            # creating dotColorDivide
            dotColorDivide = dot = nuke.nodes.Dot()
            dotColorDivide['xpos'].setValue(int(dotUpCorner['xpos'].value()) - X_DIST)
            dotColorDivide['ypos'].setValue(int(dotUpCorner['ypos'].value()))
            dotColorDivide.setSelected(SELECT_VAL)
            dotColorDivide.setInput(0, dotUpCorner)


            # create removeN
            removeN = nuke.nodes.Remove()
            removeN['operation'].setValue('remove')
            removeN['channels'].setValue('all')
            removeN['xpos'].setValue(int(dotColorDivide['xpos'].value()) - 36)
            removeN['ypos'].setValue(int(dotColorDivide['ypos'].value()) + 200)
            removeN.setSelected(SELECT_VAL)
            removeN.setInput(0, dotColorDivide)

            mergeFromold = None
            mergePlusOld = None

            for index, n in enumerate(color_new_group):
                # creating dot
                newX = dot['xpos'].value()
                newY = dot['ypos'].value()
                oldDot = dot
                dot = nuke.nodes.Dot()
                dot['xpos'].setValue(int(newX) - X_DIST)
                dot['ypos'].setValue(newY)
                dot.setSelected(SELECT_VAL)
                newDot = dot
                if index == 0:
                    newDot.setInput(0, dotColorDivide)
                else:
                    newDot.setInput(0, oldDot)

                # creating shuffle
                shuffle = nuke.nodes.Shuffle2()
                shuffle['in1'].setValue(n)
                shuffle['label'].setValue("<b>" + n)
                shuffle['note_font_size'].setValue(25)
                shuffle['xpos'].setValue(int(newDot['xpos'].value()) - (shuffle.screenWidth() / 2) + (newDot.screenWidth() / 2))
                shuffle['ypos'].setValue(int(newDot['ypos'].value()) + 100)
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
                dotshuf['xpos'].setValue(int(shuffle['xpos'].value()) - (dotshuf.screenWidth() / 2) + (shuffle.screenWidth() / 2))
                dotshuf['ypos'].setValue(int(newDot['ypos'].value()) + int(index * Y_DIST) + 350)
                dotshuf.setSelected(SELECT_VAL)
                dotshuf.setInput(0, copy)

                # creating mergeFrom
                mergeFrom = nuke.nodes.Merge2()
                mergeFrom['xpos'].setValue(int(copy['xpos'].value()) - X_DIST)
                mergeFrom['ypos'].setValue(int(dotshuf['ypos'].value()) + (mergeFrom.screenHeight() / 2) - (dotshuf.screenHeight() / 2))
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

                if index + 1 == len(colorGroup):
                    # creating dotUpCorner
                    dotUpCorner = nuke.nodes.Dot()
                    dotUpCorner['xpos'].setValue(int(mergeFrom['xpos'].value()) + 36)
                    dotUpCorner['ypos'].setValue(int(newDot['ypos'].value()))
                    dotUpCorner.setSelected(SELECT_VAL)
                    dotUpCorner.setInput(0, newDot)

                    mergefirst.setInput(0, dotUpCorner)
                    mergefirst['xpos'].setValue(int(copy['xpos'].value()) - X_DIST)

                mergeFromold = mergeFrom

                # creating dotgrade
                dotgrade = nuke.nodes.Dot()
                dotgrade['xpos'].setValue(int(dotshuf['xpos'].value()))
                dotgrade['ypos'].setValue(int(dot['ypos'].value()) + int((len(color_new_group) + 2) * Y_DIST) + 250)
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

                # creating prem
                prem = nuke.nodes.Premult()
                prem['xpos'].setValue(int(shuffle['xpos'].value()))
                prem['ypos'].setValue(int(dotgrade['ypos'].value()) + GRADE_DIST - 100)
                prem.setSelected(SELECT_VAL)
                prem.setInput(0, unprem)

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
                mergePlus['ypos'].setValue(int(dotExpr['ypos'].value()) + (mergePlus.screenHeight() / 2) - (dotExpr.screenHeight() / 2))
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

            ######################################################
            ############## LEFT SIDE EXTRA SECTION ###############
            ######################################################

            # creating shuffleExtra
            shuffle = nuke.nodes.Shuffle2()
            shuffle['in1'].setValue('rgba')
            shuffle['out1'].setValue('C_Extra_Light')
            shuffle['label'].setValue("<b>[value in1] -> [value out1]")
            shuffle['note_font_size'].setValue(25)
            shuffle['xpos'].setValue(int(mergeFrom['xpos'].value()))
            shuffle['ypos'].setValue(int(mergeFrom['ypos'].value()) + 100)
            shuffle.setSelected(SELECT_VAL)
            shuffle.setInput(0, mergeFrom)

            # creating shuffleExtraRGB
            shuffleExtraRGB = nuke.nodes.Shuffle2()
            shuffleExtraRGB['in1'].setValue('C_Extra_Light')
            shuffleExtraRGB['out1'].setValue('rgba')
            shuffleExtraRGB['label'].setValue("<b>[value in1] -> [value out1]")
            shuffleExtraRGB['note_font_size'].setValue(25)
            shuffleExtraRGB['xpos'].setValue(int(mergeFrom['xpos'].value()))
            shuffleExtraRGB['ypos'].setValue(int(shuffle['ypos'].value()) + 100)
            shuffleExtraRGB.setSelected(SELECT_VAL)
            shuffleExtraRGB.setInput(0, shuffle)

            # creating copy_extra
            copy_extra = nuke.nodes.Copy()
            copy_extra['from0'].setValue('alpha')
            copy_extra['to0'].setValue('alpha')
            copy_extra['xpos'].setValue(int(shuffleExtraRGB['xpos'].value()))
            copy_extra['ypos'].setValue(int(shuffleExtraRGB['ypos'].value()) + 150)
            copy_extra.setSelected(SELECT_VAL)
            copy_extra.setInput(0, shuffleExtraRGB)
            copy_extra.setInput(1, dotUpCorner)

            # creating dot_leftover
            dot_leftover = nuke.nodes.Dot()
            dot_leftover['xpos'].setValue(int(dotUpCorner['xpos'].value()))
            dot_leftover['ypos'].setValue(int(dotgrade['ypos'].value()))
            dot_leftover['label'].setValue("  <h1>C_Left_Over</h1>")
            dot_leftover['note_font_size'].setValue(30)
            dot_leftover.setSelected(SELECT_VAL)
            dot_leftover.setInput(0, copy_extra)

            # creating unprem_extra
            unprem_extra = nuke.nodes.Unpremult()
            unprem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
            unprem_extra['ypos'].setValue(int(unprem['ypos'].value()))
            unprem_extra.setSelected(SELECT_VAL)
            unprem_extra.setInput(0, dot_leftover)

            # creating prem
            prem_extra = nuke.nodes.Premult()
            prem_extra['xpos'].setValue(int(copy_extra['xpos'].value()))
            prem_extra['ypos'].setValue(int(prem['ypos'].value()))
            prem_extra.setSelected(SELECT_VAL)
            prem_extra.setInput(0, unprem_extra)

            # creating dot_leftover2
            dot_leftover2 = nuke.nodes.Dot()
            dot_leftover2['xpos'].setValue(int(dotUpCorner['xpos'].value()))
            dot_leftover2['ypos'].setValue(int(dotgrade2['ypos'].value()))
            dot_leftover2['label'].setValue("  <h1>C_Left_Over</h1>")
            dot_leftover2['note_font_size'].setValue(30)
            dot_leftover2.setSelected(SELECT_VAL)
            dot_leftover2.setInput(0, prem_extra)

            # creating expAlphaSide
            expAlphaSide = nuke.nodes.Expression()
            expAlphaSide['channel0'].setValue('alpha')
            expAlphaSide['expr0'].setValue('clamp(r+g+b)')
            expAlphaSide['xpos'].setValue(int(shuffle['xpos'].value()))
            expAlphaSide['ypos'].setValue(int(expAlpha['ypos'].value()))
            expAlphaSide.setSelected(SELECT_VAL)
            expAlphaSide.setInput(0, dot_leftover2)

            # creating dotExprSide
            dotExprSide = nuke.nodes.Dot()
            dotExprSide['xpos'].setValue(int(expAlphaSide['xpos'].value()) + 36)
            dotExprSide['ypos'].setValue(int(dotExpr['ypos'].value()) + int(Y_DIST))
            dotExprSide.setSelected(SELECT_VAL)
            dotExprSide.setInput(0, expAlphaSide)

            # creating mergePlusSide
            mergePlusSide = nuke.nodes.Merge2()
            mergePlusSide['xpos'].setValue(int(mergePlus['xpos'].value()))
            mergePlusSide['ypos'].setValue(int(dotExprSide['ypos'].value()) + (mergePlusSide.screenHeight() / 2) - (dotExprSide.screenHeight() / 2))
            mergePlusSide['operation'].setValue('plus')
            mergePlusSide['Achannels'].setValue('rgb')
            mergePlusSide['Bchannels'].setValue('rgb')
            mergePlusSide['output'].setValue('rgb')
            mergePlusSide['label'].setValue('C_Left_Over')
            mergePlusSide.setSelected(SELECT_VAL)
            mergePlusSide.setInput(1, dotExprSide)
            mergePlusSide.setInput(0, mergePlusOld)

            # creating dotCorner
            dotCorner = nuke.nodes.Dot()
            dotCorner['xpos'].setValue(int(dotColorDivide['xpos'].value()))
            dotCorner['ypos'].setValue(int(mergePlusSide['ypos'].value()) + (Y_DIST * 16))
            dotCorner.setSelected(SELECT_VAL)
            dotCorner.setInput(0, mergePlusSide)


            ######################################################
            ############## CONNECT ALL SECTION ###################
            ######################################################

            # creating middle_dot
            middle_dot = nuke.nodes.Dot()
            middle_dot['xpos'].setValue(int(dotMain['xpos'].value()) + 200)
            middle_dot['ypos'].setValue(int(dotMain['ypos'].value()))
            middle_dot.setSelected(SELECT_VAL)
            middle_dot.setInput(0, dotMain)

            # creating layerContact
            layerContact = nuke.nodes.LayerContactSheet()
            layerContact['xpos'].setValue(int(dotMain['xpos'].value()) + 400)
            layerContact['ypos'].setValue(int(dotMain['ypos'].value()))
            layerContact['showLayerNames'].setValue(True)
            layerContact.setSelected(SELECT_VAL)
            layerContact.setInput(0, middle_dot)

            # creating stickyNote
            stickyNote = nuke.nodes.StickyNote()
            stickyNote['xpos'].setValue(int(layerContact['xpos'].value()) - 40)
            stickyNote['ypos'].setValue(int(layerContact['ypos'].value()) + 200)
            stickyNote['label'].setValue("<h2><center>Available layers:\n\n" + noteVal + "\n\n")
            stickyNote.setSelected(SELECT_VAL)


            # creating dot_divide_bty
            dot_divide_bty = nuke.nodes.Dot()
            dot_divide_bty['xpos'].setValue(int(middle_dot['xpos'].value()))
            dot_divide_bty['ypos'].setValue(int(dotCorner['ypos'].value()) - (Y_DIST * 4))
            dot_divide_bty.setSelected(SELECT_VAL)
            dot_divide_bty.setInput(0, middle_dot)

            # creating merge_divide_bty
            merge_divide_bty = nuke.nodes.Merge2()
            merge_divide_bty['xpos'].setValue(int(copyNode['xpos'].value()))
            merge_divide_bty['ypos'].setValue(int(dot_divide_bty['ypos'].value()) + (merge_divide_bty.screenHeight() / 2) - (dot_divide_bty.screenHeight() / 2))
            merge_divide_bty['operation'].setValue('divide')
            merge_divide_bty.setSelected(SELECT_VAL)
            merge_divide_bty.setInput(0, copyNode)
            merge_divide_bty.setInput(1, dot_divide_bty)

            # creating merge_multiply
            merge_multiply = nuke.nodes.Merge2()
            merge_multiply['xpos'].setValue(int(merge_divide_bty['xpos'].value()))
            merge_multiply['ypos'].setValue(int(dotCorner['ypos'].value()))
            merge_multiply['operation'].setValue('multiply')
            merge_multiply.setSelected(SELECT_VAL)
            merge_multiply.setInput(0, merge_divide_bty)
            merge_multiply.setInput(1, dotCorner)
