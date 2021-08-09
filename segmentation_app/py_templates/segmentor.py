import onnxruntime
from PIL import Image
#import cv2
import numpy as np
#import matplotlib.pyplot as plt
path='segmentation_app/py_templates/checkpoints/'
ort_session = onnxruntime.InferenceSession(path+"ultrasound.onnx")


def normalize(img, mean=0, std=1, max_pixel_value=255.0):
	#albumentation function normalization
    mean = np.array(mean, dtype=np.float32)
    mean *= max_pixel_value

    std = np.array(std, dtype=np.float32)
    std *= max_pixel_value

    denominator = np.reciprocal(std, dtype=np.float32)

    img = img.astype(np.float32)
    img -= mean
    img *= denominator
    return img

def predict(img_path,imgsize=224,resized=None):
	img = Image.open(img_path).convert('L')
	image=img.resize((imgsize,imgsize))
	img=normalize(np.array(image))#shape is (224,224)
	img=np.expand_dims(img,0)#shape is (1,224,224)
	img=np.expand_dims(img,0)#shape is (1,1,224,224)
	ort_inputs = {ort_session.get_inputs()[0].name: img}
	ort_outs = ort_session.run(None, ort_inputs)
	img_out_y = ort_outs[0]
	img_out_y=img_out_y[0,0,:,:]
	#img_out_y=Image.fromarray(np.uint8(img_out_y*255))

	return image,img_out_y

