from django.contrib import admin
from django.urls import path,include
from cva import views

urlpatterns = [
    path("",views.index,name='home'),
    path("talk",views.supportRender,name="talk-to-support"),
    path("sendText",views.processText,name="textProcessing"),
    path("login",views.login,name="loginPage"),
]
