from rest_framework import serializers
from .models import UploadModel

class UploadSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=UploadModel
		fields='__all__'