action("/Users/UZH-wezhon/Desktop/Auri_exp3_sorted/",
       "230412 63x Exp 3_F4L_5_24_cmle_batch",
       // change here the file name
       "/ch00/"
);

function action(input, filename, ch) {		
	File.openSequence(input + filename + ch);
	selectImage("ch00");
	run("Z Project...", "projection=[Max Intensity]");
	saveAs("Tiff", input + filename + "/" + filename + "MAX_ch00.tif");
	close();
	selectImage("ch00");
	close();
}

