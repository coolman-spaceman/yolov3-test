#***********************   CHANGE CODE ONLY WHERE SPECIFIED  **************************

#***********************   DO NOT TOUCH OTHER CODE           *************************
import cv2
import numpy as np
import glob
import random


# Load Yolo
modelConfiguration = "yolov3-tiny_obj.cfg"  ### configuratoin file path
modelWeights = "yolov3-tiny_obj_1000.weights"   ### PUT YOUR WEIGHTS FILE PATH HERE


net = cv2.dnn.readNet(modelWeights, modelConfiguration)

# Name custom object
classes = ["circle","square","cylinder"]  ## change these names according to your custom classes 

# GIVE IMAGE PATH
image_path = ("/home/deejay/yolo_trainer/image/image0.jpg")



layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread(image_path)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
	for detection in out:
		scores = detection[5:]
		class_id = np.argmax(scores)
		confidence = scores[class_id]
		if confidence > 0.3:
			print(class_id)
			center_x = int(detection[0] * width)
			center_y = int(detection[1] * height)
			w = int(detection[2] * width)
			h = int(detection[3] * height)
			# Rectangle coordinates
			x = int(center_x - w / 2)
			y = int(center_y - h / 2)
			boxes.append([x, y, w, h])
			confidences.append(float(confidence))
			class_ids.append(class_id)
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
print(indexes)
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
	if i in indexes:
		x, y, w, h = boxes[i]
		label = str(classes[class_ids[i]])
		color = colors[class_ids[i]]
		cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
		cv2.putText(img, label, (x, y + 30), font, 1, color, 1)
cv2.imshow("Image", img)
key = cv2.waitKey(0)
cv2.destroyAllWindows()