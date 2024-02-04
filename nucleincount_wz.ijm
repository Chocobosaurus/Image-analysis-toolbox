setAutoThreshold("Default dark");
//run("Threshold...");
setThreshold(190, 65535, "raw");
setThreshold(190, 65535, "raw");
setOption("BlackBackground", true);
run("Convert to Mask");
run("Erode");
run("Erode");
run("Watershed");
run("Analyze Particles...", "size=600-Infinity summarize overlay");
run("Invert");
close();

