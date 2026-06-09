# ImageJ Macros for Junction ROI Post-Processing

Jing He 
jinghe@stu.ouc.edu.cn

ImageJ macro scripts for cleaning up cell junction ROIs exported from **[Tissue Analyzer (Java edition)](https://github.com/baigouy/tissue_analyzer)**, removing unwanted vertices and curved borders before quantitative analysis.

## Background

A workflow (see [Zhang et. al.](https://www.biorxiv.org/content/10.1101/2024.08.29.610110v1) for more details) for extracting cell borders from epithelial images in Tissue Analyzer (Java) is:

1. Import a raw fluorescence image marks cell border (e.g., E-cadherin–GFP)
2. Apply Gaussian filtering and contrast enhancement (e.g., [CLAHE](https://imagej.net/plugins/clahe))
3. Run watershed segmentation to detect cell outlines
4. Use Track Bonds >Export ROIs to IJ, apply skeleton erosion to produce desired junction segments with vertices removed
5. Load individual junction segments into the ImageJ ROI Manager for downstream intensity or geometry measurements

**Skeleton erosion** is designed to remove tricellular vertices, but in practice it leaves two categories of problematic ROIs in the exported set:

- **Residual vertex ROIs**: very short fragments located at cell corners that were not fully removed
- **Curved border ROIs**: arc-shaped segments that span around cell vertices rather than running straight between two tricellular junctions

> Both artifact types confound junction-level analyses: vertex ROIs inflate ROI counts and skew intensity measurements, while curved borders mix signal from geometrically distinct membrane domains.

## Geometry-based filtering

These scripts remove unwanted ROIs using two straightforward geometric criteria:

1. Minimum length threshold: Short ROIs (below a user-defined length) are assumed to be residual vertex fragments and are deleted.

2. Curvature threshold: Curvature is defined as: `Curvature = Length / Feret diameter`

where the [Feret diameter](https://imagej.net/ij/docs/menus/analyze.html#set) is the maximum caliper distance across the ROI. For a straight junction, `Length ≈ Feret`, giving a curvature near 1.0. Curved borders have a longer arc length relative to their end-to-end span, yielding curvature values substantially greater than 1.0. ROIs exceeding the curvature threshold are removed.

## Scripts

`junction_filter_live.ijm`

Filters all ROIs currently loaded in the ROI Manager by length and curvature.

**Usage:**

1. Load junction ROIs into the ROI Manager (e.g., via Tissue Analyzer >Track Bonds >Export ROIs to IJ)
2. Open the script in the ImageJ Script Editor and run it
3. Adjust the two parameters at the top of the script as needed:

| Parameter      | Default                | Description                                                  |
| -------------- | ---------------------- | ------------------------------------------------------------ |
| `minLength`    | User-definition needed | Minimum ROI length (**same units as image calibration**). ROIs shorter than this are deleted. |
| `maxCurvature` | 1.2                    | Maximum allowed curvature (Length / Feret). ROIs above this threshold are deleted. |

4. A summary dialog reports the number of ROIs kept and deleted.

> **Tip:** Run on a representative image first to verify that the defaults suit your data. Straight junctions in typical epithelial images have curvature values between 1.0–1.15; curved borders usually exceed 1.2–1.3.

`kill_outside-of-square_rois.ijm`

Restricts analysis to a user-defined rectangular region of interest by deleting all ROIs whose bounding box falls outside the drawn rectangle. Useful when you want to analyze only a specific subregion of the image (e.g., a region of interest within the germband) without re-segmenting.

**Usage:**

1. Load junction ROIs into the ROI Manager
2. **Draw a rectangular selection** on the image using the Rectangle tool — do **not** deselect it
3. Run the script
4. All ROIs not fully contained within the rectangle will be deleted; a confirmation dialog appears when complete

> **Note:** The script uses a strict containment criterion — ROIs that merely overlap the rectangle boundary are also removed. To change this to overlap-based retention, comment out the default condition block and uncomment the alternative block at the bottom of the script.
