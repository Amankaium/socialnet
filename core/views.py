from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.
def homepage(request):
    context = {}
    context["name"] = "Kaium"
    posts_list = Post.objects.all() # SELECT * FROM Post;
    context["posts"] = posts_list
    return render(request, "home.html", context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context["post"] = post_object
    return render(request, "post_info.html", context)


def profile_detail(request, id):
    context = {}
    context['profile'] = Profile.objects.get(id=id)
    return render(request, 'profile_detail.html', context)
