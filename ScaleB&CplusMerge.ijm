action("/Users/UZH-wezhon/Desktop/decon/",
       "seedinginA1A2GA_20x81xyrep32_Nov07_",
       // change here the file name
       "unlabGFPLCD_1_75",   
       "_cmle_ch00.tif",
       "_cmle_ch01.tif",
       "_cmle_ch02.tif",
       "_cmle_ch03.tif"
);

function action(input, prefix, filename, postfix00, postfix01, postfix02, postfix03) {	
	open(input + prefix + filename + postfix00);
    selectImage(prefix + filename + postfix00);
    setMinAndMax(0, 13000);
	run("Green");
	open(input + prefix + filename + postfix01);
	selectImage(prefix + filename + postfix01);
	setMinAndMax(0, 18000);
	run("Yellow");
	open(input + prefix + filename + postfix02);
	selectImage(prefix + filename + postfix02);
	setMinAndMax(0, 17000);
	run("Red");
	open(input + prefix + filename + postfix03);
	selectImage(prefix + filename + postfix03);
	setMinAndMax(0, 45000);
	run("Grays");
	
	run("Merge Channels...", 
	"c1=[" + prefix + filename + postfix02 + "] c2=[" + prefix + filename + postfix00 + "] c4=[" + prefix + filename + postfix03 + "]create keep");
}