from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from core.models import File
from core.serializers import FileSerializer
from django.shortcuts import redirect

@csrf_exempt
def file_list ( request ):
    if request.method == 'GET':
        snippets = File.objects.all()
        serializer = FileSerializer ( snippets, many = True )
        return JsonResponse ( serializer.data, safe = False )

    elif request.method == 'POST':
        data = JSONParser().parse ( request )
        serializer = FileSerializer ( data = data )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse ( serializer.data, status = 201 )
        return JsonResponse ( serializer.errors, status = 400 )

@csrf_exempt
def file_cat ( request, cat ):
    if request.method == 'GET':
        snippets = File.objects.filter( path__startswith = cat )
        serializer = FileSerializer ( snippets, many = True )
        return JsonResponse ( serializer.data, safe = False )

@csrf_exempt
def file_detail ( request, sdb, fn ):
    try:
        snippet = File.objects.get ( path = sdb + "/" + fn )
    except File.DoesNotExist:
        if request.method == "PUT" :
            data = JSONParser().parse ( request )
            serializer = FileSerializer ( data = data )
            if serializer.is_valid():
                serializer.save()
                return JsonResponse ( serializer.data, status = 201 )
            return JsonResponse ( serializer.errors, status = 400 )
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FileSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FileSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


