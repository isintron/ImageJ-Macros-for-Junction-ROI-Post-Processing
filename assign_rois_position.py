"""
Assign ROI Position, Group, and Appearance

Author: adapted for Jing He (jinghe@stu.ouc.edu.cn)
Date: 2026-04-09

Requirements:
- Image must be opened as a Hyperstack (e.g., XYCZT)
- ROI Manager must contain ROIs
- ROI names must start with slice number
	This scirpt parses ROI name to extract time slice number
	Example ROI name: 0048-0034-0134 -> slice (T) = 48
"""

from ij.plugin.frame import RoiManager
from ij import IJ
from java.awt import Color

# ==============================
# User settings
# ==============================

n_group = 1          # group number
stroke_width = 3     # line pixel width

# Choose color
stroke_color = Color.yellow

# examples:
# Color.green
# Color.blue
# Color.yellow
# Color.white
# Color.cyan

# ==============================
# Get ROI Manager
# ==============================

rm = RoiManager.getInstance()

if rm is None or rm.getCount() == 0:
    IJ.error("ROI Manager is empty!")
    exit()

imp = IJ.getImage()

# ==============================
# Main loop
# ==============================

for i in range(rm.getCount()):

    roi = rm.getRoi(i)
    name = roi.getName()

    parts = name.split("-")

    if len(parts) < 1:
        print("Skip:", name)
        continue

    # ---- extract slice number ----
    slice_number = int(parts[0])

    # ---- assign position (T) ----
    # DimensionOrder = XYCZT
    roi.setPosition(0, 0, slice_number)

    # ---- assign group ----
    roi.setGroup(n_group)

    # ---- set stroke color ----
    roi.setStrokeColor(stroke_color)

    # ---- set line width ----
    roi.setStrokeWidth(stroke_width)

    # refresh ROI Manager entry
    rm.setRoi(roi, i)

print("Finished.")