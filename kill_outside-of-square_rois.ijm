// Delete ROIs outside of a user-defined rectangular ROI
// Jing's customized version — keep only ROIs fully inside the drawn rectangle

// Step 1: Draw a rectangular ROI on your image manually before running this macro!
// Attention! Do NOT unselect the rectangular ROI!
// Step 2: Run this macro — it will delete all ROIs outside of that rectangle.

if (selectionType == -1) {
    exit("Please draw a rectangular ROI first.");
}

getSelectionBounds(xR, yR, wR, hR);
xR2 = xR + wR;
yR2 = yR + hR;

run("Set Measurements...", "bounding redirect=None decimal=3");
n = roiManager("count");

for (i = n - 1; i >= 0; i--) {  // iterate in reverse so deletion won't mess up indexing
    roiManager("select", i);
    getSelectionBounds(x, y, w, h);
    x2 = x + w;
    y2 = y + h;

//  condition: ROI must be fully inside the rectangle
   	if (x < xR || y < yR || x2 > xR2 || y2 > yR2) {
        roiManager("delete");
		}
//// keep if overlaps with rectangle at all
//	if (x2 < xR || x > xR2 || y2 < yR || y > yR2) {
//    	roiManager("delete");
//}
    }

showMessage("Finished: kept only ROIs fully within the rectangle.");
