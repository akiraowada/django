from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, list_route
import os
from rest_framework.response import Response

from .models import Image
from .serializer import ImageSerializer

UPLOAD_DIR = 'static/uploaded_photo/'

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request):
        file = request.FILES['file']
        print('TEST1')
        path = os.path.join(UPLOAD_DIR, file.name)
        print('TEST2')
        destination = open(path, 'wb')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        print('TEST3')
        if not os.path.exists(path):
            print('File not found:', path)
            return create_render(request)
        print('TEST4', path)
        image, created = Image.objects.get_or_create(filepath=path)
        print('TEST5')
        if created:
            # image.sender = request.POST['sender']
            image.title = request.POST['title']
            image.body = request.POST['body']
            image.created_at = request.POST['created_at']
            image.updated_at = request.POST['updated_at']
            image.lat = float(request.POST['lat'])
            image.lng = float(request.POST['lng'])
            image.status = request.POST['status']
            image.save()

        return Response({'message': 'OK'})
