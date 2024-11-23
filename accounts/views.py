from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.shortcuts import *
from django.http import HttpResponse, JsonResponse
from .models import *
from django.utils import *
from django.core.serializers import serialize
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from chat.models import *
from chat.forms import SharedFileForm

def index(request):
    form = SharedFileForm()
    
    if request.method == 'POST':
        form = SharedFileForm(request.POST, request.FILES)
        if form.is_valid():
            shared_file = form.save(commit=False)
            shared_file.user = request.user
            shared_file.save()
            return redirect('index')
    
    context = {
        'form': form,
        'shared_files': SharedFile.objects.all().order_by('-uploaded_at')
    }
    return render(request, 'index.html', context)

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')



def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        
        if next and next != request.path:  # Check if next is different from the current URL
            return redirect(next)
        
        return redirect(reverse('index'))  # Redirect to index if next is not provided or causes a loop

    context = {
        'form': form,
    }
    return render(request, "accounts/login.html", context)



@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'profile_user': user,
        'gender': user.gender,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined,
    }
    return render(request, 'accounts/profile.html', context)

