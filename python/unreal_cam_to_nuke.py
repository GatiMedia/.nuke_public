# --------------------------------------------------------------
#  unreal_cam_to_nuke.py
#  Version: 1.1
#  Last Updated: 11/06/2024
#  Last updated by: Attila Gasparetz
# --------------------------------------------------------------
import nuke

def unrealCamToNuke():
    if not len(nuke.selectedNodes()) == 1:
        nuke.alert('<font color=orange><h3>Select a single Camera from Unreal first!')
    else:
        if "Camera" not in str(nuke.selectedNode().Class()):
            nuke.alert('<font color=orange><h3>Select a single Camera from Unreal first!')
        else:
            sel_cam = nuke.selectedNode()
            sel_cam_name = sel_cam.name()
            conv_cam = nuke.nodes.Camera3()
            conv_cam['xpos'].setValue(int(sel_cam['xpos'].value())+110)
            conv_cam['ypos'].setValue(int(sel_cam['ypos'].value())+48)
            conv_cam['translate'].setExpression("parent."+sel_cam_name+".translate",0)
            conv_cam['translate'].setExpression("parent."+sel_cam_name+".translate",1)
            conv_cam['translate'].setExpression("parent."+sel_cam_name+".translate",2)
            conv_cam['rotate'].setExpression("-parent."+sel_cam_name+".rotate.y",0)
            conv_cam['rotate'].setExpression("parent."+sel_cam_name+".rotate.z-90",1)
            conv_cam['rotate'].setExpression("-parent."+sel_cam_name+".rotate.x+90",2)
            conv_cam['projection_mode'].setExpression("parent."+sel_cam_name+".projection_mode")
            conv_cam['focal'].setExpression("parent."+sel_cam_name+".focal")
            conv_cam['haperture'].setExpression("parent."+sel_cam_name+".haperture")
            conv_cam['vaperture'].setExpression("parent."+sel_cam_name+".vaperture")
            conv_cam['near'].setExpression("parent."+sel_cam_name+".near")
            conv_cam['far'].setExpression("parent."+sel_cam_name+".far")
            conv_cam['win_translate'].setExpression("parent."+sel_cam_name+".win_translate",0)
            conv_cam['win_translate'].setExpression("parent."+sel_cam_name+".win_translate",1)
            conv_cam['win_scale'].setExpression("parent."+sel_cam_name+".win_scale",0)
            conv_cam['win_scale'].setExpression("parent."+sel_cam_name+".win_scale",1)
            conv_cam['winroll'].setExpression("parent."+sel_cam_name+".winroll")
            conv_cam['focal_point'].setExpression("parent."+sel_cam_name+".focal_point")
            conv_cam['fstop'].setExpression("parent."+sel_cam_name+".fstop")
            conv_cam['shutter'].setExpression("parent."+sel_cam_name+".shutter")
            conv_cam['shutteroffset'].setExpression("parent."+sel_cam_name+".shutteroffset")
            conv_cam.setSelected(True)
