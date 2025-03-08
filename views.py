from django.shortcuts import render,redirect
from Face_Detection.detection import FaceRecognition
from .forms import *
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
faceRecognition = FaceRecognition()

from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'greeting.html', {})



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered")
            addFace(request.POST['face_id'])  # Assurez-vous que addFace est correctement défini
            return redirect('home')  # Ajoutez return ici pour la redirection
        else:
            messages.error(request, "Account registration failed")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('/')

def login(request):
    face_id = faceRecognition.recognizeFace()
    print(face_id)
    return redirect('greeting' ,str(face_id))

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def user_profile(request):
    #user = request.user  # Assuming you have set up user authentication
    #profile = UserProfile.objects.get(forms)  # Replace with how you retrieve the user's profile
    form = RegistrationForm(instance=UserProfile)  # Assuming you've imported RegistrationForm

    return render(request, 'profile.html', {'form': form})

    
    
    



def Greeting(request, face_id):
    try:
        face_id = int(face_id)
        user_profile = get_object_or_404(UserProfile, face_id=face_id)
        context = {'user': user_profile}
        return render(request, 'greeting.html', context=context)
    except UserProfile.DoesNotExist:
        error_message = f"UserProfile with face_id {face_id} does not exist"
        context = {'error_message': error_message}
        return render(request, 'error.html', context=context)

def common(request):
        return render(request,'common.html',{})

