"""
============================================================
Fiji Script: Assign Position and Group for Square ROIs
============================================================

Author: Jing He (贺靖)
Affiliation: Ocean University of China
Version: v1.1
Date: 2026-04-14

------------------------------------------------------------
Description
------------------------------------------------------------
This script processes Square (Rectangle) ROIs in the
Fiji ROI Manager.

Functions:
    1. Parse ROI name to extract time slice number
       Example ROI name:
           0048-0034-0134
           -> slice (T) = 48

    2. Assign ROI hyperstack position:
           DimensionOrder = XYCZT
           ROI position → Frame (T)

    3. Assign user-defined ROI group

------------------------------------------------------------
Requirements
------------------------------------------------------------
- Image must be opened as Hyperstack
- ROI names must start with slice number
- Only Rectangle/Square ROIs will be processed

============================================================
"""

from ij.plugin.frame import RoiManager
from ij import IJ
from ij.gui import Roi
from java.awt import Color

# ==============================
# User Settings
# ==============================

n_group = 1   # ROI group ID
stroke_color = Color.yellow   # ROI color

# Available colors:
# Color.red, Color.green, Color.blue,
# Color.yellow, Color.cyan, Color.magenta,
# Color.white, Color.orange, Color.pink

# ==============================
# Initialize
# ==============================

rm = RoiManager.getInstance()

if rm is None or rm.getCount() == 0:
    IJ.error("ROI Manager is empty!")
    exit()

imp = IJ.getImage()

# ==============================
# Main Loop
# ==============================

for i in range(rm.getCount()):

    roi = rm.getRoi(i)

    # ---- Only process Rectangle/Square ROI ----
    if roi.getType() != Roi.RECTANGLE:
        print("Skipped (not square):", roi.getName())
        continue

    name = roi.getName()
    parts = name.split("-")

    if len(parts) < 1:
        print("Skipped (invalid name):", name)
        continue

    # ---- extract slice number ----
    try:
        slice_number = int(parts[0])
    except:
        print("Skipped (cannot parse slice):", name)
        continue

    # ---- assign hyperstack position ----
    # DimensionOrder = XYCZT → frame = T
    roi.setPosition(0, 0, slice_number)

    # ---- assign group ----
    roi.setGroup(n_group)
    
    # ---- appearance settings ----
    roi.setStrokeColor(stroke_color)

    # refresh ROI Manager
    rm.setRoi(roi, i)

print("Finished updating Square ROIs.")
