from django.shortcuts import render
from django.http import HttpResponse
from .encryption_util import *
from meetatt.models import Postpdf, Class, Contact, Folder
from pdfminer import high_level
import re
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
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

def index(request):
    request.session['lv'] = 0
    if request.user.is_anonymous == False:
        print('->',request.user)
        return render(request, "meetatt/home.html", {
            'user': str(request.user),
        })
    else:
        return render(request, "meetatt/home.html", {
            'user': ''
        })


@login_required
def main(request):
    clas = Class.objects.all().order_by('rno')
    userr = User.objects.get(username=request.user)
    return render(request, "meetatt/upload.html", {
        'clas': clas,
        'user': userr
    })


def printa(request, pk):
    if True:
        # fie=request.GET.get('file')
        fie = request.FILES.get('file')
        print("my file ", fie)
        # local_pdf_filename = "../media/files/"+str(fie)
        # pages = [0] # just the first page

        # extracted_text = high_level.extract_text(local_pdf_filename, "", pages)
        # print(extracted_text.split('\n'))
        # fie=request.GET.get('file') it is wrong
        # y=request.user
        # post = pPost.objects.filter(id=id)
        pdf = Postpdf(pdf=fie)
        pdf.save()
        s = Postpdf.objects.filter(pdf=fie)
        # print(s)
        # ds=Postpdf.objects.get(pdf=fie)
        # myid=ds.id
        # print(myid)
        num = Postpdf.objects.all()
        clas = Class.objects.all()
        for i in num:
            x = i.pdf.path
            sid = i.id
        print(x, sid)
        request.session['rno'] = []
        request.session['name'] = []

        local_pdf_filename = x
        request.session['ctn'] = 0
        while True:
            pages = [request.session['ctn']]  # just the first page
            request.session['ctn'] = request.session['ctn']+1
            extracted_text = extract_text(local_pdf_filename, "", pages)
            text = extracted_text.split('\n')
            if (len(text) == 1):
                break
            for i in text:
                z = re.findall("[0-9]{11}", i)
                if (len(z) > 0):
                    request.session['rno'].append(z)
                z = re.findall("[A-z]", i)
                if (len(z) > 0 and "".join(z[-2:]) != 'AM'):
                    z = "".join(z)
                    z = z.lower()
                    request.session['name'].append(z)

                elif (len(z) > 0 and "".join(z[-2:]) == 'AM'):
                    z = "".join(z[:-2])
                    z = z.lower()
                    request.session['name'].append(z)
        print(request.session['name'])
        for i in clas:
            s = [i.rno]
            k = i.name
            k = k.replace(" ", "")
            k = k.lower()
            # print(k)
            d = i.tid.username
            c_id = i.cid.id
            if (s in request.session['rno'] and d == str(request.user) and c_id == int(decrypt(pk))):
                i.mark = i.mark+1
                # print(i.mark)
                i.save()
            if (k in request.session['name'] and d == str(request.user) and c_id == int(decrypt(pk))):
                i.smark = i.smark+1
                i.save()

        # print(rno,name)
        # place = Postpdf.objects.get(pdf=fie)
        # print(place.id)
        instance = Postpdf.objects.get(id=sid)
        instance.delete()
        return redirect('/detail/'+str(pk))
        return render(request, "meetatt/display.html", {
            "rno": rno,
            "name": name,
            "clas": clas
        })


def register(request):
    logout(request)
    if "email" and "name" and "phno" not in request.session:
        request.session["name"] = ""
        request.session["email"] = ""
        request.session["phno"] = ""
    return render(request, 'meetatt/index.html')


def validate_regestration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phno = request.POST.get('phno')
        password = request.POST.get('Password')
        request.session['passw'] = password
        num_results = Contact.objects.filter(email=email).count()
        num_results2 = User.objects.filter(username=username).count()
        if (num_results >= 1):
            messages.success(request, "email already exist")
            return HttpResponseRedirect(request.path_info)
        if (num_results2 >= 1):
            messages.success(request, "user already exist")
            return HttpResponseRedirect(request.path_info)
        try:
            contact = Contact(username=username, name=name,
                              email=email, phoneno=phno, date=datetime.today())
            user = User.objects.create_user(
                username, request.session["email"], password)
            contact.save()
            messages.success(request, "account verified")
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            return redirect('/')
        except:
            messages.success(request, "account not  verified")
            return redirect('/')
    else:
        return redirect('/')


def log_in(request):
    # if user.is_active:
    #     logout(request)
    #     login(request, user)
    if request.user.is_anonymous:
        if (request.method == "POST"):
            username = request.POST.get('logname')
            password = request.POST.get('pasword')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in")
                return redirect('/')
                # Redirect to a success page.

            else:
                messages.success(request, "not valid user name or password")
                return redirect('/')
                # Return an 'invalid login' error message.
        return render(request, 'meetatt/login.html')
    else:
        messages.success(request, "logged in")
        return redirect('/')


def log_out(request):
    logout(request)
    return redirect('/')


@login_required
def head(request):
    if (request.method == 'POST'):
        tit = request.POST.get('head')
        post = get_object_or_404(Contact, username=str(request.user))
        x = Folder(title=tit, fid=post)
        x.save()
        request.session['head'] = 1
        return redirect('/temphead')

    else:
        num = Contact.objects.filter(username=str(request.user))
        post = get_object_or_404(num, username=str(request.user))
        x = Folder.objects.filter(fid=post)
        lt = Folder.objects.filter(fid=post).values('id', 'title')
        request.session['l'] = []
        l = request.session['l']
        for i in lt:
            i['encrypt_key'] = encrypt(i['id'])
            i['title'] = i['title']
            l.append(i)
        print(l)
        # x=Folder.objects.filter(fid=request.user);
        return render(request, 'meetatt/head.html', {
            'folder': l
        })


@login_required
def temphead(request):
    try:
        num = Contact.objects.filter(username=str(request.user))
        post = get_object_or_404(num, username=str(request.user))
        x = Folder.objects.filter(fid=post)
        x = Folder.objects.filter(fid=post)
        lt = Folder.objects.filter(fid=post).values('id', 'title')
        request.session['l'] = []
        l = request.session['l']
        for i in lt:
            i['encrypt_key'] = encrypt(i['id'])
            i['title'] = i['title']
            l.append(i)
        print(l)

        # x=Folder.objects.filter(fid=request.user);
        if request.session['head'] == 1:
            return render(request, 'meetatt/head.html', {
                'folder': l
            })
    except:
        num = Contact.objects.filter(username=str(request.user))
        post = get_object_or_404(num, username=str(request.user))
        x = Folder.objects.filter(fid=post)
        # x=Folder.objects.filter(fid=request.user);
        return render(request, 'meetatt/head.html', {
            'folder': x
        })


@login_required
def quiz(request,pk):
    pk=int(decrypt(pk))
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
        post = get_object_or_404(Folder,id = pk)
        for i in range(len(request.session['c'])):

            if(request.method=="POST"):
                print("POST")
                request.session['z']=request.POST.get(str(request.session['c'][i]))
                request.session['rno']=request.POST.get("rno"+str(request.session['c'][i]))
                print(request.session['z'],request.session['rno'])
                clas=Class(name=request.session['z'],rno=request.session['rno'],tid=cm,cid=post,mark=0,smark=0)
                clas.save()
                print("save the data")
            else:
                break  
        if(request.method=="POST"):      
            return redirect('/head')    
        # print(l)
        
    except: 
        return redirect('/main')
               
    return render(request,"meetatt/newstudent.html",{
        'y':request.session['y']
    })
 


def detail(request, pk):
    xpk = int(decrypt(pk))
    # pk=encrypt(pk)
    clas = Class.objects.all().order_by('rno')
    userr = User.objects.get(username=request.user)
    return render(request, "meetatt/upload.html", {
        'clas': clas,
        'user': userr,
        'pk': pk,
        'xpk': xpk
    })
