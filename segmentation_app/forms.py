from django.forms import ModelForm
from .models import UploadModel,HCModel

class UploadForm(ModelForm):
	class Meta:
		model=UploadModel
		fields='__all__'

class HCForm(ModelForm):
	class Meta:
		model=HCModel
		fields='__all__'