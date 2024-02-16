# --------------------------------------------------------------
#  change_channels.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 16/02/2024
# --------------------------------------------------------------

import nuke

def changeChannels():
    sel_nodes = nuke.selectedNodes()
    if len(sel_nodes) > 0:
        ok_channels = ['all', 'none', 'rgba', 'rgb', 'alpha']
        ok_channels_shuffle = ['none', 'rgba', 'rgb', 'alpha']
        ok_operation_merge = ['max', 'min', 'multiply', 'over', 'plus', 'screen', 'stencil']
        ok_operation_channelmerge = ['max', 'min', 'multiply', 'plus', 'stencil', 'union']

        for sel_node in sel_nodes:

            # setting up for channels knob
            if sel_node.knob('channels'):
                if not sel_node['channels'].value() == "alpha" and sel_node.knob('channels').value() in ok_channels:
                    channel_index = ok_channels.index(sel_node['channels'].value())
                    sel_node['channels'].setValue(ok_channels[channel_index + 1])
                else:
                    sel_node['channels'].setValue('all')

            # setting up for output knob
            if sel_node.knob('output'):
                if not sel_node.Class() == "Merge2":
                    if not sel_node.Class() == "ChannelMerge":
                        try:
                            if not sel_node['output'].value() == "alpha" and sel_node.knob('output').value() in ok_channels:
                                channel_index = ok_channels.index(sel_node['output'].value())
                                sel_node['output'].setValue(ok_channels[channel_index + 1])
                            else:
                                sel_node['output'].setValue('all')
                        except:
                            pass

            # setting up for retimedChannels knob
            if sel_node.knob('retimedChannels'):
                if not sel_node['retimedChannels'].value() == "alpha" and sel_node.knob('retimedChannels').value() in ok_channels:
                    channel_index = ok_channels.index(sel_node['retimedChannels'].value())
                    sel_node['retimedChannels'].setValue(ok_channels[channel_index + 1])
                else:
                    sel_node['retimedChannels'].setValue('all')

            # setting up for operation knob on Merge
            if sel_node.knob('operation'):
                if sel_node.Class() == 'Merge2':
                    if not sel_node['operation'].value() == "stencil":
                        channel_index = ok_operation_merge.index(sel_node['operation'].value())
                        sel_node['operation'].setValue(ok_operation_merge[channel_index + 1])
                    else:
                        sel_node['operation'].setValue('max')

            # setting up for operation knob on ChannelMerge
                if sel_node.Class() == 'ChannelMerge':
                    if not sel_node['operation'].value() == "union":
                        channel_index = ok_operation_channelmerge.index(sel_node['operation'].value())
                        sel_node['operation'].setValue(ok_operation_channelmerge[channel_index + 1])
                    else:
                        sel_node['operation'].setValue('max')

            # setting up for old shuffle node
            if sel_node.knob('in'):
                channels = ['red','green','blue','alpha']
                if not sel_node['in'].value() == "alpha" and sel_node.knob('in').value() in ok_channels_shuffle:
                    channel_index = ok_channels_shuffle.index(sel_node['in'].value())
                    sel_node['in'].setValue(ok_channels_shuffle[channel_index + 1])
                else:
                    sel_node['in'].setValue('none')
                if sel_node['in'].value() == "none":
                    for c in channels:
                        sel_node[c].setValue('black')
                if sel_node['in'].value() == "rgb":
                    for c in channels:
                        sel_node[c].setValue(c)
                    sel_node['alpha'].setValue('black')
                if sel_node['in'].value() == "rgba":
                    for c in channels:
                        sel_node[c].setValue(c)
                if sel_node['in'].value() == "alpha":
                    for c in channels:
                        sel_node[c].setValue('white')
                    sel_node['alpha'].setValue('white')

            # setting up for new shuffle node
            if sel_node.knob('in1'):
                if not sel_node['in1'].value() == "alpha" and sel_node.knob('in1').value() in ok_channels_shuffle:
                    channel_index = ok_channels_shuffle.index(sel_node['in1'].value())
                    sel_node['in1'].setValue(ok_channels_shuffle[channel_index + 1])
                else:
                    sel_node['in1'].setValue('none')
                if sel_node['in1'].value() == "none":
                    sel_node['mappings'].setValue([(-1, 'black', 'rgba.red'), (-1, 'black', 'rgba.green'), (-1, 'black', 'rgba.blue'), (-1, 'black', 'rgba.alpha')])
                if sel_node['in1'].value() == "rgb":
                    sel_node['mappings'].setValue([(0, 'rgba.red', 'rgba.red'), (0, 'rgba.green', 'rgba.green'), (0, 'rgba.blue', 'rgba.blue'), (-1, 'black', 'rgba.alpha')])
                if sel_node['in1'].value() == "rgba":
                    sel_node['mappings'].setValue([(0, 'rgba.red', 'rgba.red'), (0, 'rgba.green', 'rgba.green'), (0, 'rgba.blue', 'rgba.blue'), (0, 'rgba.alpha', 'rgba.alpha')])
                if sel_node['in1'].value() == "alpha":
                    sel_node['mappings'].setValue([(-1, 'black', 'rgba.red'), (-1, 'black', 'rgba.green'), (-1, 'black', 'rgba.blue'), (0, 'rgba.alpha', 'rgba.alpha')])
    else:
        nuke.message('<center><b>Select a node/nodes first!</b>\n\n<b>This function iterates through the following channels:</b>\n<i>all, none, rgba, rgb, alpha</i>\n\n<b>And the following channels for Shuffle:</b>\n<i>none, rgba, rgb, alpha</i>\n\n\n\n<b>And the following operations for Merge:</b>\n<i>max, min, multiply, over, plus, screen, stencil</i>\n\n<b>And the following operations for ChannelMerge:</b>\n<i>max, min, multiply, plus, stencil, union</i></center>')
