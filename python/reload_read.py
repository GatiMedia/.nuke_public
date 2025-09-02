# --------------------------------------------------------------
#  reload_read.py
#  Last Updated by: Attila Gasparetz
#  Last Updated: 02/09/2025
# --------------------------------------------------------------

import nuke

def reload_all_read():
  for node in nuke.allNodes('Read'):
    node['reload'].execute()

def reload_sel_nodes():
  for node in nuke.selectedNodes('Read'):
    node['reload'].execute()
