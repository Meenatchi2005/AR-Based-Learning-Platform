from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from utils.decorator import login_required_message
from django.contrib.auth.decorators import login_required

from .models import Subject, Topic, Hotspot   # ✅ IMPORT HOTSPOT
from utils.email_sender import send_mail
from django.contrib.auth import authenticate, login, logout


# ================= HOME =================
def index(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects
    }
    return render(request, 'mainapp/index.html', context)


# ================= SUBJECT PAGE =================
@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def subject(request, name):
    subject = get_object_or_404(Subject, name=name)
    topics = Topic.objects.filter(subject=subject)

    context = {
        'subject': subject,
        'topics': topics,
    }
    return render(request, 'mainapp/subject/subject.html', context)


# ================= SEND EMAIL =================
@login_required
def send_email(request):
    if request.method == 'POST':
        data = request.POST

        receiver_email = data['email']
        sender_name = data['sender_name']
        sender_email = data['sender_email']
        subject_name = data['subject_name']
        topic_name = data['topic_name']
        effect_link = data['effect_link']

        send_mail(
            receiver_email,
            sender_name,
            sender_email,
            subject_name,
            topic_name,
            effect_link
        )

        messages.info(request, f'Email sent to {receiver_email}')
        return redirect('subject', subject_name)

    return redirect('home')


# ================= 3D VIEW PAGE =================
@login_required
def view_3d(request, id):
    topic = get_object_or_404(Topic, id=id)

    # ✅ GET HOTSPOTS FOR THIS TOPIC
    hotspots = Hotspot.objects.filter(topic=topic)

    context = {
        'topic': topic,
        'hotspots': hotspots
    }

    return render(request, 'mainapp/view_3d.html', context)

# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'mainapp/login.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def subject_list(request):
    return render(request, 'mainapp/subjects.html')
