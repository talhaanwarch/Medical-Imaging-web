from django.forms import ModelForm
from .models import UploadModel

class UploadForm(ModelForm):
	class Meta:
		model=UploadModel
		fields='__all__'