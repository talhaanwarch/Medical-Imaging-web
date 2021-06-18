# Medical-Imaging-App
make template ready till okie

## Create a model
```
class UploadModel(models.Model):
	name=models.CharField(max_length=50)
	image=models.ImageField('images')
```
## Create a form (`forms.py`)
```
from django.forms import ModelForm
from .models import UploadModel

class UploadForm(ModelForm):
	class Meta:
		model=UploadModel
		fields='__all__'
```
## Register the model (`admin.py`)
```
from . models import UploadModel
admin.site.register(UploadModel)
```
## Create function to save form (`views.py`)
`request.FILES` is necessary if a file or image field is added
```
from .forms import UploadForm
def home(request):
   if request.method == 'POST':
      form = UploadForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
   else:
      form = UploadForm()
   context={'printform':form}
   return render(request,'home.html',context)
```
## Add from to templated (`home.html`)
```
<form action="" method="post" enctype="multipart/form-data"> 
    {% csrf_token %}
    {{ printform.as_p }}
<input type="submit" value="Submit">

 </form>
```
