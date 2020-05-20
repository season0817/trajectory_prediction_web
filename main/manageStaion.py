from .models import Station
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

def addStation(request):
    stationId = request.POST["stationId"]
    stationName = request.POST["stationName"]
    altitude = request.POST["altitude"]
    longitude = request.POST["longitude"]
    latitude = request.POST["latitude"]
    Station.objects.create(stationId=stationId,stationName=stationName,
                           altitude=altitude,longitude=longitude,latitude=latitude)
    return HttpResponseRedirect(reverse('main:manageStation'))