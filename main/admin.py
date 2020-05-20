from django.contrib import admin
from .models import Sonde,Station,TrajectoryData,TrajectoryRecord,NextMinTrajectory
# Register your models here.
admin.site.register(Sonde)
admin.site.register(Station)
admin.site.register(TrajectoryData)
admin.site.register(TrajectoryRecord)
admin.site.register(NextMinTrajectory)
