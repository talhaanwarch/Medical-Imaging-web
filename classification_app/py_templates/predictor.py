import onnxruntime
from PIL import Image
import numpy as np
path='classification_app/py_templates/checkpoints/'
def scaling(img,channels=3):
	if len(channels)==3:
		img[:,:,0] = (img [:,:,0] - 0.5820) / 0.2217
		img[:,:,1] = (img [:,:,1] - 0.4512) / 0.1858
		img[:,:,2] = (img [:,:,2] - 0.4023) / 0.1705
	elif len(channels)==2:
		img = (img - 0.5) / 0.5
		img=np.expand_dims(img,2)
	return img 

def predict(model,image):
	if model=='covid':
		decode={0: 'positive', 1:'negative'}
		img=Image.open(image)
		img=img.resize((60,60))
		img=np.array(img)/255
		img=np.expand_dims(img,0)
		ort_session = onnxruntime.InferenceSession(path+"covidxray.onnx")
	else:
		if model=='skin':
			decode={0: 'BCC', 1: 'ACK', 2: 'NEV', 3: 'SCC', 4: 'SEK', 5: 'MEL'}
			img = Image.open(image).convert('RGB')
			ort_session = onnxruntime.InferenceSession(path+"skinmodel.onnx")

		elif model=='ecg':
			decode={0: 'Covid', 1: 'AbNormal', 2: 'MI', 3: 'MI_recovered', 4: 'Normal'}
			img = Image.open(image).convert('RGB')
			ort_session = onnxruntime.InferenceSession(path+"ecgimages.onnx")
		elif model=='xray':
			decode={0: 'No Finding', 1: 'Enlarged Cardiomediastinum', 2: 'Cardiomegaly', 3: 'Lung Opacity', 4: 'Lung Lesion', 5: 'Edema', 6: 'Consolidation', 7: 'Pneumonia', 8: 'Atelectasis', 9: 'Pneumothorax', 10: 'Pleural Effusion', 11: 'Pleural Other', 12: 'Fracture', 13: 'Support Devices'}
			img = Image.open(image).convert('L')
			ort_session = onnxruntime.InferenceSession(path+"chestmodel.onnx")

		img = img.resize((224,224))
		img=np.array(img)
		img=scaling(img,channels=img.shape)
		img=np.moveaxis(img,2,0)
		img=np.expand_dims(img,0)
	
	img=img.astype(np.float32)
	ort_inputs = {ort_session.get_inputs()[0].name: img}
	ort_outs = ort_session.run(None, ort_inputs)
	img_out_y = np.argmax(ort_outs[0],1)[0]
	result=decode[img_out_y]
	return result
