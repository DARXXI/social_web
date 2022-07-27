from multiprocessing import context
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.http.response import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# rooms = [
#     {'id': 1, 'name':'Lets learn python'},
#     {'id': 2, 'name':'Design with me'},
#     {'id': 3, 'name':'Frontend devops'},
# ]
def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username) 
        except:
            messages.add_message(request, messages.ERROR, 'no such a user')

        user = authenticate(request, username=username, password=password)#matching
        if user is not None:
            login(request, user) #creates session in browser
            return redirect('home')
        else:
            messages.error(request, 'incorrect password')
    context={}
    return render(request,'base/login.html', context)     

def logoutPage(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(host__username__icontains=q)
    )

    room_count = rooms.count()
    #querring upwards topic__name -> check models

    topics = Topic.objects.all()
    context = {'rooms': rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    #get = select some FROM table X
    context = {'room': room}
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        #print(request.POST)
        form = RoomForm(request.POST)
        #знаем всё я форме
        if form.is_valid():
            form.save()
            #save() - return the model instance to the databse
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    #видно как было         
    if request.user != room.host:
        return HttpResponse("It's not you'r room")
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            #save() - return the model instance to the databse
            return redirect('home') 

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.filter(id=pk)
    if request.method == 'POST':
        room.delete()
        #save() - return the model instance to the databse
        return redirect('home') 
    
    return render(request,'base/delete.html', {'obj': room})
