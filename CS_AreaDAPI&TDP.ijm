
img_name=getTitle();

run("Z Project...", "projection=[Max Intensity]");
run("Split Channels");
selectWindow("C3-MAX_"+img_name);
run("Gaussian Blur...", "sigma=2");
setAutoThreshold("Default dark");
//run("Threshold...");
setOption("BlackBackground", true);
run("Convert to Mask");
selectWindow("C2-MAX_"+img_name);
selectWindow("C1-MAX_"+img_name);
run("Gaussian Blur...", "sigma=2");
setAutoThreshold("Default dark");
//run("Threshold...");
//setThreshold(255, 255);
run("Convert to Mask");
run("Analyze Particles...", "size=0.84-Infinity show=[Count Masks] display summarize");
selectWindow("C3-MAX_"+img_name);
run("Analyze Particles...", "size=0.84-Infinity show=[Count Masks] display summarize");
