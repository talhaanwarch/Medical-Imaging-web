from django.shortcuts import render
# def home(request):
# 	return render(request,'segmentation_home.html',{'print':"every thing ok"})
import io
import base64
import numpy as np
from .forms import UploadForm
from .py_templates import segmentor
# Create your views here.

def out_image(image):
   #https://stackoverflow.com/a/40568024/11170350
   data = io.BytesIO()
   image.save(data, "JPEG")
   encoded_img_data = base64.b64encode(data.getvalue())
   out=encoded_img_data.decode('utf-8')
   return out

def home(request):
   if request.method == 'POST':
      form = UploadForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         image,segment=segmentor.predict(form.cleaned_data['image'])                  
         segment=out_image(segment)
         image=out_image(image)
      context={'printform':form,'image':image,'segment':segment }
      return render(request,'segmentation_home.html',context)   
   else:
      form = UploadForm()
   context={'printform':form}
   return render(request,'segmentation_home.html',context)