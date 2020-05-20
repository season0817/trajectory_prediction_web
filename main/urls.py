from django.urls import path,include
from main import views
from rest_framework import routers
app_name="main"


urlpatterns=[
    path('',views.index,name='index'),
    path('tasks/', views.TaskList.as_view(), name='task_list'),
    path('login',views.tologin,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.tologout,name='logout'),
    path('addStation',views.addStation,name='addStation'),
    path('prediction',views.trajectory,name='prediction'),
    path('prediction/trajectorySeries',views.trajectorySeries,name='trajectorySeries'),
    path('history',views.historyPage,name='history'),
    path('history/manageStation',views.manageStation,name="manageStation"),
    path('model',views.modelPage,name='model'),
]