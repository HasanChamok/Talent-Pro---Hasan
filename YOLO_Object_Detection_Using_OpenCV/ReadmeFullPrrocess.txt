1-->Initialization and setup
	a)Download and Install Python
	b)create a folder 
	c)open cmd in the file location and create an environment
		command: python -m venv yolo_venv               // Here yolo_venv is the name of the environment
	d)Activate the environment
		command: yolo_venv\Scripts\activate

	e)Now download the requirements in the requirements.txt
		command: pip install -r requirements.txt
2-->Data Collection and Labelling
	a)Dos & Don'ts
		.Try to use Hd image it is always recommended(Minimum height and weight should be 500 x 500)
		.Avoid Blur image
		.Avoid cluttery background images for objects
		
		>Open source websites for image downloading 
		.google , flicker, unplash, pexels
		.From pascal VOc you can download entire dataset
	b) Create a folder inside the main folder (1_datapreparation)
	c) Create another folder inside the newly created folder (data_images)
	d) Download images and annotate
3-->Downloa and install jupyter notebook
	a)run it in the 1_datapreparation file
	
	Steps:
	1)import necessary packages
	2)load xml files and load it in a list
	3)replace \\ with /
	4)step-2: read xml files
	#from each xml file we need to extract 
	#filename, size(width,height), object(name,xmin,xmax,ymin,ymax)
	5)For multiple xml file we have to run it into a loop
	6)Convert it into map then to list
	7)convert 3d list to 2d list
	8)Add the list to the database
4-->Preparing labels for Yolo Model
	We need information for center x and center y
	centerX , centerY = center position of the object normalized to width of the image
	w,h= width and height of the bounding box normalized to the width and height of the image

	so [name,xmin,xmax,ymin,ymax] will be converted to [name,centerX,centerY,w,h]
	
	centerX = ((xmin+xmax)/2)/width of the image
	centerY = ((ymin+ymax)/2)/width of the image
	w = ((xmax - xmin)/2)/width of the image
	h = ((ymax - ymin)/2)/width of the image



