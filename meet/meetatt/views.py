from django.shortcuts import render
from django.http import HttpResponse
from .encryption_util import *
from meetatt.models import Postpdf,Class,Contact
from pdfminer import high_level
import re
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
import random
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from datetime import datetime
import webbrowser
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import smtplib
# Create your views here
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.

# def print(request):
#     return render(request,'meetatt/index.html')
def index(request):
    request.session['ym']="";
    print(request.session['ym'])
    request.session['lv']=0
    if request.user.is_anonymous==False:
        request.session['ym']=str(request.user)
        ym=request.session['ym']
        return render(request,"meetatt/home.html",{
            'ym':ym,
        })
    else:
        request.session['ym']="";
        return render(request,"meetatt/home.html",{
            'ym':request.session['ym']
        })

@login_required
def printk(request):

        # fie = request.FILES.get('file')
        # fie=request.GET.get('file') it is wrong
        # y=request.user
    clas = Class.objects.all().order_by('rno')
    userr = User.objects.get(username=request.user)
    # print(userr.username)
        # post = pPost.objects.filter(id=id)
    return render(request,"meetatt/upload.html",{
        'clas':clas,
        'user':userr
    })

def printa(request):
    if  True:
        # fie=request.GET.get('file')
        fie = request.FILES.get('file')
        print("my file ",fie)
        # local_pdf_filename = "../media/files/"+str(fie)
        # pages = [0] # just the first page

        # extracted_text = high_level.extract_text(local_pdf_filename, "", pages)
        # print(extracted_text.split('\n'))
        # fie=request.GET.get('file') it is wrong
        # y=request.user
        
        # post = pPost.objects.filter(id=id)
        pdf=Postpdf(pdf=fie)
        pdf.save()
        s=Postpdf.objects.filter(pdf=fie)
        # print(s)
        # ds=Postpdf.objects.get(pdf=fie)
        # myid=ds.id
        # print(myid)
        num = Postpdf.objects.all()
        clas = Class.objects.all()
        for i in num:
            x=i.pdf.path
            sid=i.id
        print(x,sid)    
        request.session['rno']=[]
        request.session['name']=[] 
        
        local_pdf_filename = x
        request.session['ctn']=0
        while True:
            pages = [request.session['ctn']] # just the first page
            request.session['ctn']=request.session['ctn']+1
            extracted_text = high_level.extract_text(local_pdf_filename, "", pages)
            text=extracted_text.split('\n')
            if(len(text)==1):
                break
            for i in text:
                z=re.findall("[0-9]{11}",i)
                if(len(z)>0):
                    request.session['rno'].append(z)
                z=re.findall("[A-z]",i)
                
                if(len(z)>0 and "".join(z[-2:])!='AM'):
                        request.session['name'].append("".join(z))

                elif(len(z)>0 and "".join(z[-2:])=='AM'):
                    
                    request.session['name'].append("".join(z[:-2]))
        print(request.session['name'])
        for i in clas:
            s=[i.rno]
            k=i.name
            k=k.replace(" ", "")
            print(k)
            d=i.tid.username
            if (s in request.session['rno'] and d==str(request.user)):
                
                i.mark=i.mark+1
                # print(i.mark)
                i.save()
            if (k in request.session['name'] and d==str(request.user)):
                i.smark=i.smark+1
                i.save()
            
        # print(rno,name)
        # place = Postpdf.objects.get(pdf=fie)
        # print(place.id)
        instance = Postpdf.objects.get(id=sid)
        instance.delete()
        return redirect('/main')   
        return render(request,"meetatt/display.html",{
            "rno":rno,
            "name":name,
            "clas":clas
        })    



#for login
def fun(c):
    a=random.randint(25000,90000)
    s=str(a)
    #gmail_user=a
    gmail_user= 'csecodeshef18@gmail.com'
    gmail_password = 'csecodeshef18@gmail'
    sent_from = gmail_user
    to = [c]
    subject = "Your otp"
    #email_text = ntext[0]+"\n"+ntext[1]+"\n"+ntext[2]
    a=random.randint(25000,90000)
    s=str(a)
    email_text=a
    message = 'Subject: {}\n\n{}'.format(subject,email_text)
    try:

        # a=random.randint(25000,90000)
        # s=str(a)
        # send_mail(
        # 'Your OTP',
        # s,
        # 'csecodeshef18@gmail.com',
        # [c],
        # fail_silently=False,
        # )
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to,message)
        server.close()

        return 1,s
    except Exception as e:
        
        return 0,-5

def register(request):
    logout(request)
    if "email" and "name" and "phno" not in request.session:
        request.session["name"] = ""
        request.session["email"] = ""
        request.session["phno"] = ""
        request.session["otp"] = ""
    return render(request,'meetatt/index.html')
    
        

def otp(request):
    if request.method=="POST":
        name=request.POST.get('username')
        email=request.POST.get('email')
        phno=request.POST.get('phno')
        request.session["uname"] = name
        request.session["email"] = email
        request.session["phno"] = phno
        print(email)
        # if User.objects.filter(email = cleaned_info['username']).exists():
        num_results = Contact.objects.filter(email = email).count()
        num_results2 = User.objects.filter(username=name).count()
        print(num_results2)
        if(num_results>=1):
            messages.success(request,"email already exist")  
            return HttpResponseRedirect(request.path_info)
        if(num_results2>=1):
            messages.success(request,"user already exist")  
            return HttpResponseRedirect(request.path_info)
        # x,y=fun(email)
        x,y=(1,234)
        print(y)
        request.session["otp"]=y
        request.session['nvar']=0;
        if(int(y)<0):
            request.session["otp"]=""

        if(x!=1):
            messages.success(request,"Wrong credentials")  
            return HttpResponseRedirect(request.path_info)


        # contact=Contact(name=name,email=email,phoneno=phno,message=message,date=datetime.today())
        # contact.save()
        request.session['var']=1;
    
        return redirect('/newf') 
    # return render(request,'data/otp.html',{
        #     "y":1
        #     }) 
    # if request.method=="POST":
    #     return render(request,'data/otp.html'
    else:
        return redirect('/')
    return redirect('/')
def newf(request):
    try:
        if request.session['var']:
            request.session['var']=0;
            return render(request,'meetatt/otp.html')
        return redirect('/')
    except:
        return redirect('/')

def checkotp(request):
    if request.method=="POST":
        name=request.POST.get('name')
        password=request.POST.get('Password')
        request.session['passw']=password
        # confirmpassword=request.POST.get('conpass')
        otp=request.POST.get('otp')
        username=request.session["uname"]
        if(request.session["otp"]==otp):
            try:
                contact=Contact(username=username,name=name,email=request.session["email"],phoneno=request.session["phno"],date=datetime.today())
                user = User.objects.create_user(username, request.session["email"], password)
                contact.save()
                messages.success(request,"account verified")
                u = User.objects.get(username=username)
                u.set_password(password)
                u.save()
                del request.session['email']
                request.session['otp']="-112s6a"
                return redirect('/')
            except:
                messages.success(request,"user exist")
                request.session['otp']="-112s6a"
                return redirect('/')
        else:
            messages.success(request,"account not  verified")
            # del request.session['otp']
            request.session['otp']="-112s6a"
            return redirect('/')

    else:
        return redirect('/')


def log_in(request):
    # if user.is_active:
    #     logout(request)
    #     login(request, user)
    if request.user.is_anonymous:
            

        if(request.method=="POST"):
            username=request.POST.get('logname')
            password=request.POST.get('pasword')  
            user = authenticate(request, username=username, password=password)
            if user is not None:
                  
                login(request, user)
                if(request.session['lv']==1):
                    request.session['lv']=0
                    return redirect('/printk')
                messages.success(request,"Successfully logged in")     
                return redirect('/')
                # Redirect to a success page.
                
            else:
                messages.success(request,"not valid user name or password") 
                return redirect('/')

                # Return an 'invalid login' error message.
        return render(request,'meetatt/login.html')      
    else:
        messages.success(request,"logged in") 
        return redirect('/')     

def log_out(request):
    logout(request)
    return redirect('/')


@login_required
def quiz(request):
    print('--->');
    request.session['x']=request.GET.get('i')
    request.session['l']=[]
    if(request.session['x'] is None):
        request.session['y']=[]
        request.session['c']=[]
    else:
        request.session['y']=[i+1 for i in range(int(request.session['x']))]
        request.session['c']=[i+1 for i in range(int(request.session['x']))]
        # zl=len(c)
        # print(zl)
    try:
        cm=Contact.objects.get(username=str(request.user))
        for i in range(len(request.session['c'])):
            if(request.method=="POST"):
                print("POST")
                request.session['z']=request.POST.get(str(request.session['c'][i]))
                request.session['rno']=request.POST.get("rno"+str(request.session['c'][i]))
                clas=Class(name=request.session['z'],rno=request.session['rno'],tid=cm,mark=0)
                clas.save()
                print("save the data")
            else:
                break  
        if(request.method=="POST"):      
            return redirect('/main')    
        # print(l)
        
    except: 
        print('error')
        return redirect('/main')
               
    return render(request,"meetatt/newstudent.html",{
        'y':request.session['y']
    })
 

@login_required
def resetutil(request):
    if(request.method=="POST"):
            y=str(request.user)
            print(y)
            u = User.objects.get(username=y)
            password=request.POST.get('opas')
            npas=request.POST.get('rpas')  
            user = authenticate(request, username=y, password=password)
            if user is not None:
                print(password,npas)
                hashv=encrypt(y)+"/"+encrypt(password)+"/"+encrypt(npas)
                weblink="http://127.0.0.1:8000/reset/"+hashv
                print(weblink)
                gmail_user= 'csecodeshef18@gmail.com'
                gmail_password = 'csecodeshef18@gmail'
                sent_from = gmail_user
                to = [u.email]
                subject = "Password reset link"
                #email_text = ntext[0]+"\n"+ntext[1]+"\n"+ntext[2]
                
                email_text=weblink
                message = 'Subject: {}\n\n{}'.format(subject,email_text)
                try:

                    # a=random.randint(25000,90000)
                    # s=str(a)
                    # send_mail(
                    # 'Your OTP',
                    # s,
                    # 'csecodeshef18@gmail.com',
                    # [c],
                    # fail_silently=False,
                    # )
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to,message)
                    server.close()
                    messages.success(request,"Reset request send to mail")
                    return redirect('/') 
                except Exception as e:
                    messages.success(request,"Some error occured in sending mail")
                    return redirect('/')
                messages.success(request,"in")     
                return redirect('/')
                # Redirect to a success page.
                
            else:
                messages.success(request,"not valid password") 
                return redirect('/')
    return render(request,"meetatt/reset.html")        


def reset(request,a,b,c):
    try:
        a=decrypt(a)
        b=decrypt(b)
        c=decrypt(c)
        print("values",a,b,c)
        u = User.objects.get(username=str(request.user))
        user = authenticate(request, username=str(request.user), password=b)
        print(user)
        if user is not None:
            u.set_password(c)
            u.save()
            messages.success(request,"Password change successhul") 
            return redirect('/')
        else:
            messages.success(request,"Not allowed") 
            return redirect('/')
    except:
        messages.success(request,"Not allowed") 
        return redirect('/')


def forget(request):
    if request.method=="POST":
        a=request.POST.get('flogin')
        b=request.POST.get('femail')
        c=request.POST.get('fpass')
        u = User.objects.get(username=a)
        if(u.email==b):
            if True:
                hashv=encrypt(a)+"/"+encrypt(b)+"/"+encrypt(c)
                weblink="http://127.0.0.1:8000/changepassword/"+hashv
                print(weblink)
                gmail_user= 'csecodeshef18@gmail.com'
                gmail_password = 'csecodeshef18@gmail'
                sent_from = gmail_user
                to = [u.email]
                subject = "Change the Password "
                #email_text = ntext[0]+"\n"+ntext[1]+"\n"+ntext[2]
                
                email_text=weblink
                message = 'Subject: {}\n\n{}'.format(subject,email_text)
                try:

                    # a=random.randint(25000,90000)
                    # s=str(a)
                    # send_mail(
                    # 'Your OTP',
                    # s,
                    # 'csecodeshef18@gmail.com',
                    # [c],
                    # fail_silently=False,
                    # )
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to,message)
                    server.close()
                    messages.success(request,"Reset request send to mail")
                    return redirect('/') 
                except Exception as e:
                    messages.success(request,"Some error occured in sending mail")
                    return redirect('/')     
                return redirect('/')
                # Redirect to a success page.
                
            else:
                messages.success(request,"not valid password") 
                return redirect('/')



    return render(request,'meetatt/forget.html')



def forgetutil(request,a,b,c):
    try:

        a=decrypt(a)
        b=decrypt(b)
        c=decrypt(c)
        # print("values",a,b,c)
        u = User.objects.get(username=a)
        if True:
            u.set_password(c)
            u.save()
            messages.success(request,"Password change successful") 
            return redirect('/')
        else:
            messages.success(request,"Not allowed") 
            return redirect('/')
    except:
        messages.success(request,"Not allowed") 
        return redirect('/')    