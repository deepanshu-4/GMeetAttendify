from django.shortcuts import render,HttpResponseRedirect
from .forms import studentregistration
# Create your views here.
from .models import User
def addshow(request):
    if request.method=='POST':
        fm=studentregistration(request.POST)
        if fm.is_valid():
            nm=fm.cleaned_data['name']
            em=fm.cleaned_data['email']
            pw=fm.cleaned_data['password']
            reg=User(name=nm,email=em,password=pw)
            reg.save()
            
            fm=studentregistration()
            im=User.objects.all()            
    else:
        
        fm=studentregistration()
    im=User.objects.all()
    return render(request,'enroll/addandshow.html',{
        'form':fm,
        'st':im
    })
def delete(request,id):
    if request.method=="POST":
        pi=User.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')

def update(request,id):
    if request.method=="POST":
        pi=User.objects.get(pk=id)
        fm=studentregistration(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=User.objects.get(pk=id)
        fm=studentregistration(instance=pi)        
    return render(request,'enroll/update.html',{
        'id':id,
        "form":fm
    })        