from django.shortcuts import render

from blog.models import Profile


def home_view(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'home_page.html', context)
