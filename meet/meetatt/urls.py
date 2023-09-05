from django.urls import path
from . import views
app_name="meetatt"
urlpatterns = [
    path("",views.index,name="index"),
    path("otp",views.otp,name="otp"),
    path("newf",views.newf,name="newf"),
    path("checkotp",views.checkotp,name="checkotp"),
    path("register",views.register,name="register"),
    path("login",views.log_in,name="log_in"),
    path("logout",views.log_out,name="log_out"),
    path("main",views.printk,name="main"),
    path("newstudent",views.quiz,name="quiz"),
    path("resetutil",views.resetutil,name="resetutil"),
    path("changepassword/<str:a>/<str:b>/<str:c>/",views.forgetutil,name="forgetutil"),
    path("forget",views.forget,name="forget"),
    path("reset/<str:a>/<str:b>/<str:c>/",views.reset,name="reset"),
    path("printa",views.printa,name="printa")
]
