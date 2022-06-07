from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Chirp
from .forms import ChirpForm


def index(request):

    messages = Chirp.objects.all()
    messages = messages.order_by('-timestamp').all()
    try:
        user = User.objects.get(username=request.user)
    except:
        user = None
    context = {}
    try:
        likelist = (user.likedchirps).split(',')
    except:
        likelist = []

    for message in messages:
        isIn = str(message.id) in likelist
        context.update({message.id: {'isIn': isIn}})
    print(context)

    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    if request.method == "POST":
        print('POST gotten')
        formtype = request.POST.get('form_type')
        print('formtype is ' + formtype)
        if formtype == 'form_newchirp':
            print('formtype gotten')
            chirpForm = ChirpForm(request.POST)
            if chirpForm.is_valid():
                print('is valid')
                newChirp = Chirp.objects.create(
                    owner=request.user, chirp=request.POST.get('chirp'), likes = 0
                )
                newChirp.save()
                messages = Chirp.objects.all()
                messages = messages.order_by('-timestamp').all()
                for message in messages:
                    isIn = str(message.id) in likelist
                    context.update({message.id: {'isIn': isIn}})

                paginator = Paginator(messages, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                return render(request, "network/index.html", {
                    'chirps': messages,
                    'chirpform': ChirpForm(),
                    'context': context,
                    'page_obj': page_obj
                })

    return render(request, "network/index.html", {
        'chirps': messages,
        'chirpform': ChirpForm(),
        'context': context,
        'page_obj': page_obj
    })

#API view
@csrf_exempt
def chirp(request, chirpID=None, profileuser=None):
    try:
        user = User.objects.get(username=request.user)
    except:
        print(request.user)
        return JsonResponse({"error": "User not found."}, status=404)
    if chirpID is not None:
        chirp = Chirp.objects.get(pk=chirpID)

    if profileuser is not None:
        profileuser = User.objects.get(username=profileuser)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('action') == 'Like':
            chirp.likes = chirp.likes + 1
            chirp.save()
            try:
                likelist = (user.likedchirps).split(',')
            except:
                likelist = []
            likelist.append(str(chirpID))
            user.likedchirps = ','.join(likelist)
            user.save()
        elif data.get('action') == 'Unlike':
            chirp.likes = chirp.likes - 1
            chirp.save()
            likelist = (user.likedchirps).split(',')
            likelist.remove(str(chirpID))
            user.likedchirps = ','.join(likelist)
            user.save()
        elif data.get('action') == 'Edit':
            print('trying to edit')
            if chirp.owner == user:
                print("we're the owner")
                chirp.chirp = data.get('context')
                chirp.save()
            else:
                print("we're not the owner")
                return JsonResponse({'error': "You must be the chirp's owner to edit it."}, status=404)
        ###### NEED TO CHECK PROFILE'S USERID AND ADD IT TO USER'S FOLLOW LIST ON PUT
        elif data.get('action') == 'setFollow':
            print('Adding to follower list')
            try:
                followlist = (user.following).split(',')
                print('no exception')
            except:
                print('exception')
                followlist = []

            followlist.append(str(profileuser.id))
            print(followlist)
            if len(followlist) == 1:
                user.following = followlist[0]
                print('adding first followed')
            else:
                user.following = ','.join(followlist)
            user.save()
            profileuser.followcount = profileuser.followcount + 1
            profileuser.save()
        elif data.get('action') == 'setUnfollow':
            print('Taking off of follower list')
            try:
                followlist = (user.following).split(',')
                print('split successful')
            except:
                print('split not successful')
                followlist = []
            followlist.remove(str(profileuser.id))
            print(followlist)
            user.following = ','.join(followlist)
            user.save()
            profileuser.followcount = profileuser.followcount -1
            profileuser.save()

        return HttpResponse(status=204)
    else:
        return JsonResponse({
            'error': 'request method must be PUT'
        }, status=400)

@login_required
def profile(request, username):
    #user is who we are, profileuser is whose page we're on
    user = User.objects.get(username=request.user)
    profileuser = User.objects.get(username=username)
    messages = Chirp.objects.filter(owner=profileuser)
    messages = messages.order_by('-timestamp').all()
    context = {}
    followlist = []
    following = False
    followercount = profileuser.followcount
    try:
        followedcount = (profileuser.following).split(',')
    except:
        followedcount = []

    print(followedcount)

    try:
        likelist = (user.likedchirps).split(',')
    except:
        likelist = []

    try:
        followlist = (user.following).split(',')
    except:
        following = False

    if str(profileuser.id) in followlist:
        print('already following')
        following = True

    for message in messages:
        isIn = str(message.id) in likelist
        context.update({message.id: {'isIn': isIn}})

    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/profile.html', {
        'user': user,
        'chirps': messages,
        'context': context,
        'currentprofile': username,
        'isfollowing': following,
        'followercount': followercount,
        'followedcount': len(followedcount),
        'page_obj': page_obj
    })

@login_required
def following(request):
    user = User.objects.get(username=request.user)
    followlist = user.following
    followlist = followlist.split(',')
    followlist = list(filter(None, followlist))
    #print('FOLLOWLIST IS')
    #print(followlist)
    #print(list(filter(None, followlist)))
    followedchirps = Chirp.objects.filter(owner__in=followlist)
    print(followedchirps)
    context={}

    try:
        likelist = (user.likedchirps).split(',')
    except:
        likelist = []

    for message in followedchirps:
        isIn = str(message.id) in likelist
        context.update({message.id: {'isIn': isIn}})

    paginator = Paginator(followedchirps, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/index.html', {
        'chirps': followedchirps,
        'chirpform': ChirpForm(),
        'context': context,
        'page_obj': page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
