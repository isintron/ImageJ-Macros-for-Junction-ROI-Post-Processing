//-------------------------------------------------------
// Junction_filter_live.ijm
// Filter ROIs in the ROI Manager by geometry:
//  - Measure Length (Area) and Feret’s diameter
//  - Compute Curvature = Length / Feret
//  - Remove ROIs that are short or curved than expected
//
// Author: adapted for Jing He (jinghe@stu.ouc.edu.cn)
// Date: 2025-10-09
//-------------------------------------------------------


// ===== Adjustable parameters =====
minLength = 1.5;     // Minimum allowed length
maxCurvature = 1.2; // Maximum allowed curvature (Length/Feret)


// ===== Preparation =====
if (roiManager("count") == 0)
    exit("ROI Manager is empty!");

// Set measurements: Area, Feret's diameter, Perimeter
run("Set Measurements...", "area & feret's diameter");

// Clear previous Results table
run("Clear Results");


// ===== Main loop =====
n = roiManager("count");
filtered = 0;
deleted = 0;

// The ROI is removed in reverse order to ensure that the index is not misaligned.
for (i = n - 1; i >= 0; i--) {
    roiManager("Select", i);
    run("Measure");
    
    // Retrieve last measurement (most recent row)
    idx = nResults - 1;
    L = getResult("Length", idx);
    F = getResult("Feret", idx);

    if (isNaN(L) || isNaN(F) || F == 0) {
        roiManager("Delete");
        deleted++;
        continue;
    }

    Curv = L / F;
    setResult("Curvature", idx, Curv);

    // Filter condition
    if (L < minLength || Curv > maxCurvature) {
        roiManager("Delete");
        deleted++;
    } else {
        filtered++;
    }
}

// Update results
updateResults();


// ===== Final message =====
showMessage("Junction Filtering Complete",
    "Original ROIs: " + n + "\n" +
    "Remaining after filtering: " + filtered + "\n" +
    "Deleted ROIs: " + deleted);
