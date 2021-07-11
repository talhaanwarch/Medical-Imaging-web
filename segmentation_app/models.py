from django.db import models

# Create your models here.
MODEL_CHOICES = (
    ('ultrasound','Ultrasound'), #2nd field display in front
    # ( 'ecg','Cardiology'),
    # ('xray','Radiology'),
    # ('covid','COVID'),
   
)

class UploadModel(models.Model):
	name=models.CharField(max_length=50)
	aImodels=models.CharField(max_length=15, choices=MODEL_CHOICES)
	image=models.ImageField('image')