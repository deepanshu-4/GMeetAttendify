from django.urls import path
from . import views
app_name="meetatt"
urlpatterns = [
    path("",views.index,name="index"),
    path("validate_regestration",views.validate_regestration,name="validate_regestration"),
    path("register",views.register,name="register"),
    path("login",views.log_in,name="log_in"),
    path("logout",views.log_out,name="log_out"),
    path("main",views.main,name="main"),
    path("newstudent/<str:pk>/",views.quiz,name="quiz"),
    path("printa/<str:pk>/",views.printa,name="printa"),
    path("head",views.head,name="head"),
    path("temphead",views.temphead,name="temphead"),
    path("detail/<str:pk>/",views.detail,name="detail"),
]
