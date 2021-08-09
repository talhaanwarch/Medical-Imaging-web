import onnxruntime
from PIL import Image
import cv2
import numpy as np
#import matplotlib.pyplot as plt
path='segmentation_app/py_templates/checkpoints/'
ort_session = onnxruntime.InferenceSession(path+"ultrasound.onnx")
from .segmentor import normalize

def opencv_fitEllipse(binary_mask, method="Direct"):
    print(binary_mask)
    assert binary_mask.min() >= 0.0 and binary_mask.max() <= 1.0
    points = np.argwhere(binary_mask > 0.5)  # TODO: tune threshold

    if method == "AMS":
        (xx, yy), (MA, ma), angle = cv2.fitEllipseAMS(points)
    elif method == "Direct":
        (xx, yy), (MA, ma), angle = cv2.fitEllipseDirect(points)
    elif method == "Simple":
        (xx, yy), (MA, ma), angle = cv2.fitEllipse(points)
    else:
        raise ValueError("Wrong method")

    return (xx, yy), (MA, ma), angle
def calculate_circum(mask,factor):
  """
  Calculate circumference of ellipse
  """
  (xx, yy), (MA, ma), angle = opencv_fitEllipse(mask)
  #assert 512 / mask.shape[1] == 800 / mask.shape[2]
  
  center_x_mm = factor * yy
  center_y_mm = factor * xx
  semi_axes_a_mm = factor * ma / 2
  semi_axes_b_mm = factor * MA / 2
  angle_rad = (-angle * np.pi / 180) % np.pi
  #calculate circumference to check if it matches the ground circumferencce
  h = (semi_axes_a_mm - semi_axes_b_mm) ** 2 / (
      semi_axes_a_mm + semi_axes_b_mm
  ) ** 2
  circ = (
      np.pi
      * (semi_axes_a_mm + semi_axes_b_mm)
      * (1 + (3 * h) / (10 + np.sqrt(4 - 3 * h)))
  )
  return circ,[center_x_mm,center_y_mm,semi_axes_a_mm,semi_axes_b_mm,angle_rad]

def predict(img_path):
  image = Image.open(img_path).convert('L')
  img=image.resize((384,384))
  img=normalize(np.array(img))#shape is (224,224)
  img=np.expand_dims(img,0)#shape is (1,224,224)
  img=np.expand_dims(img,0)#shape is (1,1,224,224)
  ort_inputs = {ort_session.get_inputs()[0].name: img}
  ort_outs = ort_session.run(None, ort_inputs)
  img_out_y = ort_outs[0]
  img_out_y=img_out_y[0,0,:,:]
  img_out_y=np.where(img_out_y>0.5,1,0)
  img_out_y=cv2.resize(img_out_y.astype('float32'),(image.size))
  #erosion and dilution
  kernel = np.ones((5,5), np.uint8)
  img_out_y = cv2.erode(img_out_y, kernel, iterations=5)
  img_out_y = cv2.dilate(img_out_y, kernel, iterations=20) 
  return img_out_y,image