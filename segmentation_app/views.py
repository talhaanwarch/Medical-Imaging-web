from django.shortcuts import render
# def home(request):
# 	return render(request,'segmentation_home.html',{'print':"every thing ok"})
import io
import base64
import numpy as np
from PIL import Image
from .forms import UploadForm,HCForm
from .py_templates import segmentor,hcsegmentor
# Create your views here.

def out_image(image,mask):
   mask=Image.fromarray(np.uint8(mask*255))
   #https://stackoverflow.com/a/40568024/11170350
   def encodedecode(img):
      data = io.BytesIO()
      img.save(data, "JPEG")
      encoded_img_data = base64.b64encode(data.getvalue())
      out=encoded_img_data.decode('utf-8')
      return out
   image=encodedecode(image)
   mask=encodedecode(mask)
   return image,mask

def home(request):
   if request.method == 'POST':
      form = UploadForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         image,segment=segmentor.predict(form.cleaned_data['image'])                  
         image,segment=out_image(image,segment)
         
      context={'printform':form,'image':image,'segment':segment }
      return render(request,'segmentation_home.html',context)   
   else:
      form = UploadForm()
   context={'printform':form}
   return render(request,'segmentation_home.html',context)

def hchome(request):
   if request.method == 'POST':
      form = HCForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         pred,img=hcsegmentor.predict(form.cleaned_data['image'])
         circum,res=hcsegmentor.calculate_circum(pred,form.cleaned_data['scale'],)                  
         img,pred=out_image(img,pred)
      val={'circum':circum,'center_x_mm':res[0],'center_y_mm':res[1],'semi_axes_a_mm':res[2],'semi_axes_b_mm':res[3],'angle_rad':res[4]}
      context={'printform':form,'image':img,'segment':pred,'val':val }
      return render(request,'hcsegmentation_home.html',context)   
   else:
      form = HCForm()
   context={'printform':form}
   return render(request,'hcsegmentation_home.html',context)