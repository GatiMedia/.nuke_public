# --------------------------------------------------------------
#  unreal_cam_to_nuke.py
#  Version: 1.0
#  Last Updated: 07/02/2024
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
            conv_cam.setSelected(True)
