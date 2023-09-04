import nuke

def shuffleRGB():
    for node in nuke.selectedNodes():
        try:
            dot = nuke.nodes.Dot()
            dot['xpos'].setValue(node['xpos'].value() + 35)
            dot['ypos'].setValue(node['ypos'].value() + 150)
            dot.setInput(0, node)
            
            shuffleR = nuke.createNode('Shuffle2')
            shuffleR['xpos'].setValue(dot['xpos'].value() - 144)
            shuffleR['ypos'].setValue(dot['ypos'].value() + 120)
            shuffleR['mappings'].setValue([(0, 'rgba.red', 'rgba.red'), (0, 'rgba.red', 'rgba.green'), (0, 'rgba.red', 'rgba.blue'), (0, 'rgba.red', 'rgba.alpha')])
            shuffleR['tile_color'].setValue(4278190335)
            shuffleR['label'].setValue('[value in1]')
            shuffleR.hideControlPanel()

            shuffleG = nuke.createNode('Shuffle2')
            shuffleG['xpos'].setValue(dot['xpos'].value() - 34)
            shuffleG['ypos'].setValue(dot['ypos'].value() + 120)
            shuffleG['mappings'].setValue([(0, 'rgba.green', 'rgba.red'), (0, 'rgba.green', 'rgba.green'), (0, 'rgba.green', 'rgba.blue'), (0, 'rgba.green', 'rgba.alpha')])
            shuffleG['tile_color'].setValue(536805631)
            shuffleG['label'].setValue('[value in1]')
            shuffleG.hideControlPanel()

            shuffleB = nuke.createNode('Shuffle2')
            shuffleB['xpos'].setValue(dot['xpos'].value() + 76)
            shuffleB['ypos'].setValue(dot['ypos'].value() + 120)
            shuffleB['mappings'].setValue([(0, 'rgba.blue', 'rgba.red'), (0, 'rgba.blue', 'rgba.green'), (0, 'rgba.blue', 'rgba.blue'), (0, 'rgba.blue', 'rgba.alpha')])
            shuffleB['tile_color'].setValue(10485759)
            shuffleB['label'].setValue('[value in1]')
            shuffleB.hideControlPanel()

            dot.setInput(0, node)
            shuffleR.setInput(0, dot)
            shuffleR.setInput(1, None)
            shuffleG.setInput(0, dot)
            shuffleG.setInput(1, None)
            shuffleB.setInput(0, dot)
            shuffleB.setInput(1, None)
        except Exception:
            pass
