setAutoThreshold("Otsu dark");
setOption("BlackBackground", true);
run("Convert to Mask");
run("Erode");
run("Erode");
run("Erode");
run("Analyze Particles...", "size=10-Infinity display exclude clear include");
