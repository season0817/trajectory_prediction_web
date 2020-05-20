from django.db import models

# Create your models here.
class Station(models.Model):
    stationId=models.IntegerField(verbose_name="放球站ID",unique=True,null=False)
    stationName=models.CharField(max_length=100,verbose_name="放球站")
    altitude=models.FloatField(verbose_name="海拔")
    longitude=models.FloatField(verbose_name="经度")
    latitude = models.FloatField(verbose_name="纬度")

class Sonde(models.Model):
    sondeId = models.CharField(max_length=10,verbose_name="探空仪ID",unique=True,null=False)
    description=models.CharField(max_length=200,verbose_name="描述")

class TrajectoryRecord(models.Model):
    startDatetime=models.DateTimeField()
    endDatetime=models.DateTimeField()
    stationId = models.ForeignKey('Station', on_delete=models.CASCADE
                ,to_field='stationId',verbose_name="放球站ID")
    sondeId = models.CharField(max_length=10,verbose_name="探空仪ID")

class TrajectoryData(models.Model):
    datetime = models.DateTimeField()
    pressure = models.FloatField(verbose_name="气压")
    temperature = models.FloatField(verbose_name="温度")
    humid = models.FloatField(verbose_name="湿度")
    nspeed = models.FloatField(verbose_name="北向速度")
    espeed = models.FloatField(verbose_name="东向速度")
    uspeed = models.FloatField(verbose_name="上升速度")
    longitude = models.FloatField(verbose_name="经度")
    latitude = models.FloatField(verbose_name="纬度")
    altitude = models.FloatField(verbose_name="海拔")
    trajectoryRecordId=models.ForeignKey('TrajectoryRecord', on_delete=models.CASCADE
                ,verbose_name="记录ID")
    class Meta:
        ordering = ['datetime']

class user(models.Model):
    email = models.CharField(max_length=30, unique=True)
    username=models.CharField(max_length=30)
    password = models.CharField(max_length=12)

class NextMinTrajectory(models.Model):
    longitude = models.FloatField(verbose_name="经度")
    latitude = models.FloatField(verbose_name="纬度")
    altitude = models.FloatField(verbose_name="海拔")

