import onnxruntime
from PIL import Image
import numpy as np
ort_session = onnxruntime.InferenceSession("chestmodel.onnx")
#decode={0: 'BCC', 1: 'ACK', 2: 'NEV', 3: 'SCC', 4: 'SEK', 5: 'MEL'}
img = Image.open("view1_frontal.jpg").convert('L')
img = img.resize((224,224))
img=np.array(img)
img=np.moveaxis(img,2,0)
img=np.expand_dims(img,0)/255.0
print(img.shape)
img [:,0,:,:] = (img [:,0,:,:]  * 0.5) / 0.5
# img [:,1,:,:] = (img [:,1,:,:] - 255 * 0.4512) / 255 * 0.1858
# img [:,2,:,:] = (img [:,2,:,:] - 255 * 0.4023) / 255 * 0.1705
img=img.astype(np.float32)
ort_inputs = {ort_session.get_inputs()[0].name: img}
ort_outs = ort_session.run(None, ort_inputs)
# img_out_y = np.argmax(ort_outs[0],1)[0]
# result=decode[img_out_y]
# print(result)
