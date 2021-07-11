from django.shortcuts import render
from rest_framework import viewsets
from .models import UploadModel
from .serializers import UploadSerializer
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

class Imageuploadviewset(viewsets.ModelViewSet):
   queryset = UploadModel.objects.all()
   serializer_class = UploadSerializer
   # def list(self, request):
   #    print("list in TaskViewSet")
   #    return Response({"list in TaskViewSet"})

   def create(self, request):
      ai=request.POST['aImodels']
      img=request.FILES['image']
      user=request.POST['name']
      pred=predictor.predict(ai,img)
      print("create in TaskViewSet")
      return JsonResponse({'user':user,'model':ai,'prediction':pred})


   # def retrieve(self, request, pk=None):
   #    print("retrieve in TaskViewSet")
   #    return Response("retrieve in TaskViewSet")


   # def update(self, request, pk=None):
   #    print("update in TaskViewSet")
   #    return Response("update in TaskViewSet")


   # def partial_update(self, request, pk=None):
   #    print("partial_update in TaskViewSet")
   #    return Response("partial_update in TaskViewSet",)


   # def destroy(self, request, pk=None):
   #    print("destroy in TaskViewSet")
   #    return Response("destroy in TaskViewSet")

# class FileUploadView(APIView):
#     permission_classes = []
#     parser_class = (FileUploadParser,)
#     def get(self,request):
#         if request.method == 'GET':
#         	return return JsonResponse(response)

#     def post(self, request, *args, **kwargs):

#       file_serializer = UploadSerializer(data=request.data)

#       if file_serializer.is_valid():
#           file_serializer.save()
#           return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#       else:
#           return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .forms import UploadForm
from .py_templates import predictor
# Create your views here.
def home(request):
   if request.method == 'POST':
      form = UploadForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         pred=predictor.predict(form.cleaned_data['aImodels'],form.cleaned_data['image'])
      context={'printform':form,'pred':pred}
      return render(request,'classification_home.html',context)   
   else:
      form = UploadForm()
   context={'printform':form}
   return render(request,'classification_home.html',context)