from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import datetime
from .trajectoryPredictor import TrajectoryPredictor
import json
from random import randrange
from django.http import HttpResponse
from pyecharts.charts import Line
from pyecharts import options as opts
from .models import TrajectoryData,Station,TrajectoryRecord,NextMinTrajectory
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from .manageStaion import addStation
from .serializers import NextMinTrajectorySerializer
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class TaskList(APIView):
    def get(self, request, format=None):
        tasks = NextMinTrajectory.objects.all()
        serializer = NextMinTrajectorySerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        nextMinPredictor = TrajectoryPredictor()
        try:
            longitude,latitude,altitude = float(request.POST["longitude"]),float(request.POST["latitude"]),float(request.POST["altitude"])
            pressure, temperature, humid = float(request.POST["pressure"]), float(request.POST["temperature"]), float(request.POST["humid"])
            nspeed, espeed, uspeed = float(request.POST["nspeed"]), float(request.POST["espeed"]), float(request.POST["uspeed"])
            one_X = [pressure, temperature, humid, nspeed, espeed, uspeed, longitude, latitude, altitude]
            nextlongtitude,nextlatitude,nextaltitude=nextMinPredictor.makeNextMinPrediction(one_X)
            serializer = NextMinTrajectorySerializer(data={"longitude":nextlongtitude,"latitude":nextlatitude,"altitude":nextaltitude})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("参数错误", status=status.HTTP_400_BAD_REQUEST)


def index(request):
    content={}
    content['user']=request.user
    return render(request,'main/index.html',context=content)

def tologin(request):
    if request.method == 'POST':
        return login_check(request)
    else:
        return render(request, 'main/login.html',{'login_info':0})

def login_check(request):
    useremail = request.POST.get('username')
    password = request.POST.get('password')
    n=authenticate(username=useremail,password=password)
    print(n)
    if n:
        login(request,user=n)
        return HttpResponseRedirect(reverse('main:index'))
    return render(request, 'main/login.html')

def register(request):
    if request.method == 'POST':
        return register_check(request)
    else:
        return render(request, 'main/register.html')

def register_check(request):
    useremail = request.POST.get('email')
    password = request.POST.get('password')
    username=request.POST.get('username')
    u=User.objects.filter(email=useremail).first()
    if not u:
        User.objects.create_user(username=username,email=useremail,password=password)
        return HttpResponseRedirect(reverse('main:login'))
    return render(request, 'main/register.html')

def tologout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

@login_required
def trajectory(request):
    content = {}
    content['user'] = request.user
    global trajectoryPredictor
    trajectoryPredictor=TrajectoryPredictor()

    stations = Station.objects.all()
    content["stations"] = stations
    return render(request, 'main/trajectory.html',context=content)

@login_required
def trajectorySeries(request):
    stationId, stationName = request.POST["stationId"].split()
    stationId=int(stationId)
    pressure,temperature,humid=float(request.POST["pressure"]),float(request.POST["temperature"]),float(request.POST["humid"])
    nspeed,espeed,uspeed=float(request.POST["nspeed"]),float(request.POST["espeed"]),float(request.POST["uspeed"])
    stationObj=Station.objects.get(stationId=stationId)
    longitude,latitude=stationObj.longitude,stationObj.latitude
    altitude=float(request.POST["altitude"])
    one_X=[pressure,temperature,humid,nspeed,espeed,uspeed,longitude,latitude,altitude]

    longitudes, latitudes, altitudes=trajectoryPredictor.makeAPrediction(one_X)
    longitudes.insert(0,longitude)
    latitudes.insert(0,latitude)
    altitudes.insert(0,latitude)
    content={}
    content['user'] = request.user
    content['longitudes']=longitudes
    content['latitudes']=latitudes
    content['altitudes']=altitudes
    content['stationName']=stationObj.stationName
    content['stationLongitude'],content['stationLatitude']=longitude,latitude
    return render(request, 'main/trajectoryMap.html',context=content)

@login_required
def historyPage(request):
    return HttpResponseRedirect(reverse('main:manageStation'))

@login_required
def manageStation(request):
    content = {}
    content['user'] = request.user
    stations = Station.objects.all()
    content["longitude"] = [s.longitude for s in stations]
    content["latitude"] = [s.latitude for s in stations]
    content["altitude"] = [s.altitude for s in stations]
    content["name"] = [str(s.stationId) + str(s.stationName) for s in stations]
    content["stations"]=stations
    return render(request, 'main/manageStation.html', context=content)








@login_required
def modelPage(request):
    return render(request, 'main/model.html')



